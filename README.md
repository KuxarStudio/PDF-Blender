# PDF-Blender

**Offline PDF toolkit for Windows: merge, split, protect, unprotect, convert to Word and compare PDFs without uploading anything.**

PDF-Blender is a desktop app (Python + Tkinter) built for finance and corporate teams that handle sensitive documents such as invoices, contracts and reports. Every operation runs on your own machine: no cloud service, no account, no file ever leaves your computer.

Made by [Kuxar Studio](https://kuxarstudio.com/en/tools/) · Spanish version: [kuxarstudio.com/herramientas](https://kuxarstudio.com/herramientas/)

## Features

| Tool | What it does |
|---|---|
| Merge PDFs | Combine several PDFs into one, in the order you choose. |
| Split PDF | Extract a page range from a large document into a new file. |
| Convert to Word (.docx) | Turn a PDF into an editable Word file, keeping the layout as far as possible. |
| Remove restrictions | Remove owner-password restrictions (copy, edit, print) from PDFs you are entitled to modify. |
| Protect | Encrypt a PDF with a user password. |
| Compare texts | Compare two versions of a document and get an interactive side-by-side HTML report of additions and deletions. |

## Why offline?

- **Nothing is uploaded.** Documents are processed locally, so there is nothing to leak to a third-party server.
- **Simple interface.** Designed for people who do not code.
- **Standalone.** It can be compiled into a single `.exe`, so end users need no Python installation.

## Quick start

### End users (no coding)

1. Open the **Releases** section of this repository.
2. Download the latest `pdf_tools_v2.exe`.
3. Double-click it to launch the app.

### Developers

```bash
git clone https://github.com/KuxarStudio/PDF-Blender.git
cd PDF-Blender
python -m venv venv
# Windows: .\venv\Scripts\activate    macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python pdf_tools_v2.py
```

## Built with

- Python 3 and Tkinter (standard GUI library)
- [pypdf](https://pypi.org/project/pypdf/) for reading, writing, merging and encrypting PDFs
- [pdf2docx](https://pypi.org/project/pdf2docx/) for PDF to Word conversion
- `difflib` (standard library) for text comparison

## Contributing and feedback

Issues and pull requests are welcome. If you use PDF-Blender at work and something is missing, open an issue and say what task you were trying to do.

## License

GNU General Public License v3.0 (GPL-3.0). You are free to use, modify and distribute the software; derived works must also be open source under the same license. See [LICENSE](LICENSE).
