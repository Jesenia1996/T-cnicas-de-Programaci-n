import tkinter as tk
from tkinter import messagebox, Button


class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Lista interna para almacenar tareas: (texto, completada)
        self.tareas = []

        # Frame superior: entrada y botón de añadir
        frame_superior = tk.Frame(root)
        frame_superior.pack(pady=10)

        self.entrada_tarea = tk.Entry(frame_superior, width=40, font=("Arial", 12))
        self.entrada_tarea.pack(side=tk.LEFT, padx=5)
        self.entrada_tarea.focus_set()  # Enfocar al iniciar

        btn_anadir: Button = tk.Button(frame_superior, text="Añadir", command=self.anadir_tarea)
        btn_anadir.pack(side=tk.LEFT, padx=5)

        # Frame central: lista de tareas
        frame_lista = tk.Frame(root)
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(frame_lista, width=60, height=12, font=("Arial", 11))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Frame inferior: botones de acción
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        self.btn_completar = tk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada)
        self.btn_completar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Atajos de teclado
        self.entrada_tarea.bind("<Return>", lambda event: self.anadir_tarea())
        self.root.bind("<C>", lambda event: self.marcar_completada())
        self.root.bind("<D>", lambda event: self.eliminar_tarea())
        self.root.bind("<Delete>", lambda event: self.eliminar_tarea())
        self.root.bind("<Escape>", lambda event: self.cerrar_aplicacion())

        # Actualizar la lista al inicio (vacía)
        self.actualizar_lista()

    def anadir_tarea(self):
        texto = self.entrada_tarea.get().strip()
        if texto:
            self.tareas.append([texto, False])  # [texto, completada]
            self.entrada_tarea.delete(0, tk.END)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una tarea válida.")

    def marcar_completada(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.tareas[indice][1] = not self.tareas[indice][1]  # Alternar estado
            self.actualizar_lista()
            self.listbox.selection_set(indice)  # Mantener selección
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para marcarla.")

    def eliminar_tarea(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            del self.tareas[indice]
            self.actualizar_lista()
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminarla.")

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for tarea, completada in self.tareas:
            visual = tarea
            if completada:
                visual = "✓ " + tarea
                # Aplicar estilo visual: tachado (simulado con prefijo)
            self.listbox.insert(tk.END, visual)
            # Opcional: cambiar color (Tkinter Listbox no soporta estilos por ítem fácilmente)
            # Para simplicidad, usamos el prefijo "✓ "

    def cerrar_aplicacion(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()