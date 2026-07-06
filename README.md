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
for item in doc.iter_inner_content():
    # Process paragraphs, tables, runs, etc.
    pass
```

---

## 📦 Installation

```bash
pip install docxray
```

### Additional Dependencies

**ImageMagick** is required for full image processing support when using the **Wand** library. Without ImageMagick, Docxray will fall back to using **Pillow** for image handling.

- **For Wand (recommended for advanced formats like WMF/EMF):**
  - **macOS:** `brew install imagemagick`
  - **Ubuntu/Debian:** `sudo apt-get install imagemagick libmagickwand-dev`
  - **Windows:** Download and install from [ImageMagick official site](https://imagemagick.org/script/download.php) (ensure the development headers are included)


> **Note:** If both Wand and ImageMagick are available, Docxray will use them for superior format support. If ImageMagick is missing, the library automatically falls back to Pillow for basic image operations.

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
for item in doc.iter_inner_content():
    if isinstance(item, Paragraph):
        for p_item in item.iter_inner_content():
            if isinstance(p_item, Run) and p_item.italic:
                print(f"Italic text: {p_item.raw_text}")
```

---

## 📄 License

MIT — free for personal and commercial use.

---

## 🙏 Acknowledgements

Built as a fork of the excellent [`python-docx`](https://github.com/python-openxml/python-docx) project, extended for deeper ECMA-376 compliance and analysis capabilities.