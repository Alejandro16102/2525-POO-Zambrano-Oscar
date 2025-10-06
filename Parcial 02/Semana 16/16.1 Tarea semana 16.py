import tkinter as tk
from tkinter import messagebox, font as tkfont


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas - Atajos de Teclado")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')

        # Lista de tareas
        self.tasks = []

        # Configurar fuentes
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.task_font = tkfont.Font(family="Helvetica", size=11)
        self.shortcut_font = tkfont.Font(family="Courier", size=9)

        self.setup_ui()
        self.bind_shortcuts()

        # Añadir tareas de ejemplo
        self.add_task_internal("Ejemplo: Estudiar Python")
        self.add_task_internal("Ejemplo: Hacer ejercicio")
        self.toggle_complete_internal(1)  # Marcar segunda como completada

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = tk.Label(
            main_frame,
            text="📋 Gestor de Tareas",
            font=self.title_font,
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))

        # Estadísticas
        self.stats_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 9),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.stats_label.pack(pady=(0, 20))

        # Frame para entrada de tareas
        input_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # Campo de entrada
        entry_container = tk.Frame(input_frame, bg='white')
        entry_container.pack(fill=tk.X, padx=10, pady=10)

        self.task_entry = tk.Entry(
            entry_container,
            font=self.task_font,
            relief=tk.FLAT,
            bg='white',
            fg='#2c3e50'
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=5)
        self.task_entry.focus()

        # Botón añadir
        add_button = tk.Button(
            entry_container,
            text="➕ Añadir",
            command=self.add_task,
            font=("Helvetica", 10, "bold"),
            bg='#3498db',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        add_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Hint para Enter
        hint_label = tk.Label(
            input_frame,
            text="💡 Presiona Enter para añadir",
            font=("Helvetica", 8),
            bg='white',
            fg='#95a5a6'
        )
        hint_label.pack(pady=(0, 5))

        # Frame para lista de tareas
        list_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Título de lista
        list_title = tk.Label(
            list_frame,
            text="Lista de Tareas",
            font=("Helvetica", 12, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        list_title.pack(pady=10)

        # Canvas y Scrollbar para tareas
        canvas_frame = tk.Frame(list_frame, bg='white')
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame de atajos de teclado
        shortcuts_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        shortcuts_frame.pack(fill=tk.X)

        shortcuts_title = tk.Label(
            shortcuts_frame,
            text="⌨️ Atajos de Teclado",
            font=("Helvetica", 11, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        shortcuts_title.pack(pady=(10, 5))

        shortcuts_text = [
            "Enter - Añadir tarea",
            "C - Completar tarea seleccionada",
            "D / Delete - Eliminar tarea seleccionada",
            "Escape - Cerrar aplicación"
        ]

        for shortcut in shortcuts_text:
            label = tk.Label(
                shortcuts_frame,
                text=f"  • {shortcut}",
                font=("Helvetica", 9),
                bg='white',
                fg='#7f8c8d',
                anchor='w'
            )
            label.pack(fill=tk.X, padx=20, pady=2)

        tk.Label(shortcuts_frame, text="", bg='white').pack(pady=5)

    def bind_shortcuts(self):
        # Enter para añadir tarea
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        # Atajos globales
        self.root.bind('<c>', lambda e: self.toggle_complete_selected())
        self.root.bind('<C>', lambda e: self.toggle_complete_selected())
        self.root.bind('<d>', lambda e: self.delete_selected())
        self.root.bind('<D>', lambda e: self.delete_selected())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Escape>', lambda e: self.close_app())

    def add_task_internal(self, task_text):
        """Añade tarea sin mostrar notificación (para inicialización)"""
        task_id = len(self.tasks)
        self.tasks.append({
            'id': task_id,
            'text': task_text,
            'completed': False,
            'selected': False
        })
        self.render_tasks()

    def add_task(self):
        task_text = self.task_entry.get().strip()

        if not task_text:
            messagebox.showwarning("Advertencia", "⚠️ Por favor, escribe una tarea")
            return

        task_id = len(self.tasks)
        self.tasks.append({
            'id': task_id,
            'text': task_text,
            'completed': False,
            'selected': False
        })

        self.task_entry.delete(0, tk.END)
        self.render_tasks()
        self.show_notification("✅ Tarea añadida correctamente")

    def toggle_complete(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                status = "completada" if task['completed'] else "marcada como pendiente"
                self.show_notification(f"✓ Tarea {status}")
                break
        self.render_tasks()

    def toggle_complete_internal(self, task_id):
        """Toggle sin notificación (para inicialización)"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                break
        self.render_tasks()

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.render_tasks()
        self.show_notification("🗑️ Tarea eliminada")

    def select_task(self, task_id):
        for task in self.tasks:
            task['selected'] = (task['id'] == task_id)
        self.render_tasks()

    def toggle_complete_selected(self):
        selected = [task for task in self.tasks if task['selected']]
        if selected:
            self.toggle_complete(selected[0]['id'])
        else:
            self.show_notification("⚠️ Selecciona una tarea primero (haz clic sobre ella)")

    def delete_selected(self):
        selected = [task for task in self.tasks if task['selected']]
        if selected:
            self.delete_task(selected[0]['id'])
        else:
            self.show_notification("⚠️ Selecciona una tarea primero (haz clic sobre ella)")

    def render_tasks(self):
        # Limpiar frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Actualizar estadísticas
        pending = sum(1 for task in self.tasks if not task['completed'])
        completed = sum(1 for task in self.tasks if task['completed'])
        self.stats_label.config(text=f"{pending} pendiente(s) • {completed} completada(s)")

        if not self.tasks:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="No hay tareas\n¡Añade tu primera tarea arriba!",
                font=("Helvetica", 11),
                bg='white',
                fg='#bdc3c7',
                pady=50
            )
            empty_label.pack()
            return

        # Renderizar tareas
        for task in self.tasks:
            self.create_task_widget(task)

    def create_task_widget(self, task):
        # Color de fondo según estado
        if task['selected']:
            bg_color = '#e3f2fd'
            border_color = '#2196F3'
        elif task['completed']:
            bg_color = '#e8f5e9'
            border_color = '#4caf50'
        else:
            bg_color = 'white'
            border_color = '#e0e0e0'

        # Frame de tarea
        task_frame = tk.Frame(
            self.scrollable_frame,
            bg=border_color,
            relief=tk.RAISED,
            bd=2
        )
        task_frame.pack(fill=tk.X, padx=5, pady=3)

        inner_frame = tk.Frame(task_frame, bg=bg_color)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Frame de contenido
        content_frame = tk.Frame(inner_frame, bg=bg_color)
        content_frame.pack(fill=tk.X, padx=10, pady=8)

        # Checkbox visual
        check_label = tk.Label(
            content_frame,
            text="✓" if task['completed'] else "○",
            font=("Helvetica", 14),
            bg=bg_color,
            fg='#4caf50' if task['completed'] else '#bdc3c7',
            width=2
        )
        check_label.pack(side=tk.LEFT)

        # Texto de tarea
        text_style = self.task_font.copy()
        if task['completed']:
            text_style.configure(overstrike=True)

        task_label = tk.Label(
            content_frame,
            text=task['text'],
            font=text_style,
            bg=bg_color,
            fg='#7f8c8d' if task['completed'] else '#2c3e50',
            anchor='w'
        )
        task_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # Botones
        button_frame = tk.Frame(content_frame, bg=bg_color)
        button_frame.pack(side=tk.RIGHT)

        complete_btn = tk.Button(
            button_frame,
            text="✓",
            command=lambda: self.toggle_complete(task['id']),
            font=("Helvetica", 12, "bold"),
            bg='#4caf50' if not task['completed'] else '#9e9e9e',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=3,
            height=1
        )
        complete_btn.pack(side=tk.LEFT, padx=2)

        delete_btn = tk.Button(
            button_frame,
            text="🗑",
            command=lambda: self.delete_task(task['id']),
            font=("Helvetica", 12),
            bg='#f44336',
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            width=3,
            height=1
        )
        delete_btn.pack(side=tk.LEFT, padx=2)

        # Hacer toda la tarea clickeable para seleccionar
        for widget in [inner_frame, content_frame, check_label, task_label]:
            widget.bind('<Button-1>', lambda e, tid=task['id']: self.select_task(tid))

    def show_notification(self, message):
        # Crear ventana temporal de notificación
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        notification.configure(bg='#2c3e50')

        label = tk.Label(
            notification,
            text=message,
            font=("Helvetica", 10),
            bg='#2c3e50',
            fg='white',
            padx=20,
            pady=10
        )
        label.pack()

        # Posicionar en esquina inferior derecha
        notification.update_idletasks()
        x = self.root.winfo_x() + self.root.winfo_width() - notification.winfo_width() - 20
        y = self.root.winfo_y() + self.root.winfo_height() - notification.winfo_height() - 20
        notification.geometry(f"+{x}+{y}")

        # Destruir después de 2 segundos
        self.root.after(2000, notification.destroy)

    def close_app(self):
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.destroy()


# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()