import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter, PdfReader
import os
from pdf2docx import Converter
import difflib # <-- Nueva librería nativa para comparar
import webbrowser # <-- Para abrir el reporte HTML automáticamente

class PDFToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tools Pro 2.5")
        self.root.geometry("500x600") # Ventana un poco más alta
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Variables para todas las herramientas
        self.archivos = []
        self.archivo_a_dividir = None
        self.archivo_a_convertir = None
        self.archivo_a_desproteger = None
        self.archivo_a_proteger = None
        self.archivo_comp_1 = None # Comparador: PDF 1
        self.archivo_comp_2 = None # Comparador: PDF 2
        
        self.mostrar_menu()

    def limpiar_pantalla(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpiar_pantalla()
        tk.Label(self.main_frame, text="🛠️ PDF Tools Pro 2.5", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.main_frame, text="Selecciona la herramienta que necesitas:", font=("Arial", 12)).pack(pady=10)
        
        # Lista de herramientas (¡Ahora con 6 opciones!)
        botones = [
            ("🔗 Fusionar PDFs", "#4CAF50", self.interfaz_fusionar),
            ("✂️ Dividir PDF", "#FF9800", self.interfaz_dividir),
            ("📝 Convertir a Word", "#2196F3", self.interfaz_convertir_word),
            ("🔓 Desproteger PDF", "#F44336", self.interfaz_desproteger),
            ("🔒 Proteger (Añadir Clave)", "#607D8B", self.interfaz_proteger),
            ("⚖️ Comparar Textos", "#9C27B0", self.interfaz_comparar) # Nuevo botón morado
        ]
        
        for texto, color, comando in botones:
            tk.Button(self.main_frame, text=texto, bg=color, fg="white", font=("Arial", 11, "bold"), 
                      width=30, pady=8, command=comando, cursor="hand2").pack(pady=5)

    # ==========================================
    # MÓDULO 1: FUSIONAR PDF
    # ==========================================
    def interfaz_fusionar(self):
        self.limpiar_pantalla()
        self.archivos = [] 
        tk.Label(self.main_frame, text="🔗 Módulo: Fusionador", font=("Arial", 16, "bold"), fg="#4CAF50").pack(pady=10)
        self.lista_visual = tk.Listbox(self.main_frame, selectmode=tk.MULTIPLE, width=60, height=8)
        self.lista_visual.pack(pady=5, padx=20)
        tk.Button(self.main_frame, text="Añadir PDFs", command=self.seleccionar_archivos, bg="#e0e0e0").pack(pady=5)
        tk.Button(self.main_frame, text="Limpiar lista", command=self.limpiar_lista).pack(pady=5)
        tk.Button(self.main_frame, text="FUSIONAR Y GUARDAR", command=self.fusionar_archivos, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_archivos(self):
        archivos_nuevos = filedialog.askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])
        for path in archivos_nuevos:
            if path not in self.archivos:
                self.archivos.append(path)
                self.lista_visual.insert(tk.END, os.path.basename(path))

    def limpiar_lista(self):
        self.archivos = []
        self.lista_visual.delete(0, tk.END)

    def fusionar_archivos(self):
        if len(self.archivos) < 2: return messagebox.showwarning("Atención", "Selecciona al menos 2 archivos.")
        ruta_salida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivo PDF", "*.pdf")])
        if ruta_salida:
            try:
                merger = PdfWriter()
                for pdf in self.archivos: merger.append(pdf)
                with open(ruta_salida, "wb") as f: merger.write(f)
                merger.close()
                messagebox.showinfo("Éxito", f"Guardado en:\n{ruta_salida}")
                self.limpiar_lista() 
            except Exception as e: messagebox.showerror("Error", f"Fallo: {e}")

    # ==========================================
    # MÓDULO 2: DIVIDIR PDF
    # ==========================================
    def interfaz_dividir(self):
        self.limpiar_pantalla()
        self.archivo_a_dividir = None 
        tk.Label(self.main_frame, text="✂️ Módulo: Dividir PDF", font=("Arial", 16, "bold"), fg="#FF9800").pack(pady=10)
        self.lbl_archivo_div = tk.Label(self.main_frame, text="Ningún archivo seleccionado", fg="gray")
        self.lbl_archivo_div.pack(pady=15)
        tk.Button(self.main_frame, text="Seleccionar PDF", command=self.seleccionar_pdf_dividir, bg="#e0e0e0").pack(pady=5)
        frame_paginas = tk.Frame(self.main_frame)
        frame_paginas.pack(pady=20)
        tk.Label(frame_paginas, text="Desde:").grid(row=0, column=0)
        self.entry_desde = tk.Entry(frame_paginas, width=5)
        self.entry_desde.grid(row=0, column=1, padx=5)
        tk.Label(frame_paginas, text="Hasta:").grid(row=0, column=2)
        self.entry_hasta = tk.Entry(frame_paginas, width=5)
        self.entry_hasta.grid(row=0, column=3, padx=5)
        tk.Button(self.main_frame, text="EXTRAER Y GUARDAR", command=self.dividir_archivo, bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(pady=20)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_pdf_dividir(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if archivo:
            self.archivo_a_dividir = archivo
            self.lbl_archivo_div.config(text=f"📄 {os.path.basename(archivo)}", fg="black")

    def dividir_archivo(self):
        if not self.archivo_a_dividir: return messagebox.showwarning("Atención", "Selecciona un PDF.")
        try:
            reader = PdfReader(self.archivo_a_dividir)
            writer = PdfWriter()
            for i in range(int(self.entry_desde.get())-1, int(self.entry_hasta.get())):
                writer.add_page(reader.pages[i])
            ruta = filedialog.asksaveasfilename(defaultextension=".pdf")
            if ruta:
                with open(ruta, "wb") as f: writer.write(f)
                messagebox.showinfo("Éxito", "Páginas extraídas.")
        except Exception as e: messagebox.showerror("Error", f"Fallo: {e}")

    # ==========================================
    # MÓDULO 3: CONVERTIR A WORD
    # ==========================================
    def interfaz_convertir_word(self):
        self.limpiar_pantalla()
        tk.Label(self.main_frame, text="📝 Módulo: Convertir a Word", font=("Arial", 16, "bold"), fg="#2196F3").pack(pady=10)
        self.lbl_archivo_word = tk.Label(self.main_frame, text="Ningún archivo seleccionado", fg="gray")
        self.lbl_archivo_word.pack(pady=15)
        tk.Button(self.main_frame, text="Seleccionar PDF", command=self.seleccionar_pdf_word, bg="#e0e0e0").pack(pady=5)
        tk.Button(self.main_frame, text="CONVERTIR A DOCX", command=self.convertir_a_word, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_pdf_word(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if archivo:
            self.archivo_a_convertir = archivo
            self.lbl_archivo_word.config(text=f"📄 {os.path.basename(archivo)}", fg="black")

    def convertir_a_word(self):
        if not self.archivo_a_convertir: return
        ruta = filedialog.asksaveasfilename(defaultextension=".docx")
        if ruta:
            try:
                cv = Converter(self.archivo_a_convertir)
                cv.convert(ruta); cv.close()
                messagebox.showinfo("Éxito", "Convertido correctamente.")
            except Exception as e: messagebox.showerror("Error", e)

    # ==========================================
    # MÓDULO 4: DESPROTEGER PDF
    # ==========================================
    def interfaz_desproteger(self):
        self.limpiar_pantalla()
        self.archivo_a_desproteger = None
        tk.Label(self.main_frame, text="🔓 Módulo: Desproteger PDF", font=("Arial", 16, "bold"), fg="#F44336").pack(pady=10)
        self.lbl_archivo_desproteger = tk.Label(self.main_frame, text="Ningún archivo seleccionado", fg="gray")
        self.lbl_archivo_desproteger.pack(pady=10)
        tk.Button(self.main_frame, text="Seleccionar PDF Bloqueado", command=self.seleccionar_pdf_desproteger, bg="#e0e0e0").pack(pady=5)
        tk.Label(self.main_frame, text="Contraseña (solo si pide clave para abrir):", font=("Arial", 9, "italic")).pack(pady=5)
        self.entry_pass_desproteger = tk.Entry(self.main_frame, show="*", width=20)
        self.entry_pass_desproteger.pack(pady=5)
        tk.Button(self.main_frame, text="ELIMINAR RESTRICCIONES", command=self.desproteger_pdf, bg="#F44336", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_pdf_desproteger(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if archivo:
            self.archivo_a_desproteger = archivo
            self.lbl_archivo_desproteger.config(text=f"📄 {os.path.basename(archivo)}", fg="black")

    def desproteger_pdf(self):
        if not self.archivo_a_desproteger: return
        password = self.entry_pass_desproteger.get()
        try:
            reader = PdfReader(self.archivo_a_desproteger)
            if reader.is_encrypted and not reader.decrypt(password if password else ""):
                return messagebox.showwarning("Clave requerida", "Requiere contraseña de apertura.")
            writer = PdfWriter()
            for page in reader.pages: writer.add_page(page)
            ruta = filedialog.asksaveasfilename(defaultextension=".pdf")
            if ruta:
                with open(ruta, "wb") as f: writer.write(f)
                messagebox.showinfo("Éxito", "Restricciones eliminadas.")
                self.entry_pass_desproteger.delete(0, tk.END)
        except Exception as e: messagebox.showerror("Error", e)

    # ==========================================
    # MÓDULO 5: PROTEGER PDF
    # ==========================================
    def interfaz_proteger(self):
        self.limpiar_pantalla()
        tk.Label(self.main_frame, text="🔒 Módulo: Proteger PDF", font=("Arial", 16, "bold"), fg="#607D8B").pack(pady=10)
        self.lbl_archivo_proteger = tk.Label(self.main_frame, text="Ningún archivo seleccionado", fg="gray")
        self.lbl_archivo_proteger.pack(pady=10)
        tk.Button(self.main_frame, text="Seleccionar PDF", command=self.seleccionar_pdf_proteger, bg="#e0e0e0").pack(pady=5)
        tk.Label(self.main_frame, text="Nueva contraseña:").pack(pady=5)
        self.entry_pass_proteger = tk.Entry(self.main_frame, show="*", width=20)
        self.entry_pass_proteger.pack(pady=5)
        tk.Button(self.main_frame, text="APLICAR CANDADO", command=self.proteger_pdf, bg="#607D8B", fg="white", font=("Arial", 10, "bold")).pack(pady=15)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_pdf_proteger(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if archivo:
            self.archivo_a_proteger = archivo
            self.lbl_archivo_proteger.config(text=f"📄 {os.path.basename(archivo)}", fg="black")

    def proteger_pdf(self):
        if not self.archivo_a_proteger or not self.entry_pass_proteger.get(): return
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf")
        if ruta:
            try:
                reader = PdfReader(self.archivo_a_proteger)
                writer = PdfWriter()
                for page in reader.pages: writer.add_page(page)
                writer.encrypt(self.entry_pass_proteger.get())
                with open(ruta, "wb") as f: writer.write(f)
                messagebox.showinfo("Éxito", "PDF protegido correctamente.")
            except Exception as e: messagebox.showerror("Error", e)

    # ==========================================
    # MÓDULO 6: COMPARAR PDFs
    # ==========================================
    def interfaz_comparar(self):
        self.limpiar_pantalla()
        self.archivo_comp_1 = None
        self.archivo_comp_2 = None
        
        tk.Label(self.main_frame, text="⚖️ Módulo: Comparar PDFs", font=("Arial", 16, "bold"), fg="#9C27B0").pack(pady=10)
        tk.Label(self.main_frame, text="Extrae el texto y muestra las diferencias en una web", fg="gray", font=("Arial", 9)).pack()
        
        # Selección Archivo 1
        self.lbl_comp_1 = tk.Label(self.main_frame, text="Documento Original: Ninguno", fg="gray")
        self.lbl_comp_1.pack(pady=(15, 5))
        tk.Button(self.main_frame, text="Seleccionar Versión 1", command=lambda: self.seleccionar_comp(1), bg="#e0e0e0").pack()

        # Selección Archivo 2
        self.lbl_comp_2 = tk.Label(self.main_frame, text="Documento Modificado: Ninguno", fg="gray")
        self.lbl_comp_2.pack(pady=(15, 5))
        tk.Button(self.main_frame, text="Seleccionar Versión 2", command=lambda: self.seleccionar_comp(2), bg="#e0e0e0").pack()

        tk.Button(self.main_frame, text="GENERAR REPORTE", command=self.comparar_pdfs, bg="#9C27B0", fg="white", font=("Arial", 10, "bold")).pack(pady=25)
        tk.Button(self.main_frame, text="⬅️ Volver al Menú", command=self.mostrar_menu, font=("Arial", 10)).pack(side=tk.BOTTOM, pady=20)

    def seleccionar_comp(self, num):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if archivo:
            if num == 1:
                self.archivo_comp_1 = archivo
                self.lbl_comp_1.config(text=f"📄 Versión 1: {os.path.basename(archivo)}", fg="black")
            else:
                self.archivo_comp_2 = archivo
                self.lbl_comp_2.config(text=f"📄 Versión 2: {os.path.basename(archivo)}", fg="black")

    def extraer_texto_pdf(self, ruta_pdf):
        texto_total = ""
        reader = PdfReader(ruta_pdf)
        for page in reader.pages:
            texto = page.extract_text()
            if texto:
                texto_total += texto + "\n"
        return texto_total

    def comparar_pdfs(self):
        if not self.archivo_comp_1 or not self.archivo_comp_2:
            return messagebox.showwarning("Atención", "Debes seleccionar los dos PDFs para comparar.")
            
        ruta_salida = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Página Web", "*.html")], title="Guardar informe comparativo")
        
        if ruta_salida:
            try:
                # Extraemos el texto de ambos PDFs
                texto1 = self.extraer_texto_pdf(self.archivo_comp_1).splitlines()
                texto2 = self.extraer_texto_pdf(self.archivo_comp_2).splitlines()
                
                # Generamos el archivo HTML con las diferencias
                html_diff = difflib.HtmlDiff(wrapcolumn=60).make_file(texto1, texto2, context=True, numlines=2)
                
                with open(ruta_salida, "w", encoding="utf-8") as f:
                    f.write(html_diff)
                    
                messagebox.showinfo("Éxito", "Informe generado. Se abrirá en tu navegador.")
                
                # Abrimos el HTML automáticamente en Chrome/Edge/Firefox
                webbrowser.open('file://' + os.path.realpath(ruta_salida))
                
            except Exception as e:
                messagebox.showerror("Error", f"Fallo al comparar: {e}")

if __name__ == "__main__":
    root = tk.Tk(); app = PDFToolsApp(root); root.mainloop()