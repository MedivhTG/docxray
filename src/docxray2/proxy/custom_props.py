from __future__ import annotations

from typing import TYPE_CHECKING

# docxray stuff
from docxray2.oxml.shared_dpc import E_Properties, E_Property
from docxray2.parts.types import ProvidesDocxXmlPart

from .base import DocxElementProxy, DocxParentedElementProxy

if TYPE_CHECKING:
    # docxray stuff
    from docxray2.parts.custom_file_properties import (  # noqa: F401
        CustomFilePropertiesPart,
    )

CUSTOM_PROPERTIES_GUID = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}"


# TODO: add link target as object in future + other features (add, del)


class CustomProperties(
    DocxElementProxy[E_Properties, "CustomFilePropertiesPart"]
):
    def __init__(
        self, element: E_Properties, parent: ProvidesDocxXmlPart
    ) -> None:
        super().__init__(element, parent)
        self._props: list[Property] | None = None
        self._pids_map: dict[int, Property] = {}
        self._names_map: dict[str, Property] = {}

    def get_properties(self) -> list[Property]:
        if self._props is not None:
            return self._props
        self._props = []
        for prop_elm in self.element.properties:
            self._link_property(Property(prop_elm, self))
        return self._props

    # def add_property(
    #     self,
    #     name: str,
    #     link_target: str | None = None,
    #     insert_index: int | None = None,
    # ) -> None:
    #     if not name:
    #         raise ValueError("Custom property name cannot be empty")
    #     if name in self._names_map:
    #         raise ValueError("Custom property name must be unique")
    #     next_pid = max(self._pids_map, default=1) + 1
    #     prop_elm = E_Property.new()
    #     prop_elm.fmtid = CUSTOM_PROPERTIES_GUID
    #     prop_elm.pid = next_pid
    #     prop_elm.name = name
    #     if link_target:
    #         prop_elm.link_target = link_target
    #     prop = Property(
    #         custom_file_property_name=name,
    #         property_id=next_pid,
    #         bookmark_link_target=link_target,
    #     )
    #     if insert_index is not None:
    #         self.element.insert_child(insert_index, prop_elm)
    #     else:
    #         self.element.append_child(prop_elm)
    #     self._link_property(prop)

    def _link_property(self, prop: Property) -> None:
        self._pids_map[prop.property_id] = prop
        self._names_map[prop.custom_file_property_name] = prop
        if not isinstance(self._props, list):
            raise TypeError("Properties instantiated wrong")
        self._props.append(prop)


# TODO: add setters
class Property(
    DocxParentedElementProxy[
        E_Property, CustomProperties, "CustomFilePropertiesPart"
    ]
):
    def __init__(self, element: E_Property, parent: CustomProperties) -> None:
        if element.fmtid != CUSTOM_PROPERTIES_GUID:
            raise ValueError(
                f"Custom property must be created with format id `{CUSTOM_PROPERTIES_GUID}`"
            )
        pid = element.pid
        if pid in parent._pids_map:
            raise ValueError(
                f"Custom property must be evaluated with unique property id! Got `{pid}`"
            )
        name = element.name
        if not name:
            raise ValueError("Custom property name cannot be empty")
        if name in parent._names_map:
            raise ValueError("Custom property name must be unique")
        self._pid = pid
        self._name = name
        self._link_target = element.link_target
        super().__init__(element, parent)

    @property
    def format_id(self) -> str:
        return CUSTOM_PROPERTIES_GUID

    @property
    def property_id(self) -> int:
        return self._pid

    @property
    def custom_file_property_name(self) -> str:
        return self._name

    @property
    def bookmark_link_target(self) -> str | None:
        return self._link_target
