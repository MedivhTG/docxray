from pathlib import Path

from docxray import Document
from docxray.oxml.trans.proxy.table import Table
from docxray.oxml.trans.proxy.text.paragraph import Paragraph
from docxray.transform.builders import HtmlTable
from docxray.transform.ruleset import Rule, RuleSet


class TestDocument:
    def test_open(self, test_file: Path) -> None:
        doc = Document(test_file)
        assert doc is not None

    def test_iter_inner_content(self, test_file: Path) -> None:
        doc = Document(test_file)
        html = ""
        for item in doc.iter_inner_content():
            if isinstance(item, Table):
                table_html = item.transform()
                html += table_html
                w = 1
            else:
                p_html = item.transform()
                html += p_html
                w = 1
        w = 1
        html = ""
        for item in doc.iter_inner_content_with_lists():
            if isinstance(item, Table):
                ruleset = RuleSet.html_default()
                ruleset.set_html_rule(
                    "Table", Rule(HtmlTable, transform_list_views=True)
                )
                table_html = item.transform()
                html += table_html
                w = 1
            elif isinstance(item, Paragraph):
                p_html = item.transform()
                html += p_html
                w = 1
            else:
                list_html = item.transform()
                html += list_html
                w = 1
        w = 1
