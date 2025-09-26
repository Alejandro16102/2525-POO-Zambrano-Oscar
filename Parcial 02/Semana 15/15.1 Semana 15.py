import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TaskManager:
    def __init__(self, root):
        """
        Inicializa la aplicación de gestión de tareas.

        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Lista para almacenar las tareas como diccionarios
        # Cada tarea tendrá: {'texto': str, 'completada': bool, 'fecha': str}
        self.tasks = []

        # Configurar el estilo de la aplicación
        self.setup_style()

        # Crear la interfaz gráfica
        self.create_widgets()

        # Configurar eventos de teclado
        self.setup_events()

    def setup_style(self):
        """
        Configura el estilo visual de la aplicación.
        """
        # Configurar colores y fuentes
        self.root.configure(bg='#f0f0f0')

        # Crear un estilo personalizado para ttk
        style = ttk.Style()
        style.theme_use('clam')

    def create_widgets(self):
        """
        Crea todos los widgets de la interfaz gráfica.
        Organiza la interfaz en frames para mejor estructura.
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título de la aplicación
        title_label = ttk.Label(main_frame, text="📋 Gestor de Tareas",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Frame para entrada de nueva tarea
        entry_frame = ttk.Frame(main_frame)
        entry_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        entry_frame.columnconfigure(0, weight=1)

        # Campo de entrada para nuevas tareas
        ttk.Label(entry_frame, text="Nueva tarea:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.task_entry = ttk.Entry(entry_frame, font=('Arial', 10))
        self.task_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        # Botón para añadir tarea
        self.add_button = ttk.Button(entry_frame, text="➕ Añadir Tarea",
                                     command=self.add_task)
        self.add_button.grid(row=1, column=1)

        # Frame para la lista de tareas y scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Lista de tareas con scrollbar
        self.task_listbox = tk.Listbox(list_frame, font=('Arial', 10),
                                       selectmode=tk.SINGLE, height=15)
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)

        # Frame para botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)

        # Botones de acción
        self.complete_button = ttk.Button(button_frame, text="✅ Marcar Completada",
                                          command=self.toggle_task_completion)
        self.complete_button.pack(side=tk.LEFT, padx=(0, 5))

        self.delete_button = ttk.Button(button_frame, text="🗑️ Eliminar Tarea",
                                        command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.clear_completed_button = ttk.Button(button_frame, text="🧹 Limpiar Completadas",
                                                 command=self.clear_completed_tasks)
        self.clear_completed_button.pack(side=tk.LEFT, padx=5)

        # Frame para estadísticas
        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        self.stats_label = ttk.Label(stats_frame, text="Total: 0 | Pendientes: 0 | Completadas: 0",
                                     font=('Arial', 9))
        self.stats_label.pack()

    def setup_events(self):
        """
        Configura los eventos de teclado y mouse para mejorar la usabilidad.
        """
        # Permitir añadir tarea presionando Enter en el campo de entrada
        self.task_entry.bind('<Return>', lambda event: self.add_task())

        # Evento de doble clic en una tarea para marcarla como completada
        self.task_listbox.bind('<Double-Button-1>', lambda event: self.toggle_task_completion())

        # Evento de tecla Delete para eliminar tarea seleccionada
        self.task_listbox.bind('<Delete>', lambda event: self.delete_task())

        # Enfocar el campo de entrada al iniciar
        self.task_entry.focus_set()

    def add_task(self):
        """
        Añade una nueva tarea a la lista.
        Valida que el campo no esté vacío y actualiza la interfaz.
        """
        task_text = self.task_entry.get().strip()

        # Validar que la tarea no esté vacía
        if not task_text:
            messagebox.showwarning("Advertencia", "Por favor, introduce una tarea válida.")
            return

        # Crear la nueva tarea como diccionario
        new_task = {
            'texto': task_text,
            'completada': False,
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # Añadir la tarea a la lista
        self.tasks.append(new_task)

        # Limpiar el campo de entrada
        self.task_entry.delete(0, tk.END)

        # Actualizar la visualización
        self.update_task_display()

        # Mostrar mensaje de confirmación (opcional)
        print(f"Tarea añadida: {task_text}")

    def toggle_task_completion(self):
        """
        Marca/desmarca una tarea como completada.
        Cambia el estado visual de la tarea seleccionada.
        """
        selection = self.task_listbox.curselection()

        # Verificar que hay una tarea seleccionada
        if not selection:
            messagebox.showinfo("Información", "Por favor, selecciona una tarea.")
            return

        task_index = selection[0]

        # Cambiar el estado de completada
        self.tasks[task_index]['completada'] = not self.tasks[task_index]['completada']

        # Actualizar la visualización
        self.update_task_display()

        # Mantener la selección en la misma tarea
        self.task_listbox.selection_set(task_index)

        # Mostrar mensaje del cambio de estado
        status = "completada" if self.tasks[task_index]['completada'] else "pendiente"
        print(f"Tarea marcada como {status}: {self.tasks[task_index]['texto']}")

    def delete_task(self):
        """
        Elimina la tarea seleccionada de la lista.
        Pide confirmación antes de eliminar.
        """
        selection = self.task_listbox.curselection()

        # Verificar que hay una tarea seleccionada
        if not selection:
            messagebox.showinfo("Información", "Por favor, selecciona una tarea para eliminar.")
            return

        task_index = selection[0]
        task_text = self.tasks[task_index]['texto']

        # Pedir confirmación antes de eliminar
        confirm = messagebox.askyesno("Confirmar eliminación",
                                      f"¿Estás seguro de que quieres eliminar la tarea:\n'{task_text}'?")

        if confirm:
            # Eliminar la tarea de la lista
            deleted_task = self.tasks.pop(task_index)

            # Actualizar la visualización
            self.update_task_display()

            print(f"Tarea eliminada: {deleted_task['texto']}")

    def clear_completed_tasks(self):
        """
        Elimina todas las tareas completadas.
        Funcionalidad adicional para mejorar la usabilidad.
        """
        completed_tasks = [task for task in self.tasks if task['completada']]

        if not completed_tasks:
            messagebox.showinfo("Información", "No hay tareas completadas para eliminar.")
            return

        # Pedir confirmación
        confirm = messagebox.askyesno("Confirmar eliminación",
                                      f"¿Eliminar {len(completed_tasks)} tarea(s) completada(s)?")

        if confirm:
            # Filtrar solo las tareas no completadas
            self.tasks = [task for task in self.tasks if not task['completada']]

            # Actualizar la visualización
            self.update_task_display()

            print(f"Eliminadas {len(completed_tasks)} tareas completadas")

    def update_task_display(self):
        """
        Actualiza la visualización de la lista de tareas.
        Formatea las tareas según su estado (completada o pendiente).
        """
        # Limpiar la lista actual
        self.task_listbox.delete(0, tk.END)

        # Añadir cada tarea con su formato correspondiente
        for i, task in enumerate(self.tasks):
            if task['completada']:
                # Formato para tareas completadas: texto tachado y marca de completado
                display_text = f"✅ {task['texto']} (Completada - {task['fecha']})"
                self.task_listbox.insert(tk.END, display_text)
                # Cambiar color para tareas completadas
                self.task_listbox.itemconfig(i, {'fg': 'gray'})
            else:
                # Formato para tareas pendientes
                display_text = f"⏳ {task['texto']} (Añadida - {task['fecha']})"
                self.task_listbox.insert(tk.END, display_text)
                # Color normal para tareas pendientes
                self.task_listbox.itemconfig(i, {'fg': 'black'})

        # Actualizar estadísticas
        self.update_statistics()

    def update_statistics(self):
        """
        Actualiza las estadísticas mostradas en la parte inferior.
        """
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task['completada']])
        pending_tasks = total_tasks - completed_tasks

        stats_text = f"Total: {total_tasks} | Pendientes: {pending_tasks} | Completadas: {completed_tasks}"
        self.stats_label.config(text=stats_text)


def main():
    """
    Función principal para ejecutar la aplicación.
    """
    # Crear la ventana principal
    root = tk.Tk()

    # Crear la aplicación de gestión de tareas
    app = TaskManager(root)

    # Configurar el comportamiento al cerrar la ventana
    root.protocol("WM_DELETE_WINDOW", lambda: (print("Cerrando aplicación..."), root.destroy()))

    # Iniciar el bucle principal de la aplicación
    root.mainloop()


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()