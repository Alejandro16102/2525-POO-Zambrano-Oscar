import tkinter as tk
from tkinter import ttk


class DataManagerGUI:
    def __init__(self):
        # Ventana principal con título descriptivo
        self.root = tk.Tk()
        self.root.title("Gestor de Datos - Aplicación GUI")
        self.root.geometry("400x300")

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta
        tk.Label(self.root, text="Ingrese información:", font=("Arial", 12)).pack(pady=10)

        # Campo de texto
        self.entry = tk.Entry(self.root, width=30, font=("Arial", 10))
        self.entry.pack(pady=5)

        # Frame para botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Botón Agregar
        self.add_btn = tk.Button(button_frame, text="Agregar", command=self.add_data,
                                 bg="#4CAF50", fg="white", width=10)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        # Botón Limpiar
        self.clear_btn = tk.Button(button_frame, text="Limpiar", command=self.clear_data,
                                   bg="#f44336", fg="white", width=10)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Etiqueta para la lista
        tk.Label(self.root, text="Datos guardados:", font=("Arial", 12)).pack(pady=(20, 5))

        # Lista para mostrar datos
        self.listbox = tk.Listbox(self.root, width=50, height=8)
        self.listbox.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # Scrollbar para la lista
        scrollbar = tk.Scrollbar(self.listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    def add_data(self):
        """Evento: Agregar información a la lista"""
        data = self.entry.get().strip()
        if data:
            self.listbox.insert(tk.END, data)
            self.entry.delete(0, tk.END)  # Limpiar campo de texto

    def clear_data(self):
        """Evento: Limpiar información seleccionada o todo"""
        selection = self.listbox.curselection()
        if selection:
            # Limpiar elemento seleccionado
            self.listbox.delete(selection[0])
        else:
            # Limpiar toda la lista si no hay selección
            self.listbox.delete(0, tk.END)
        self.entry.delete(0, tk.END)  # También limpiar campo de texto

    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    app = DataManagerGUI()
    app.run()