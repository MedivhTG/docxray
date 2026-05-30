from pathlib import Path

from docxray import Document
from docxray.oxml.trans.proxy.drawing import Drawing
from docxray.oxml.trans.proxy.shared import Length
from docxray.oxml.trans.proxy.table import Table
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.oxml.trans.proxy.text.run import Run
from docxray.transform.builders import HtmlTable
from docxray.transform.ruleset import Rule, RuleSet


class TestDocument:
    def test_open(self, test_file: Path) -> None:
        doc = Document(test_file)
        assert doc is not None

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = Document(test_file)
        for item in doc.iter_inner_content():
            if isinstance(item, Table):
                table_html = item.transform()
                w = 1
            else:
                p_html = item.transform()
                w = 1

        for p_or_t in doc.iter_inner_content_with_lists():
            if isinstance(p_or_t, Table):
                ruleset = RuleSet.html_default()
                ruleset.set_html_rule(
                    "Table", Rule(HtmlTable, transform_list_views=True)
                )
                table_html = p_or_t.transform(ruleset)
                w = 1
            elif isinstance(p_or_t, Paragraph):
                p_html = p_or_t.transform()
                w = 1
            else:
                list_html = p_or_t.transform()
                w = 1
