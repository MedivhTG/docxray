# Docxray

**A sophisticated DOCX analysis library** — fork of `python-docx` with advanced parsing, styling intelligence, and deep ECMA-376 compliance.

> Built for reading, inspecting, and transforming `.docx` (OOXML Transitional) documents with precision.

---

## ✨ Key Features

- 🧠 **Smart property resolution** – inherits formatting from style hierarchies, following ECMA-376 rules (not just raw XML values)
- 🖼️ **Rich image support** – works with **Pillow** or **Wand (ImageMagick)**; handles modern formats plus legacy **WMF/EMF**
- 🔄 **HTML transformation** – proxy objects (`Paragraph`, `Table`, etc.) include methods to convert content to HTML with rendering options
- ✅ **XSD soft validation** – validates simple types against the official schema
- 🔢 **Intelligent list handling** – numeral module correctly restores list-item text for most common cases

---

## 🚀 Quick Start

```python
from docxray import Document

doc = Document("path/to/your/document.docx")

# Iterate through all inner content
for element in doc.iter_inner_content():
    # Process paragraphs, tables, runs, etc.
    pass
```

---

## 📦 Installation

```bash
pip install docxray
```

*Optional dependencies:*
- `Pillow` – for standard image formats
- `Wand` – for extended formats (including WMF/EMF)

---

## 📖 Documentation

Docxray is designed for **read‑only** document analysis. It provides:

- Full access to document structure (paragraphs, runs, tables, images)
- Styling attributes resolved through the complete OOXML style inheritance chain
- Convenient proxies for manipulating content before export (e.g., to HTML)
- Validation utilities to check document conformance

---

## 🧪 Example: Inspecting Run Properties

```python
for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        # Resolves inherited italic/bold/etc. from styles
        if run.italic:
            print(f"Italic text: {run.raw_text}")
```

---

## 📄 License

MIT — free for personal and commercial use.

---

## 🙏 Acknowledgements

Built as a fork of the excellent [`python-docx`](https://github.com/python-openxml/python-docx) project, extended for deeper ECMA-376 compliance and analysis capabilities.