from datetime import datetime, timedelta

# docxray stuff
from docxray2 import Document

origin = "tests/examples/content_check.docx"
out = "here.docx"

doc = Document(origin)
core_props = doc.get_or_add_core_props()
core_props.category = "Parsed"
core_props.content_status = "Alpha"
core_props.created = datetime.now() - timedelta(days=1)
core_props.creator = "docxray"
core_props.description = "Created by docxray"
core_props.keywords = "Content, documents, docxray"
core_props.language = "ru-RU"
core_props.last_modified_by = "docxray"
core_props.last_printed = datetime.now()
core_props.modified = datetime.now()
core_props.revision = "3"
core_props.subject = "DOCXRAY"
core_props.title = "Call"
core_props.version = "111"

doc.save(out)
wait = 1
