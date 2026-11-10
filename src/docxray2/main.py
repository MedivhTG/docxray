from datetime import datetime

# docxray stuff
from docxray2 import Document

doc = Document("tests/examples/content_check.docx")
core_props = doc.core_props
core_props.category = "GOODS"
core_props.content_status = "Alpha"
core_props.created = datetime.now()
doc.save("here.docx")
wait = 1
