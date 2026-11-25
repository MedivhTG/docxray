from datetime import UTC, datetime, timedelta

# docxray stuff
from docxray2 import Document
from docxray2.proxy.enums import WD_CUSTOM_PROPERTY_TYPE
from docxray2.proxy.extf_props import HeadingGroup

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
extf_props.heading_groups = [HeadingGroup(name="Headers", titles=["Название"])]
extf_props.number_of_hidden_slides = 5
extf_props.hyperlink_list = None
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

custom_props = doc.get_or_add_custom_props()

# ---------- ЧТЕНИЕ ----------

# 1. В документе ровно 7 свойств
assert len(custom_props.properties) == 7

# 2. Порядок отсортирован по pid: 2..8
assert [p.property_id for p in custom_props.properties] == [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
]

# 3. Чтение по имени: разные типы приходят «своими» типами
prop = custom_props.get_property_by_name("Группа")
assert prop is not None
assert prop.value == "Номер 1"

prop = custom_props.get_property_by_pid(6)
assert prop is not None
assert prop.value == 5

prop = custom_props.get_property_by_name("Отпечатано")
assert prop is not None
assert prop.value is True

prop = custom_props.get_property_by_name("Проверено")
assert prop is not None
assert prop.value is False

# 4. Дата спарсена в W3CDTFDateTime, а не в строку
prop = custom_props.get_property_by_name("Дата записи")
assert prop is not None
assert prop.value_type == WD_CUSTOM_PROPERTY_TYPE.DATE

# 5. Свойства с linkTarget: значение None, но сам linkTarget доступен
link_prop = custom_props.get_property_by_name("Ссылка")
assert link_prop is not None
assert link_prop.bookmark_link_target == "Бином_Ньютона"

question_prop = custom_props.get_property_by_name("Вопрос")
assert question_prop is not None
assert question_prop.bookmark_link_target == "_Таблица"
assert (
    question_prop.value is None
)  # связанное свойство с пустым <vt:lpwstr/> — валидно

# 6. Unicode-значение "Ссылка" прочиталось без искажений
assert link_prop.value == "**𝑥+𝑎**𝑛*=*𝑘=0*𝑛***𝑛*𝑘***𝑥*𝑘**𝑎*𝑛−𝑘**"

# ---------- СОЗДАНИЕ ----------

# 7. Новый pid = max + 1 = 9
singer = custom_props.add_property("Singer", "My name is Slim Shady")
assert singer.property_id == 9

# 8. Типы значений подбираются автоматически
assert (
    custom_props.add_property("Число", 42).value_type
    == WD_CUSTOM_PROPERTY_TYPE.NUMBER
)
assert (
    custom_props.add_property("Флаг", True).value_type
    == WD_CUSTOM_PROPERTY_TYPE.BOOLEAN
)
assert (
    custom_props.add_property(
        "Момент", datetime(2026, 1, 1, tzinfo=UTC)
    ).value_type
    == WD_CUSTOM_PROPERTY_TYPE.DATE
)

try:
    custom_props.add_property("Пустышка", None)
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# 9. Дубликат имени — ошибка
try:
    custom_props.add_property("Группа", "Номер 2")
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# 10. Пустое имя — ошибка
try:
    custom_props.add_property("", "значение")
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# ---------- ИЗМЕНЕНИЕ ----------

# 11. Смена значения: смена типа (NUMBER -> TEXT) проходит без ручной замены элемента
client = custom_props.get_property_by_name("Клиент")
assert client is not None
client.value = "не число"
assert client.value == "не число"
assert client.value_type == WD_CUSTOM_PROPERTY_TYPE.TEXT

# 12. Смена имени: старого больше нет, новое на месте
client.custom_file_property_name = "Заказчик"
assert custom_props.get_property_by_name("Клиент") is None
assert custom_props.get_property_by_name("Заказчик") is client

# 13. Смена pid: конфликт с существующим — ошибка
try:
    singer.property_id = 2
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# 14. Свободный pid принимается и список пересортировался
next_free_pid = max(p.property_id for p in custom_props.properties) + 1
singer.property_id = next_free_pid
assert [p.property_id for p in custom_props.properties] == sorted(
    p.property_id for p in custom_props.properties
)

# 15. Значение для связанного свойства — нельзя
try:
    question_prop.value = "текст"
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# 16. pid < 2 — ошибка
try:
    singer.property_id = 1
    assert False, "должен был подняться ValueError"
except ValueError:
    pass

# ---------- УДАЛЕНИЕ ----------

# 17. Удаление по имени
custom_props.del_property("Singer")
assert custom_props.get_property_by_name("Singer") is None

# 18. Удаление по pid
custom_props.del_property(6)
assert custom_props.get_property_by_pid(6) is None

# 19. Удаление несуществующего — молча, без исключения
custom_props.del_property("Такого нет")  # не должно упасть
custom_props.del_property(999)

# 20. Итог: 7 исходных + 4 добавленных - 2 удалённых
assert len(custom_props.properties) == 9

# 21. Итог: состав после всех манипуляций
remaining = {p.custom_file_property_name for p in custom_props.properties}
assert remaining == {
    "Ссылка",
    "Вопрос",
    "Группа",
    "Дата записи",
    "Отпечатано",
    "Проверено",
    "Число",
    "Флаг",
    "Момент",
}

doc.save(out)

wait = 1
