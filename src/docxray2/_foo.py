from typing import Self

from lxml import etree

CONTENT_TYPES = """
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/>
<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>
<Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/>
<Override PartName="/word/diagrams/data1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
<Override PartName="/word/diagrams/layout1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
<Override PartName="/word/diagrams/quickStyle1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
<Override PartName="/word/diagrams/colors1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
<Override PartName="/word/diagrams/drawing1.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
<Override PartName="/word/diagrams/data2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
<Override PartName="/word/diagrams/layout2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
<Override PartName="/word/diagrams/quickStyle2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
<Override PartName="/word/diagrams/colors2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
<Override PartName="/word/diagrams/drawing2.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
<Override PartName="/word/diagrams/data3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
<Override PartName="/word/diagrams/layout3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
<Override PartName="/word/diagrams/quickStyle3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
<Override PartName="/word/diagrams/colors3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
<Override PartName="/word/diagrams/drawing3.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
<Override PartName="/word/diagrams/data4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
<Override PartName="/word/diagrams/layout4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
<Override PartName="/word/diagrams/quickStyle4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
<Override PartName="/word/diagrams/colors4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
<Override PartName="/word/diagrams/drawing4.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
<Override PartName="/word/diagrams/data5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
<Override PartName="/word/diagrams/layout5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
<Override PartName="/word/diagrams/quickStyle5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
<Override PartName="/word/diagrams/colors5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
<Override PartName="/word/diagrams/drawing5.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
<Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
<Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


def elm_ns_cls_lookup(
    fallback_cls: type[etree.ElementBase] = etree.ElementBase,
) -> etree.ElementNamespaceClassLookup:
    lookup: etree.ElementNamespaceClassLookup = (
        etree.ElementNamespaceClassLookup()
    )
    fallback = etree.ElementDefaultClassLookup(element=fallback_cls)
    lookup.set_fallback(fallback)
    return lookup


class Element(etree.ElementBase):
    _tag: str | None = None
    _ns: str | None = None
    _nsmap: dict[str, str] = {}
    _lookup: etree.ElementNamespaceClassLookup | None = None
    _qname: etree.QName | None = None

    @classmethod
    def qname(cls) -> etree.QName:
        if not cls._qname:
            raise ValueError("No qualified name provided")
        return cls._qname

    def __init_subclass__(
        cls,
        tag: str | None = None,
        ns: str | None = None,
        nsmap: dict[str, str] | None = None,
        lookup: etree.ElementNamespaceClassLookup | None = None,
    ) -> None:
        if tag:
            cls._tag = tag
            cls.TAG = tag
        if ns:
            cls._ns = ns
            cls.NAMESPACE = ns
        if nsmap:
            cls._nsmap = nsmap
        if lookup:
            cls._lookup = lookup
        cls.register_elm()
        return super().__init_subclass__()

    @classmethod
    def register_elm(cls) -> None:
        if not (cls._ns and cls._nsmap and cls._lookup and cls._tag):
            return
        uri = cls._nsmap[cls._ns]
        ns = cls._lookup.get_namespace(uri)
        ns[cls._tag] = cls
        cls._qname = etree.QName(uri, cls._tag)

    @classmethod
    def parse(cls, text, parser: etree.XMLParser):
        return etree.fromstring(text, parser)


opc_parser = etree.XMLParser()
opc_lookup = elm_ns_cls_lookup(Element)
opc_parser.set_element_class_lookup(opc_lookup)
OPC_NSMAP = {
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}


class OpcElement(Element, nsmap=OPC_NSMAP, lookup=opc_lookup):
    @classmethod
    def from_xml(cls, text) -> Self:
        return cls.parse(text, opc_parser)  # type: ignore


class NS_ContentTypes(OpcElement, ns="ct"):
    pass


class CT_Types(NS_ContentTypes):
    @property
    def defaults(self):
        return self.findall(E_Default.qname(), self._nsmap)


class CT_Default(NS_ContentTypes):
    pass


class CT_Override(NS_ContentTypes):
    pass


class E_Types(CT_Types, tag="Types"):
    pass


class E_Default(CT_Default, tag="Default"):
    pass


class E_Override(CT_Override, tag="Override"):
    pass


types_elm = E_Types.from_xml(CONTENT_TYPES)
dflts_lst = types_elm.defaults
w = 1
