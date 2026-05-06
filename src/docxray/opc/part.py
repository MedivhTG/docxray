"""Open Packaging Convention (OPC) objects related to package parts."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Callable, Generic, Self, Type, TypeVar

# docxray stuff
from docxray.opc.packuri import PackURI
from docxray.opc.rel import Relationships, _Relationship
from docxray.opc.shared import cls_method_fn
from docxray.oxml.transitional.parser import parse_xml
from docxray.oxml.transitional.xmlchemy import OxmlElement
from docxray.types import ELM_T

if TYPE_CHECKING:
    # docxray stuff
    from docxray.opc.package import OpcPackage


PART_T = TypeVar("PART_T", bound="Part")


class Part:
    """Base class for package parts.

    Provides common properties and methods, but intended to be subclassed in client code
    to implement specific part behaviors.
    """

    def __init__(
        self,
        partname: PackURI,
        content_type: str,
        blob: bytes | None = None,
        package: OpcPackage | None = None,
    ) -> None:
        self._partname = partname
        self._content_type = content_type
        self._blob = blob
        self._package = package

    def after_unmarshal(self) -> None:
        """Entry point for post-unmarshaling processing, for example to parse the part
        XML.

        May be overridden by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    def before_marshal(self) -> None:
        """Entry point for pre-serialization processing, for example to finalize part
        naming if necessary.

        May be overridden by subclasses without forwarding call to super.
        """
        # don't place any code here, just catch call if not overridden by
        # subclass
        pass

    @property
    def blob(self) -> bytes:
        """Contents of this package part as a sequence of bytes.

        May be text or binary. Intended to be overridden by subclasses. Default behavior
        is to return load blob.
        """
        return self._blob or b""

    @property
    def content_type(self) -> str:
        """Content type of this part."""
        return self._content_type

    @classmethod
    def load(
        cls,
        partname: PackURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Self:
        return cls(partname, content_type, blob, package)

    def load_rel(
        self,
        reltype: str,
        target: Part | str,
        rId: str,
        is_external: bool = False,
    ) -> _Relationship:
        """Return newly added |_Relationship| instance of `reltype`.

        The new relationship relates the `target` part to this part with key `rId`.

        Target mode is set to ``RTM.EXTERNAL`` if `is_external` is |True|. Intended for
        use during load from a serialized package, where the rId is well-known. Other
        methods exist for adding a new relationship to a part when manipulating a part.
        """
        return self.rels.add_relationship(reltype, target, rId, is_external)

    @property
    def package(self) -> OpcPackage | None:
        """|OpcPackage| instance this part belongs to."""
        return self._package

    @property
    def partname(self) -> PackURI:
        """|PackURI| instance holding partname of this part, e.g.
        '/ppt/slides/slide1.xml'."""
        return self._partname

    def part_related_by(
        self, reltype: str, assert_part: type[PART_T]
    ) -> PART_T:
        """Return part to which this part has a relationship of `reltype`.

        Raises |KeyError| if no such relationship is found and |ValueError| if more than
        one such relationship is found. Provides ability to resolve implicitly related
        part, such as Slide -> SlideLayout.
        """
        target_part = self.rels.part_with_reltype(reltype)
        assert isinstance(target_part, assert_part)
        return target_part

    @property
    def related_parts(self) -> dict[str, Part | str]:
        """Dictionary mapping related parts by rId, so child objects can resolve
        explicit relationships present in the part XML, e.g. sldIdLst to a specific
        |Slide| instance."""
        return self.rels.related_parts

    @cached_property
    def rels(self) -> Relationships:
        """|Relationships| instance holding the relationships for this part."""
        # -- prevent breakage in `python-docx-template` by retaining legacy `._rels` attribute --
        self._rels = Relationships(self._partname.baseURI)
        return self._rels

    def target_ref(self, rId: str) -> str:
        """Return URL contained in target ref of relationship identified by `rId`."""
        rel = self.rels[rId]
        return rel.target_ref


class PartFactory:
    """Provides a way for client code to specify a subclass of |Part| to be constructed
    by |Unmarshaller| based on its content type and/or a custom callable."""

    part_class_selector: Callable[[str, str], Type[Part] | None] | None = None
    part_type_for: dict[str, Type[Part]] = {}
    default_part_type = Part

    @classmethod
    def create_part(
        cls,
        partname: PackURI,
        content_type: str,
        reltype: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Part:
        PartClass: Type[Part] | None = None
        if cls.part_class_selector is not None:
            part_class_selector = cls_method_fn(cls, "part_class_selector")
            PartClass = part_class_selector(content_type, reltype)
        if PartClass is None:
            PartClass = cls._part_cls_for(content_type)
        return PartClass.load(partname, content_type, blob, package)

    @classmethod
    def _part_cls_for(cls, content_type: str) -> type[Part]:
        """Return the custom part class registered for `content_type`, or the default
        part class if no custom class is registered for `content_type`."""
        if content_type in cls.part_type_for:
            return cls.part_type_for[content_type]
        return cls.default_part_type


class XmlPart(Part, Generic[ELM_T]):
    """Base class for package parts containing an XML payload, which is most of them.

    Provides additional methods to the |Part| base class that take care of parsing and
    reserializing the XML payload and managing relationships to other parts.
    """

    def __init__(
        self,
        partname: PackURI,
        content_type: str,
        element: ELM_T,
        package: OpcPackage,
    ) -> None:
        super().__init__(partname, content_type, package=package)
        self._element = element

    @property
    def element(self) -> ELM_T:
        """The root XML element of this XML part."""
        return self._element

    @classmethod
    def load(
        cls,
        partname: PackURI,
        content_type: str,
        blob: bytes,
        package: OpcPackage,
    ) -> Self:
        element = parse_xml(blob, OxmlElement)
        return cls(
            partname,
            content_type,
            element,  # type: ignore[arg-type]
            package,
        )

    @property
    def part(self) -> Self:
        return self
