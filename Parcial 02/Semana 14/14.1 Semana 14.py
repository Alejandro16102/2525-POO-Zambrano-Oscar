import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import calendar


class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # Lista para almacenar los eventos
        self.eventos = []

        # Variables para el DatePicker personalizado
        self.fecha_seleccionada = datetime.date.today()
        self.ventana_calendario = None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título de la aplicación
        titulo = tk.Label(main_frame, text="AGENDA PERSONAL",
                          font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=(0, 20))

        # Frame para la visualización de eventos (TreeView)
        frame_eventos = tk.LabelFrame(main_frame, text="Eventos Programados",
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        frame_eventos.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # TreeView para mostrar los eventos
        columnas = ('ID', 'Fecha', 'Hora', 'Descripción')
        self.tree = ttk.Treeview(frame_eventos, columns=columnas, show='headings', height=10)

        # Configurar encabezados
        self.tree.heading('ID', text='ID')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Hora', text='Hora')
        self.tree.heading('Descripción', text='Descripción')

        # Configurar ancho de columnas
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('Fecha', width=100, anchor=tk.CENTER)
        self.tree.column('Hora', width=80, anchor=tk.CENTER)
        self.tree.column('Descripción', width=500, anchor=tk.W)

        # Scrollbar para el TreeView
        scrollbar = ttk.Scrollbar(frame_eventos, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar TreeView y Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))

        # Frame para entrada de datos
        frame_entrada = tk.LabelFrame(main_frame, text="Agregar Nuevo Evento",
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        frame_entrada.pack(fill=tk.X, pady=(0, 20))

        # Crear campos de entrada en una cuadrícula
        # Fecha
        tk.Label(frame_entrada, text="Fecha:", font=('Arial', 10),
                 bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        # Frame para fecha con botón de calendario
        fecha_frame = tk.Frame(frame_entrada, bg='#f0f0f0')
        fecha_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.fecha_var = tk.StringVar()
        self.fecha_var.set(self.fecha_seleccionada.strftime('%d/%m/%Y'))

        self.fecha_entry = tk.Entry(fecha_frame, width=12, font=('Arial', 10),
                                    textvariable=self.fecha_var, state='readonly')
        self.fecha_entry.pack(side=tk.LEFT)

        btn_calendario = tk.Button(fecha_frame, text="📅", command=self.abrir_calendario,
                                   font=('Arial', 8), padx=5)
        btn_calendario.pack(side=tk.LEFT, padx=(2, 0))

        # Hora
        tk.Label(frame_entrada, text="Hora:", font=('Arial', 10),
                 bg='#f0f0f0', fg='#2c3e50').grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)

        self.hora_entry = tk.Entry(frame_entrada, width=10, font=('Arial', 10))
        self.hora_entry.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)
        self.hora_entry.insert(0, "09:00")

        # Descripción
        tk.Label(frame_entrada, text="Descripción:", font=('Arial', 10),
                 bg='#f0f0f0', fg='#2c3e50').grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

        self.desc_entry = tk.Entry(frame_entrada, width=50, font=('Arial', 10))
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

        # Configurar expansión de columnas
        frame_entrada.grid_columnconfigure(1, weight=1)

        # Frame para botones de acción
        frame_botones = tk.Frame(main_frame, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X, pady=10)

        # Botones
        btn_agregar = tk.Button(frame_botones, text="Agregar Evento",
                                command=self.agregar_evento, bg='#27ae60', fg='white',
                                font=('Arial', 10, 'bold'), padx=20, pady=8,
                                cursor='hand2')
        btn_agregar.pack(side=tk.LEFT, padx=(0, 10))

        btn_eliminar = tk.Button(frame_botones, text="Eliminar Evento Seleccionado",
                                 command=self.eliminar_evento, bg='#e74c3c', fg='white',
                                 font=('Arial', 10, 'bold'), padx=20, pady=8,
                                 cursor='hand2')
        btn_eliminar.pack(side=tk.LEFT, padx=10)

        btn_salir = tk.Button(frame_botones, text="Salir",
                              command=self.salir_aplicacion, bg='#95a5a6', fg='white',
                              font=('Arial', 10, 'bold'), padx=20, pady=8,
                              cursor='hand2')
        btn_salir.pack(side=tk.RIGHT)

        # Agregar algunos eventos de ejemplo
        self.agregar_eventos_ejemplo()

    def abrir_calendario(self):
        if self.ventana_calendario:
            self.ventana_calendario.destroy()

        self.ventana_calendario = tk.Toplevel(self.root)
        self.ventana_calendario.title("Seleccionar Fecha")
        self.ventana_calendario.geometry("250x280")
        self.ventana_calendario.configure(bg='white')
        self.ventana_calendario.resizable(False, False)

        # Centrar la ventana
        self.ventana_calendario.transient(self.root)
        self.ventana_calendario.grab_set()

        # Variables para el calendario
        self.cal_year = self.fecha_seleccionada.year
        self.cal_month = self.fecha_seleccionada.month

        self.crear_calendario()

    def crear_calendario(self):
        # Limpiar ventana
        for widget in self.ventana_calendario.winfo_children():
            widget.destroy()

        # Frame para navegación
        nav_frame = tk.Frame(self.ventana_calendario, bg='white')
        nav_frame.pack(pady=10)

        btn_prev = tk.Button(nav_frame, text="<", command=self.mes_anterior,
                             font=('Arial', 10, 'bold'))
        btn_prev.pack(side=tk.LEFT, padx=5)

        mes_año = tk.Label(nav_frame, text=f"{calendar.month_name[self.cal_month]} {self.cal_year}",
                           font=('Arial', 12, 'bold'), bg='white')
        mes_año.pack(side=tk.LEFT, padx=20)

        btn_next = tk.Button(nav_frame, text=">", command=self.mes_siguiente,
                             font=('Arial', 10, 'bold'))
        btn_next.pack(side=tk.LEFT, padx=5)

        # Frame para el calendario
        cal_frame = tk.Frame(self.ventana_calendario, bg='white')
        cal_frame.pack(padx=10, pady=5)

        # Días de la semana
        dias_semana = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do']
        for i, dia in enumerate(dias_semana):
            tk.Label(cal_frame, text=dia, font=('Arial', 9, 'bold'),
                     bg='lightgray', width=3).grid(row=0, column=i, padx=1, pady=1)

        # Obtener calendario del mes
        cal = calendar.monthcalendar(self.cal_year, self.cal_month)

        for semana_num, semana in enumerate(cal, 1):
            for dia_num, dia in enumerate(semana):
                if dia == 0:
                    tk.Label(cal_frame, text="", width=3, height=1, bg='white').grid(
                        row=semana_num, column=dia_num, padx=1, pady=1)
                else:
                    btn = tk.Button(cal_frame, text=str(dia), width=3, height=1,
                                    command=lambda d=dia: self.seleccionar_dia(d))
                    btn.grid(row=semana_num, column=dia_num, padx=1, pady=1)

                    # Resaltar día actual
                    if (self.cal_year == datetime.date.today().year and
                            self.cal_month == datetime.date.today().month and
                            dia == datetime.date.today().day):
                        btn.configure(bg='lightblue')

    def mes_anterior(self):
        if self.cal_month == 1:
            self.cal_month = 12
            self.cal_year -= 1
        else:
            self.cal_month -= 1
        self.crear_calendario()

    def mes_siguiente(self):
        if self.cal_month == 12:
            self.cal_month = 1
            self.cal_year += 1
        else:
            self.cal_month += 1
        self.crear_calendario()

    def seleccionar_dia(self, dia):
        self.fecha_seleccionada = datetime.date(self.cal_year, self.cal_month, dia)
        self.fecha_var.set(self.fecha_seleccionada.strftime('%d/%m/%Y'))
        self.ventana_calendario.destroy()
        self.ventana_calendario = None

    def agregar_evento(self):
        # Obtener datos de los campos de entrada
        fecha = self.fecha_var.get()
        hora = self.hora_entry.get().strip()
        descripcion = self.desc_entry.get().strip()

        # Validar campos
        if not hora or not descripcion:
            messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
            return

        # Validar formato de hora
        if not self.validar_hora(hora):
            messagebox.showerror("Hora inválida",
                                 "Por favor, ingrese una hora válida en formato HH:MM (ejemplo: 14:30)")
            return

        # Crear nuevo evento
        evento_id = len(self.eventos) + 1
        nuevo_evento = {
            'id': evento_id,
            'fecha': fecha,
            'hora': hora,
            'descripcion': descripcion
        }

        # Agregar evento a la lista
        self.eventos.append(nuevo_evento)

        # Actualizar TreeView
        self.tree.insert('', 'end', values=(evento_id, fecha, hora, descripcion))

        # Limpiar campos de entrada
        self.limpiar_campos()

        # Mensaje de confirmación
        messagebox.showinfo("Éxito", "Evento agregado correctamente.")

    def eliminar_evento(self):
        # Obtener elemento seleccionado
        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un evento para eliminar.")
            return

        # Diálogo de confirmación
        if messagebox.askyesno("Confirmar eliminación",
                               "¿Está seguro de que desea eliminar el evento seleccionado?"):
            # Obtener ID del evento seleccionado
            item = self.tree.item(seleccion[0])
            evento_id = item['values'][0]

            # Eliminar de la lista de eventos
            self.eventos = [evento for evento in self.eventos if evento['id'] != evento_id]

            # Eliminar del TreeView
            self.tree.delete(seleccion[0])

            messagebox.showinfo("Éxito", "Evento eliminado correctamente.")

    def validar_hora(self, hora):
        try:
            # Validar formato HH:MM
            datetime.datetime.strptime(hora, '%H:%M')
            return True
        except ValueError:
            return False

    def limpiar_campos(self):
        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, "09:00")
        self.desc_entry.delete(0, tk.END)

    def salir_aplicacion(self):
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir de la aplicación?"):
            self.root.quit()

    def agregar_eventos_ejemplo(self):
        # Algunos eventos de ejemplo para mostrar la funcionalidad
        hoy = datetime.date.today()
        eventos_ejemplo = [
            {
                'fecha': hoy.strftime('%d/%m/%Y'),
                'hora': '09:00',
                'descripcion': 'Reunión de trabajo - Revisión de proyecto'
            },
            {
                'fecha': (hoy + datetime.timedelta(days=1)).strftime('%d/%m/%Y'),
                'hora': '14:30',
                'descripcion': 'Cita médica - Control general'
            },
            {
                'fecha': (hoy + datetime.timedelta(days=3)).strftime('%d/%m/%Y'),
                'hora': '18:00',
                'descripcion': 'Cumpleaños de Ana - Restaurante'
            }
        ]

        for evento in eventos_ejemplo:
            evento_id = len(self.eventos) + 1
            evento['id'] = evento_id
            self.eventos.append(evento)
            self.tree.insert('', 'end', values=(evento_id, evento['fecha'],
                                                evento['hora'], evento['descripcion']))


def main():
    # Crear ventana principal
    root = tk.Tk()

    # Crear instancia de la aplicación
    app = AgendaApp(root)

    # Iniciar bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()