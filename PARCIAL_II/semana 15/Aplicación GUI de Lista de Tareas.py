import tkinter as tk
from tkinter import messagebox


class ListaDeTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Lista de tareas como diccionario con estado
        self.tareas = []

        # ------------------ Entrada de texto ------------------
        self.entry_tarea = tk.Entry(root, width=40)
        self.entry_tarea.pack(pady=10)

        # Evento: presionar "Enter" añade tarea
        self.entry_tarea.bind("<Return>", self.agregar_tarea)

        # ------------------ Botones ------------------
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=5)

        self.btn_agregar = tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar_tarea)
        self.btn_agregar.grid(row=0, column=0, padx=5)

        self.btn_completar = tk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada)
        self.btn_completar.grid(row=0, column=1, padx=5)

        self.btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.btn_eliminar.grid(row=0, column=2, padx=5)

        # ------------------ Listbox ------------------
        self.lista_tareas = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.lista_tareas.pack(pady=10)

        # Evento extra: doble clic marca como completada
        self.lista_tareas.bind("<Double-1>", self.marcar_completada)

    # ------------------ Funciones principales ------------------
    def agregar_tarea(self, event=None):
        """Agrega una nueva tarea a la lista"""
        tarea = self.entry_tarea.get().strip()
        if tarea == "":
            messagebox.showwarning("Entrada vacía", "Por favor escribe una tarea.")
            return
        self.tareas.append({"texto": tarea, "completada": False})
        self.actualizar_lista()
        self.entry_tarea.delete(0, tk.END)

    def marcar_completada(self, event=None):
        """Marca o desmarca como completada la tarea seleccionada"""
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona una tarea de la lista.")
            return
        index = seleccion[0]
        self.tareas[index]["completada"] = not self.tareas[index]["completada"]
        self.actualizar_lista()

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada"""
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para eliminar.")
            return
        index = seleccion[0]
        self.tareas.pop(index)
        self.actualizar_lista()

    def actualizar_lista(self):
        """Refresca la lista de tareas en pantalla"""
        self.lista_tareas.delete(0, tk.END)
        for tarea in self.tareas:
            texto = tarea["texto"]
            if tarea["completada"]:
                texto += " ✅"
            self.lista_tareas.insert(tk.END, texto)


# ------------------ Programa principal ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ListaDeTareas(root)
    root.mainloop()
