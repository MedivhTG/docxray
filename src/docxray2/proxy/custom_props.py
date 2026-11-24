from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_dpc import E_Properties, E_Property, PropertyValue
from docxray2.oxml.shared_dpvt import E_I4, E_Bool, E_Filetime, E_Lpwstr
from docxray2.parts.types import ProvidesDocxXmlPart
from docxray2.xsd.w3cdtf import W3CDTFDateTime

from .base import DocxElementProxy, DocxParentedElementProxy
from .enums import WD_CUSTOM_PROPERTY_TYPE

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
    """Custom file properties of a WordprocessingML package.

    Root ``op:Properties`` element (ECMA-376 Part 1, §22.3.2.1). Each child
    ``op:property`` is a name/value pair uniquely identified by ``name`` and
    linked to an OLE property via ``fmtid``/``pid`` (§22.3.2.2).

    Maintains PID and name indexes for O(1) lookup; ``properties`` is ordered
    ascending by ``property_id``.
    """

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
        """All custom properties, ascending by ``property_id``.

        Returns:
            list[Property]: Live list view; mutate via :meth:`add_property` / :meth:`del_property`,
                not directly.
        """
        return self._props

    def add_property(
        self,
        name: str,
        value: int | str | W3CDTFDateTime | datetime | bool | None,
        link_target: str | None = None,
    ) -> Property:
        """Create and append a new custom property.

        ``pid`` is assigned as ``max(existing_pids) + 1`` (or ``2`` if empty).
        ``fmtid`` is always ``CUSTOM_PROPERTIES_GUID``.

        Args:
            name (str): Unique, non-empty property name.
            value (int | str | W3CDTFDateTime | datetime | bool | None):
                Property value; ``datetime`` is converted to W3CDTF.
                ``None`` is allowed only with ``link_target``.
            link_target (str | None): Bookmark name. When set, the value
                element is a cache per ECMA-376 §22.3.2.2 and must be ``None``.

        Returns:
            Property: The newly created property.

        Raises:
            ValueError: On empty/duplicate name, PID assignment failure, or
                ``None`` value for an unlinked property.
            TypeError: On unsupported value type.
        """
        next_pid = max(self._pids_map, default=1) + 1
        prop_elm = E_Property.new()
        prop_elm.fmtid = CUSTOM_PROPERTIES_GUID
        prop_elm.pid = next_pid
        prop_elm.name = name
        prop_elm.link_target = link_target
        value_elm = self._prop_value_elm_by_type(value)
        value_elm.content = value
        prop_elm.append_child(value_elm)
        prop = Property(prop_elm, self)
        self.element.append_child(prop_elm)
        self._link_property(prop)
        return prop

    def del_property(self, pid_or_name: int | str) -> None:
        """Remove a property by PID or name; no-op if not found.

        Args:
            pid_or_name (int | str): ``pid`` (``int``) or ``name`` (``str``).
        """
        if isinstance(pid_or_name, int):
            prop = self.get_property_by_pid(pid_or_name)
        else:
            prop = self.get_property_by_name(pid_or_name)
        if prop is None:
            return
        self.element.remove_child(prop.element)
        self._unlink_property(prop)

    def get_property_by_pid(self, pid: int) -> Property | None:
        """Return property with ``pid``, or ``None``.

        Args:
            pid (int): Property ID.

        Returns:
            Property | None: Matching property, if any.
        """
        return self._pids_map.get(pid)

    def get_property_by_name(self, name: str) -> Property | None:
        """Return property with ``name``, or ``None``.

        Args:
            name (str): Property name.

        Returns:
            Property | None: Matching property, if any.
        """
        return self._names_map.get(name)

    def _link_property(self, prop: Property) -> None:
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

    def _prop_value_elm_by_type(
        self,
        value: (
            int
            | str
            | W3CDTFDateTime
            | datetime
            | bool
            | None
            | WD_CUSTOM_PROPERTY_TYPE
        ),
    ) -> E_I4 | E_Bool | E_Lpwstr | E_Filetime:
        if isinstance(value, WD_CUSTOM_PROPERTY_TYPE):
            value_type = value
        else:
            value_type = WD_CUSTOM_PROPERTY_TYPE.new(value)
        match value_type:
            case WD_CUSTOM_PROPERTY_TYPE.NUMBER:
                return E_I4.new()
            case WD_CUSTOM_PROPERTY_TYPE.BOOLEAN:
                return E_Bool.new()
            case WD_CUSTOM_PROPERTY_TYPE.TEXT:
                return E_Lpwstr.new()
            case WD_CUSTOM_PROPERTY_TYPE.DATE:
                return E_Filetime.new()
            case WD_CUSTOM_PROPERTY_TYPE.NULL:
                return E_Lpwstr.new()
            case _:
                raise ValueError(f"Unknown value type {value_type}")


