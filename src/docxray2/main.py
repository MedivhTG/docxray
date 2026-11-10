from datetime import datetime

# docxray stuff
from docxray2 import Document

doc = Document("tests/examples/content_check.docx")
core_props = doc.core_props
core_props.category = "Parsed"
core_props.content_status = "Alpha"
core_props.created = datetime.now()
core_props.creator = "docxray"
core_props.description = "Created by docxray"
core_props.keywords = "Content, documents, docxray"
doc.save("here.docx")
wait = 1
