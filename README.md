# PDF-Blender (PDF Tools Pro) 🛠️

A comprehensive, 100% offline desktop application designed to manipulate, convert, and secure PDF files. 

Built with Python and Tkinter, this tool was specifically developed for corporate and financial departments to handle sensitive documentation (invoices, contracts, reports) locally, ensuring absolute data privacy without relying on third-party cloud services.

## ✨ Key Features
* **🔗 Merge PDFs:** Combine multiple PDF files into a single document with a specific order.
* **✂️ Split PDF:** Extract a specific range of pages from a large document to create a new one.
* **📝 Convert to Word (.docx):** Transform PDF documents into fully editable Microsoft Word files while maintaining the original layout.
* **🔓 Remove Restrictions (Unprotect):** Bypass owner passwords to enable text highlighting, copying, and editing on restricted documents.
* **🔒 Secure (Protect):** Encrypt sensitive PDFs by adding a user password to prevent unauthorized access.
* **⚖️ Compare Texts:** Analyze two versions of a document and generate an interactive side-by-side HTML report highlighting additions and deletions.

## 🛡️ Why PDF-Blender?
* **Zero Data Leaks:** Processing is done entirely on your local machine. No files are ever uploaded to external servers, guaranteeing maximum confidentiality.
* **User-Friendly GUI:** Simple and intuitive graphical interface designed for non-technical users.
* **Standalone Execution:** Can be compiled into a single `.exe` file, requiring no Python installation for the end-user.

## 🚀 How to Use

### For End-Users (No coding required)
1. Navigate to the **Releases** section on the right side of this repository.
2. Download the latest `pdf_tools_v2.exe` file.
3. Double-click the downloaded file to launch the application.

### For Developers
If you want to run the source code or contribute to the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone [https://github.com/KuxarStudio/PDF-Blender.git](https://github.com/KuxarStudio/PDF-Blender.git)

2. Navigate to the project directory and create a virtual environment:

Bash
cd PDF-Blender
python -m venv venv

3. Activate the virtual environment:

Windows: .\venv\Scripts\activate
macOS/Linux: source venv/bin/activate

4. Install the required dependencies:

pip install pypdf pdf2docx

5. Run the application:

python pdf_tools_v2.py

🛠️ Built With

- Python 3
- Tkinter - Standard GUI library.
- pypdf - For reading, writing, merging, and encrypting PDF files.
- pdf2docx - For PDF to Word conversion.
- difflib - Native library for text comparison.

📄 License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
You are free to use, modify, and distribute this software, but any derived works must also be open-source and distributed under the same license. See the LICENSE file for more details.
