from datetime import UTC, datetime, timedelta

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
core_props.last_printed = datetime.now(UTC)
core_props.modified = datetime(1601, 1, 1)
core_props.revision = "3"
core_props.subject = "DOCXRAY"
core_props.title = "Call"
core_props.version = "111"

extf_props = doc.get_or_add_extf_props()

extf_props.application_name = None
extf_props.application_version = None
extf_props.total_number_of_characters = None
extf_props.number_of_characters_with_spaces = None
extf_props.name_of_company = None
extf_props.digital_signature = None
extf_props.document_security = 1
extf_props.heading_groups = []
extf_props.number_of_hidden_slides = 5
extf_props.relative_hyperlink_base = "http://google.com"
extf_props.hyperlinks_changed = True
extf_props.number_of_lines = 10000
extf_props.links_up_to_date = None
extf_props.manager = "I'm"
extf_props.total_number_of_multimedia_clips = 5
extf_props.number_of_slides_containing_notes = 3
extf_props.total_number_of_pages = 14212
extf_props.total_number_of_paragraphs = 1
extf_props.intended_format_of_presentation = "Video"
extf_props.thumbnail_display_mode = True
extf_props.shared_document = True
extf_props.slides_metadata = None
extf_props.name_of_document_template = "Normal"
extf_props.total_edit_time_metadata = 2
extf_props.word_count = 0

doc.save(out)

wait = 1
