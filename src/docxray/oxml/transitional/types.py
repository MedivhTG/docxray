from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .xmlchemy import OxmlElement

ELM_T = TypeVar("ELM_T", bound="OxmlElement")
