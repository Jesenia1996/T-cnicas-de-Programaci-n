import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Intentamos importar DateEntry de tkcalendar para el DatePicker
try:
    import tkcalendar
except Exception as e:
    DateEntry = None


EVENTS_FILE = "events.json"
DATE_FORMAT = "%Y-%m-%d"  # formato interno para fecha
TIME_FORMAT = "%H:%M"     # formato interno para hora


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("760x480")
        self.resizable(False, False)

        # Estructura principal: frames
        self.frame_list = ttk.Frame(self, padding=(10, 10))
        self.frame_entry = ttk.Frame(self, padding=(10, 10))
        self.frame_actions = ttk.Frame(self, padding=(10, 10))

        self.frame_list.grid(row=0, column=0, sticky="nsew")
        self.frame_entry.grid(row=1, column=0, sticky="ew")
        self.frame_actions.grid(row=2, column=0, sticky="ew")

        # Configuración de grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Componentes
        self._create_treeview()
        self._create_entry_area()
        self._create_action_buttons()

        # Datos
        self.events = []  # lista de diccionarios: {id, date, time, description}
        self._load_events()

        # Atajos
        self.bind('<Delete>', lambda e: self.delete_selected_event())
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def _create_treeview(self):
        """Crea la vista de lista de eventos (Treeview)"""
        columns = ("date", "time", "description")
        self.tree = ttk.Treeview(self.frame_list, columns=columns, show='headings', height=12)
        self.tree.heading('date', text='Fecha')
        self.tree.heading('time', text='Hora')
        self.tree.heading('description', text='Descripción')
        self.tree.column('date', width=120, anchor='center')
        self.tree.column('time', width=80, anchor='center')
        self.tree.column('description', width=500, anchor='w')

        # Scrollbar
        vsb = ttk.Scrollbar(self.frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        self.frame_list.grid_rowconfigure(0, weight=1)
        self.frame_list.grid_columnconfigure(0, weight=1)

    def _create_entry_area(self):
        """Crea widgets para entrada de datos: fecha, hora y descripción"""
        # Labels
        lbl_date = ttk.Label(self.frame_entry, text="Fecha:")
        lbl_time = ttk.Label(self.frame_entry, text="Hora (HH:MM):")
        lbl_desc = ttk.Label(self.frame_entry, text="Descripción:")

        # Widgets de entrada
        if DateEntry is not None:
            self.entry_date = DateEntry(self.frame_entry, date_pattern='yyyy-mm-dd')
        else:
            # Si no existe tkcalendar, usamos Entry simple con placeholder del formato yyyy-mm-dd
            self.entry_date = ttk.Entry(self.frame_entry)
            self.entry_date.insert(0, datetime.now().strftime(DATE_FORMAT))

        self.entry_time = ttk.Entry(self.frame_entry, width=10)
        self.entry_time.insert(0, datetime.now().strftime(TIME_FORMAT))

        self.entry_desc = ttk.Entry(self.frame_entry, width=60)

        # Posicionamiento usando grid
        lbl_date.grid(row=0, column=0, padx=(0, 6), pady=6, sticky='e')
        self.entry_date.grid(row=0, column=1, padx=(0, 12), pady=6, sticky='w')

        lbl_time.grid(row=0, column=2, padx=(0, 6), pady=6, sticky='e')
        self.entry_time.grid(row=0, column=3, padx=(0, 12), pady=6, sticky='w')

        lbl_desc.grid(row=1, column=0, padx=(0, 6), pady=6, sticky='e')
        self.entry_desc.grid(row=1, column=1, columnspan=3, padx=(0, 12), pady=6, sticky='w')

        # Botón rápido para agregar desde la zona de entrada (también hay en acciones)
        btn_quick_add = ttk.Button(self.frame_entry, text="Agregar rápido", command=self.add_event)
        btn_quick_add.grid(row=0, column=4, padx=(10, 0), pady=6)

    def _create_action_buttons(self):
        """Crea los botones de acciones"""
        btn_add = ttk.Button(self.frame_actions, text="Agregar Evento", command=self.add_event)
        btn_edit = ttk.Button(self.frame_actions, text="Corregir Evento", command=self.edit_selected_event)
        btn_delete = ttk.Button(self.frame_actions, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        btn_exit = ttk.Button(self.frame_actions, text="Salir", command=self.on_exit)

        btn_add.grid(row=0, column=0, padx=8, pady=8)
        btn_edit.grid(row=0, column=1, padx=8, pady=8)
        btn_delete.grid(row=0, column=2, padx=8, pady=8)
        btn_exit.grid(row=0, column=3, padx=8, pady=8)

    # ----------------- Persistencia -----------------
    def _load_events(self):
        """Carga eventos desde EVENTS_FILE si existe"""
        if os.path.exists(EVENTS_FILE):
            try:
                with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
            except Exception:
                messagebox.showwarning("Carga", "No se pudo leer el archivo de eventos. Se iniciará vacío.")
                self.events = []
        else:
            self.events = []
        self._refresh_treeview()

    def _save_events(self):
        """Guarda la lista de eventos en un archivo JSON"""
        try:
            with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Guardar", f"Error al guardar eventos: {e}")

    # ----------------- Operaciones sobre eventos -----------------
    def _refresh_treeview(self):
        """Refresca la vista del Treeview desde self.events"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        # ordenar por fecha y hora
        try:
            sorted_events = sorted(self.events, key=lambda e: (e['date'], e['time']))
        except KeyError:
            sorted_events = self.events

        for ev in sorted_events:
            self.tree.insert('', 'end', iid=ev['id'], values=(ev['date'], ev['time'], ev['description']))

    def _validate_date(self, date_text):
        try:
            datetime.strptime(date_text, DATE_FORMAT)
            return True
        except Exception:
            return False

    def _validate_time(self, time_text):
        try:
            datetime.strptime(time_text, TIME_FORMAT)
            return True
        except Exception:
            return False

    def add_event(self):
        """Agrega un evento nuevo desde los campos de entrada"""
        date_val = self.entry_date.get()
        time_val = self.entry_time.get().strip()
        desc_val = self.entry_desc.get().strip()

        if not date_val or not time_val or not desc_val:
            messagebox.showwarning("Entrada incompleta","Por favor complete fecha, hora y descripción.")
            return

        if not self._validate_date(date_val):
            messagebox.showwarning("Fecha inválida", f"El formato de fecha debe ser {DATE_FORMAT}")
            return

        if not self._validate_time(time_val):
            messagebox.showwarning("Hora inválida", f"El formato de hora debe ser {TIME_FORMAT}")
            return

        # Generar id único
        new_id = str(int(datetime.now().timestamp() * 1000))
        new_event = {
            'id': new_id,
            'date': date_val,
            'time': time_val,
            'description': desc_val
        }
        self.events.append(new_event)
        self._save_events()
        self._refresh_treeview()

        # Limpiar campos de descripción y actualizar fecha/hora a current
        self.entry_desc.delete(0, tk.END)
        # no borrar fecha/hora para comodidad del usuario

    def get_selected_event(self):
        sel = self.tree.selection()
        if not sel:
            return None
        sel_id = sel[0]
        for ev in self.events:
            if ev['id'] == sel_id:
                return ev
        return None

    def edit_selected_event(self):
        """Abre una ventana para editar el evento seleccionado"""
        ev = self.get_selected_event()
        if ev is None:
            messagebox.showinfo("Seleccionar", "Seleccione un evento para corregir.")
            return

        EditEventDialog(self, ev, on_save=self._on_edit_save)

    def _on_edit_save(self, updated_event):
        """Callback cuando se guarda la corrección"""
        # actualizar en self.events
        for i, ev in enumerate(self.events):
            if ev['id'] == updated_event['id']:
                self.events[i] = updated_event
                break
        self._save_events()
        self._refresh_treeview()

    def delete_selected_event(self):
        """Elimina el evento seleccionado con confirmación"""
        ev = self.get_selected_event()
        if ev is None:
            messagebox.showinfo("Seleccionar", "Seleccione un evento para eliminar.")
            return

        answer = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el evento:\n{ev['date']} {ev['time']} - {ev['description']}?")
        if not answer:
            return

        self.events = [e for e in self.events if e['id'] != ev['id']]
        self._save_events()
        self._refresh_treeview()

    def on_exit(self):
        """Acción al cerrar la aplicación"""
        # Guardar antes de salir
        self._save_events()
        self.destroy()


class EditEventDialog(tk.Toplevel):
    """Diálogo para editar un evento existente"""
    def __init__(self, parent, event, on_save=None):
        super().__init__(parent)
        self.title("Corregir Evento")
        self.resizable(False, False)
        self.event = event.copy()
        self.on_save = on_save

        # Widgets
        lbl_date = ttk.Label(self, text="Fecha:")
        lbl_time = ttk.Label(self, text="Hora (HH:MM):")
        lbl_desc = ttk.Label(self, text="Descripción:")

        if DateEntry is not None:
            self.entry_date = DateEntry(self, date_pattern='yyyy-mm-dd')
            # fijar valor
            self.entry_date.set_date(self.event['date'])
        else:
            self.entry_date = ttk.Entry(self)
            self.entry_date.insert(0, self.event['date'])

        self.entry_time = ttk.Entry(self, width=10)
        self.entry_time.insert(0, self.event['time'])

        self.entry_desc = ttk.Entry(self, width=60)
        self.entry_desc.insert(0, self.event['description'])

        # Botones
        btn_save = ttk.Button(self, text="Guardar", command=self._save)
        btn_cancel = ttk.Button(self, text="Cancelar", command=self.destroy)

        # Layout
        lbl_date.grid(row=0, column=0, padx=6, pady=6, sticky='e')
        self.entry_date.grid(row=0, column=1, padx=6, pady=6)
        lbl_time.grid(row=1, column=0, padx=6, pady=6, sticky='e')
        self.entry_time.grid(row=1, column=1, padx=6, pady=6)
        lbl_desc.grid(row=2, column=0, padx=6, pady=6, sticky='e')
        self.entry_desc.grid(row=2, column=1, padx=6, pady=6)

        btn_save.grid(row=3, column=0, padx=6, pady=10)
        btn_cancel.grid(row=3, column=1, padx=6, pady=10)

        # Centramos el diálogo con respecto al padre
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def _save(self):
        date_val = self.entry_date.get()
        time_val = self.entry_time.get().strip()
        desc_val = self.entry_desc.get().strip()

        if not date_val or not time_val or not desc_val:
            messagebox.showwarning("Entrada incompleta", "Por favor complete fecha, hora y descripción.")
            return

        # Validaciones sencillas
        try:
            datetime.strptime(date_val, DATE_FORMAT)
        except Exception:
            messagebox.showwarning("Fecha inválida", f"Formato esperado: {DATE_FORMAT}")
            return

        try:
            datetime.strptime(time_val, TIME_FORMAT)
        except Exception:
            messagebox.showwarning("Hora inválida", f"Formato esperado: {TIME_FORMAT}")
            return

        updated = {
            'id': self.event['id'],
            'date': date_val,
            'time': time_val,
            'description': desc_val
        }

        if self.on_save:
            self.on_save(updated)
        self.destroy()


if __name__ == '__main__':
    # Mensaje de ayuda si no está tkcalendar
    if DateEntry is None:
        print("Aviso: La librería 'tkcalendar' no está instalada. Se usará un campo de texto para la fecha.")
        print("Instale con: pip install tkcalendar  (opcional, para DatePicker)")

    app = AgendaApp()
    app.mainloop()
