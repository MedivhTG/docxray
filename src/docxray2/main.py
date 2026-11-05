# docxray stuff
from docxray2 import Document

doc = Document("tests/examples/content_check.docx")
doc.core_props.category = "GOODS"
doc.save("here.docx")
wait = 1
