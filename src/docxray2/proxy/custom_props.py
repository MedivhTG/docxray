from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_dpc import E_Properties, E_Property, PropertyValue
from docxray2.oxml.shared_dpvt import E_I4, E_Bool, E_Filetime, E_Lpwstr
from docxray2.parts.types import ProvidesDocxXmlPart
from docxray2.xsd.w3cdtf import W3CDTFDateTime

from .base import DocxElementProxy, DocxParentedElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.custom_file_properties import (  # noqa: F401
        CustomFilePropertiesPart,
    )

CUSTOM_PROPERTIES_GUID = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}"
PID_MIN = 2


class CustomProperties(
    DocxElementProxy[E_Properties, "CustomFilePropertiesPart"]
):
    def __init__(
        self, element: E_Properties, parent: ProvidesDocxXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._props: list[Property] = []
        self._pids_map: dict[int, Property] = {}
        self._names_map: dict[str, Property] = {}
        for prop_elm in self.element.properties:
            self._link_property(Property(prop_elm, self))
        self._sort_props_by_pid()

    @property
    def properties(self) -> list[Property]:
        return self._props

    def add_property(
        self,
        name: str,
        link_target: str | None = None,
    ) -> Property:
        next_pid = max(self._pids_map, default=1) + 1
        prop_elm = E_Property.new()
        prop_elm.fmtid = CUSTOM_PROPERTIES_GUID
        prop_elm.pid = next_pid
        prop_elm.name = name
        prop_elm.link_target = link_target
        prop = Property(prop_elm, self)
        self.element.append_child(prop_elm)
        self._link_property(prop)
        return prop

    def del_property(self, pid_or_name: int | str) -> None:
        if isinstance(pid_or_name, int):
            prop = self.get_property_by_pid(pid_or_name)
        else:
            prop = self.get_property_by_name(pid_or_name)
        if prop is None:
            return
        self.element.remove_child(prop.element)
        self._unlink_property(prop)

    def get_property_by_pid(self, pid: int) -> Property | None:
        return self._pids_map.get(pid)

    def get_property_by_name(self, name: str) -> Property | None:
        return self._names_map.get(name)

    def _link_property(
        self, prop: Property, link_at: int | None = None
    ) -> None:
        if link_at is not None:
            self._props.insert(link_at, prop)
        else:
            self._props.append(prop)
        self._map_property(prop)

    def _unlink_property(self, prop: Property) -> None:
        try:
            self._props.remove(prop)
        except ValueError:
            pass
        self._unmap_property(prop)

    def _map_property(self, prop: Property) -> None:
        self._pids_map[prop._pid] = prop
        self._names_map[prop._name] = prop

    def _unmap_property(self, prop: Property) -> None:
        self._pids_map.pop(prop._pid, None)
        self._names_map.pop(prop._name, None)

    def _sort_props_by_pid(self) -> None:
        self._props = sorted(self._props, key=lambda p: p.property_id)


class Property(
    DocxParentedElementProxy[
        E_Property, CustomProperties, "CustomFilePropertiesPart"
    ]
):
    def __init__(self, element: E_Property, parent: CustomProperties) -> None:
        super().__init__(element, parent)
        if element.fmtid != CUSTOM_PROPERTIES_GUID:
            raise ValueError(
                f"Custom property must be created with format id `{CUSTOM_PROPERTIES_GUID}`"
            )
        self._pid = self._validate_pid(element.pid)
        self._name = self._validate_name(element.name)
        self._link_target = element.link_target
        self._elm_value, self._value = self._validate_value(
            element.value, bool(self._link_target)
        )

    @property
    def format_id(self) -> str:
        return CUSTOM_PROPERTIES_GUID

    @property
    def property_id(self) -> int:
        return self._pid

    @property_id.setter
    def property_id(self, value: int) -> None:
        value = self._validate_pid(value)
        if value == self._pid:
            return
        parent = self.parent
        parent._unmap_property(self)
        self.element.pid = value
        self._pid = value
        parent._map_property(self)
        parent._sort_props_by_pid()

    @property
    def custom_file_property_name(self) -> str:
        return self._name

    @custom_file_property_name.setter
    def custom_file_property_name(self, value: str) -> None:
        value = self._validate_name(value)
        if value == self._name:
            return
        parent = self.parent
        parent._unmap_property(self)
        self.element.name = value
        self._name = value
        parent._map_property(self)

    @property
    def bookmark_link_target(self) -> str | None:
        return self._link_target

    # TODO: add link target as object in future
    @bookmark_link_target.setter
    def bookmark_link_target(self, value: str | None) -> None:
        self.element.link_target = value
        self._link_target = value

    @property
    def value(self) -> int | str | W3CDTFDateTime | bool | None:
        return self._value

    @value.setter
    def value(
        self, value: int | str | W3CDTFDateTime | datetime | bool | None
    ) -> None:
        if (
            not isinstance(value, (int, str, W3CDTFDateTime, datetime, bool))
            and value is not None
        ):
            raise TypeError(
                "Value must be integer, string, datetime, boolean or None!"
            )
        self._elm_value.content = value
        if isinstance(value, datetime):
            value = W3CDTFDateTime.from_datetime_python(value)
        self._value = value

    def _validate_name(self, name: str | None) -> str:
        if not name:
            raise ValueError("Custom property name cannot be empty")
        if name in self.parent._names_map:
            raise ValueError("Custom property name must be unique")
        return name

    def _validate_pid(self, pid: int) -> int:
        if pid < PID_MIN:
            raise ValueError("Custom property mut be more or equal to 2")
        if pid in self.parent._pids_map:
            raise ValueError(
                f"Custom property must be evaluated with unique property id! Got `{pid}`"
            )
        return pid

    def _validate_value(
        self, elm_value: PropertyValue, is_link_target: bool
    ) -> tuple[
        E_Lpwstr | E_Filetime | E_I4 | E_Bool,
        int | str | W3CDTFDateTime | bool | None,
    ]:
        if not isinstance(elm_value, (E_Lpwstr, E_Filetime, E_I4, E_Bool)):
            raise TypeError(
                "Value of property must contain string, datetime, integer or boolean!"
            )
        val = elm_value.content
        if not is_link_target and val is None:
            raise ValueError("Value cannot be empty for common property!")
        return elm_value, val
