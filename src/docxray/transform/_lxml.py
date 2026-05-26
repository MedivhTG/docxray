from typing import Literal

from lxml.html import HtmlElement, tostring


def to_str_html(
    doc: HtmlElement,
    *,
    pretty_print: bool = False,
    include_meta_content_type: bool = False,
    encoding: type[str] | Literal["unicode"] = "unicode",
    with_tail: bool = True,
    doctype: str | None = None,
) -> str:
    return tostring(
        doc,
        pretty_print=pretty_print,
        include_meta_content_type=include_meta_content_type,
        encoding=encoding,
        with_tail=with_tail,
        doctype=doctype,
    )