class Property(
    DocxParentedElementProxy[
        E_Property, CustomProperties, "CustomFilePropertiesPart"
    ]
):
    """Single custom file property (``op:property``, ECMA-376 §22.3.2.2).

    Invariants:
      - ``fmtid`` equals ``CUSTOM_PROPERTIES_GUID``.
      - ``pid`` >= 2, unique in parent.
      - ``name`` unique in parent.
      - If ``linkTarget`` present, the value element is a cache and the
        object-model value is ``None``; otherwise the value is non-``None``.
    """

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
            element.value, self._link_target is not None
        )

    @property
    def format_id(self) -> str:
        """OLE format ID; always ``CUSTOM_PROPERTIES_GUID``.

        Returns:
            str: The fixed custom-properties GUID.
        """
        return CUSTOM_PROPERTIES_GUID

    @property
    def property_id(self) -> int:
        """OLE property ID (``pid``), unique in the collection.

        Returns:
            int: The property ID.
        """
        return self._pid

    @property_id.setter
    def property_id(self, value: int) -> None:
        if value == self._pid:
            return
        value = self._validate_pid(value)
        parent = self.parent
        parent._unmap_property(self)
        self.element.pid = value
        self._pid = value
        parent._map_property(self)
        parent._sort_props_by_pid()

    @property
    def custom_file_property_name(self) -> str:
        """Property name (``name`` attribute), unique in the collection.

        Returns:
            str: The property name.
        """
        return self._name

    @custom_file_property_name.setter
    def custom_file_property_name(self, value: str) -> None:
        if value == self._name:
            return
        value = self._validate_name(value)
        parent = self.parent
        parent._unmap_property(self)
        self.element.name = value
        self._name = value
        parent._map_property(self)

    # TODO: add link target as object in future + setter?
    @property
    def bookmark_link_target(self) -> str | None:
        return self._link_target

    @property
    def value(self) -> int | str | W3CDTFDateTime | bool | None:
        """Cached value in Python form.

        ``None`` for linked properties, and (by construction) never ``None``
        for unlinked ones.

        Returns:
            int | str | W3CDTFDateTime | bool | None: The value.
        """
        return self._value

    @value.setter
    def value(
        self, value: int | str | W3CDTFDateTime | datetime | bool | None
    ) -> None:
        if value is not None and self._link_target is not None:
            raise ValueError(
                "For property with link_target value must be None!"
            )
        if isinstance(value, datetime):
            value = W3CDTFDateTime.from_datetime_python(value)
        old_value_type = WD_CUSTOM_PROPERTY_TYPE.new(self._value)
        new_value_type = WD_CUSTOM_PROPERTY_TYPE.new(value)
        if old_value_type != new_value_type:
            self.element.remove_child(self._elm_value)
            self._elm_value = self.parent._prop_value_elm_by_type(value)
            self.element.append_child(self._elm_value)
        self._elm_value.content = value
        self._value = value

    @property
    def value_type(self) -> WD_CUSTOM_PROPERTY_TYPE:
        """Variant type of the current value.

        Derived from ``_value``, so consistent with the setter. ``NULL``
        when ``value is None`` (linked properties).

        Returns:
            WD_CUSTOM_PROPERTY_TYPE: The variant type.
        """
        return WD_CUSTOM_PROPERTY_TYPE.new(self._value)

    def _validate_name(self, name: str | None) -> str:
        if name is not None and not isinstance(name, str):
            raise TypeError("Name must be string or None")
        if not name:
            raise ValueError("Custom property name cannot be empty")
        if name in self.parent._names_map:
            raise ValueError("Custom property name must be unique")
        return name

    def _validate_pid(self, pid: int) -> int:
        if isinstance(pid, bool) or not isinstance(pid, int):
            raise TypeError("Pid must be int")
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
