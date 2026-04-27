import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter
import os

class FusionadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusionador de PDF Pro")
        self.root.geometry("500x400")
        
        self.archivos = []

        # Interfaz
        self.label = tk.Label(root, text="Archivos seleccionados:", font=("Arial", 12))
        self.label.pack(pady=10)

        # Lista visual de archivos
        self.lista_visual = tk.Listbox(root, selectmode=tk.MULTIPLE, width=60, height=10)
        self.lista_visual.pack(pady=5, padx=20)

        # Botones
        self.btn_añadir = tk.Button(root, text="Añadir PDFs", command=self.seleccionar_archivos, bg="#4CAF50", fg="white")
        self.btn_añadir.pack(pady=5)

        self.btn_limpiar = tk.Button(root, text="Limpiar lista", command=self.limpiar_lista)
        self.btn_limpiar.pack(pady=5)

        self.btn_fusionar = tk.Button(root, text="FUSIONAR Y GUARDAR", command=self.fusionar_archivos, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        self.btn_fusionar.pack(pady=20)

    def seleccionar_archivos(self):
        archivos_nuevos = filedialog.askopenfilenames(
            title="Selecciona los archivos PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        for path in archivos_nuevos:
            if path not in self.archivos:
                self.archivos.append(path)
                self.lista_visual.insert(tk.END, os.path.basename(path))

    def limpiar_lista(self):
        self.archivos = []
        self.lista_visual.delete(0, tk.END)

    def fusionar_archivos(self):
        if len(self.archivos) < 2:
            messagebox.showwarning("Atención", "Selecciona al menos 2 archivos para fusionar.")
            return

        # Preguntar dónde guardar
        ruta_salida = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            title="Guardar PDF fusionado como..."
        )

        if ruta_salida:
            try:
                merger = PdfWriter()
                for pdf in self.archivos:
                    merger.append(pdf)
                
                with open(ruta_salida, "wb") as f_salida:
                    merger.write(f_salida)
                
                merger.close()
                messagebox.showinfo("Éxito", f"Archivo guardado en:\n{ruta_salida}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo fusionar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FusionadorApp(root)
    root.mainloop()