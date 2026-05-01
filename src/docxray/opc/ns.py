# docxray stuff
from docxray.opc.constants import NAMESPACE as NS

nsmap = {
    "ct": NS.OPC_CONTENT_TYPES,
    "pr": NS.OPC_RELATIONSHIPS,
    "r": NS.OFC_RELATIONSHIPS,
}


def qn(tag: str) -> str:
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{%s}%s" % (uri, tagroot)


class CT:
    DEFAULT = qn("ct:Default")
    OVERRIDE = qn("ct:Override")


class PR:
    RELATIONSHIP = qn("pr:Relationship")
