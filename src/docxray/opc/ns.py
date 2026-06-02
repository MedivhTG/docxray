"""OPC namespaces with qualifiend names."""

from .constants import NAMESPACE as NS

nsmap = {
    "ct": NS.OPC_CONTENT_TYPES,
    "pr": NS.OPC_RELATIONSHIPS,
    "r": NS.OFC_RELATIONSHIPS,
}


def qn(tag: str) -> str:
    """Get tag name in clark-notation, e.g. qualifiend name in XML.

    **Example**:
    ```python
       p_name = qn("w:p")
       print(p_name) # will print `{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p`
    ```

    Args:
        tag (str): XML tag with namespace char.

    Returns:
        str: Qualified name string.
    """
    prefix, tagroot = tag.split(":")
    uri = nsmap[prefix]
    return "{%s}%s" % (uri, tagroot)


class CT:
    """Constants with qualified names for namespace `http://schemas.openxmlformats.org/package/2006/content-types`"""

    DEFAULT = qn("ct:Default")
    OVERRIDE = qn("ct:Override")


class PR:
    """Constants with qualified names for namespace `http://schemas.openxmlformats.org/package/2006/relationships`"""

    RELATIONSHIP = qn("pr:Relationship")
