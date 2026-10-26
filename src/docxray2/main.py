# from __future__ import annotations

# import re
# from typing import Self

# from lxml import etree

# from .xmlchemy import BaseOxmlElement, elm_ns_cls_lookup
# from .xsd.simple_type import Restriction, SimpleType
# from .xsd.st_primitives import XsdAnyUri, XsdString

# _TOKEN = r"[!#$%&'*+\-.0-9A-Z^_`a-z|~]"
# _QUOTED_CHAR = r"[\x20-\x21\x23-\x7e\x80-\xff]|\s|\\[\x00-\x7f]"
# ST_CONTENT_TYPE_PATTERN = re.compile(
#     rf"((({_TOKEN})+)/(({_TOKEN})+)"
#     rf"((\s+)*;(\s+)*"
#     rf"((({_TOKEN})+)=((({_TOKEN})+)|\"({_QUOTED_CHAR})*\"))"
#     rf")*)"
# )
# ST_EXTENSION_PATTERN = re.compile(
#     r"([!$&amp;'\(\)\*\+,:=]|(%[0-9a-fA-F][0-9a-fA-F])|[:@]|[a-zA-Z0-9\-_~])+"
# )


# class ST_ContentType(SimpleType[str]):
#     SCHEMA = Restriction(XsdString)
#     FACETS = {"pattern": ST_CONTENT_TYPE_PATTERN}


# class ST_Extension(SimpleType[str]):
#     SCHEMA = Restriction(XsdString)
#     FACETS = {"pattern": ST_EXTENSION_PATTERN}


# # -------

# CONTENT_TYPES = """
# <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
# <Default Extension="jpg" ContentType="image/jpeg"/>
# <Default Extension="png" ContentType="image/png"/>
# <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
# <Default Extension="xml" ContentType="application/xml"/>
# <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
# <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
# <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
# <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
# <Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/>
# <Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>
# <Override PartName="/word/endnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.endnotes+xml"/>
# <Override PartName="/word/diagrams/data1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
# <Override PartName="/word/diagrams/layout1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
# <Override PartName="/word/diagrams/quickStyle1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
# <Override PartName="/word/diagrams/colors1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
# <Override PartName="/word/diagrams/drawing1.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
# <Override PartName="/word/diagrams/data2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
# <Override PartName="/word/diagrams/layout2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
# <Override PartName="/word/diagrams/quickStyle2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
# <Override PartName="/word/diagrams/colors2.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
# <Override PartName="/word/diagrams/drawing2.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
# <Override PartName="/word/diagrams/data3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
# <Override PartName="/word/diagrams/layout3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
# <Override PartName="/word/diagrams/quickStyle3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
# <Override PartName="/word/diagrams/colors3.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
# <Override PartName="/word/diagrams/drawing3.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
# <Override PartName="/word/diagrams/data4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
# <Override PartName="/word/diagrams/layout4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
# <Override PartName="/word/diagrams/quickStyle4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
# <Override PartName="/word/diagrams/colors4.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
# <Override PartName="/word/diagrams/drawing4.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
# <Override PartName="/word/diagrams/data5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"/>
# <Override PartName="/word/diagrams/layout5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramLayout+xml"/>
# <Override PartName="/word/diagrams/quickStyle5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramStyle+xml"/>
# <Override PartName="/word/diagrams/colors5.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.diagramColors+xml"/>
# <Override PartName="/word/diagrams/drawing5.xml" ContentType="application/vnd.ms-office.drawingml.diagramDrawing+xml"/>
# <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
# <Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
# <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
# <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
# </Types>
# """


# opc_nslookup = elm_ns_cls_lookup()
# opc_parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
# opc_parser.set_element_class_lookup(opc_nslookup)

# OPC_NSMAP = {
#     "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
# }


# class OpcOxml(BaseOxmlElement, nslookup=opc_nslookup, nsmap=OPC_NSMAP):
#     @classmethod
#     def from_xml(cls, text: str) -> Self:
#         return cls.parse(text, opc_parser)


# class NsOxmlContentTypes(OpcOxml, ns="ct"):
#     pass


# class CT_Types(NsOxmlContentTypes):
#     @property
#     def defaults(self) -> list[E_Default]:
#         return self.zero_or_more(E_Default)

#     @property
#     def overrides(self) -> list[E_Override]:
#         return self.zero_or_more(E_Override)


# class CT_Default(NsOxmlContentTypes):
#     @property
#     def extension(self) -> str:
#         return self.attr_required("Extension", ST_Extension)

#     @property
#     def content_type(self) -> str:
#         return self.attr_required("ContentType", ST_ContentType)


# class CT_Override(NsOxmlContentTypes):
#     @property
#     def content_type(self) -> str:
#         return self.attr_required("ContentType", ST_ContentType)

#     @property
#     def part_name(self) -> str:
#         return self.attr_required("PartName", XsdAnyUri)


# class E_Types(CT_Types, tag="Types"):
#     pass


# class E_Default(CT_Default, tag="Default"):
#     pass


# class E_Override(CT_Override, tag="Override"):
#     pass


# elm = E_Types.from_xml(CONTENT_TYPES)
# f = elm.defaults[0].content_type
# w = 1


from .opc.pkg_reader import PkgReader

reader = PkgReader.from_file("tests/examples/content_check.docx")
wait = 1
