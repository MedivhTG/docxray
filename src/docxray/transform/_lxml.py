import re
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
    raw_ampersant: bool = True,
    resolve_html_entities: bool = True,
) -> str:
    parsed = tostring(
        doc,
        pretty_print=pretty_print,
        include_meta_content_type=include_meta_content_type,
        encoding=encoding,
        with_tail=with_tail,
        doctype=doctype,
    )
    if raw_ampersant:
        parsed = parsed.replace("&amp;", "&")
    if resolve_html_entities:
        parsed = encode_html_entities(parsed)
    return parsed


PYCODE_TO_HTML5_ENTITY = {"\xa0": "nbsp"}
HTML_ENTITY_PATTERN = re.compile(
    "|".join(re.escape(c) for c in PYCODE_TO_HTML5_ENTITY.keys())
)


def encode_html_entities(text: str) -> str:
    return HTML_ENTITY_PATTERN.sub(
        lambda m: f"&{PYCODE_TO_HTML5_ENTITY[m.group(0)]};", text
    )
