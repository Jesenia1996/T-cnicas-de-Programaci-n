import tkinter as tk
from tkinter import messagebox

# -----------------------
# Aplicación GUI Básica
# -----------------------

def agregar_dato():
    """Agrega el texto ingresado a la lista."""
    dato = entrada.get().strip()
    if dato:  # Validar que no esté vacío
        lista_datos.insert(tk.END, dato)
        entrada.delete(0, tk.END)  # Limpiar el campo después de agregar
    else:
        messagebox.showwarning("Advertencia", "El campo está vacío, ingrese un dato.")

def limpiar_dato():
    """Limpia el dato seleccionado o toda la lista si no hay selección."""
    seleccion = lista_datos.curselection()
    if seleccion:  # Si hay un ítem seleccionado
        lista_datos.delete(seleccion)
    else:
        confirmacion = messagebox.askyesno("Confirmar", "¿Desea limpiar toda la lista?")
        if confirmacion:
            lista_datos.delete(0, tk.END)

# -----------------------
# Ventana principal
# -----------------------
ventana = tk.Tk()
ventana.title("Aplicación GUI Básica - Gestión de Datos")
ventana.geometry("400x300")

# -----------------------
# Componentes GUI
# -----------------------
label = tk.Label(ventana, text="Ingrese un dato:", font=("Arial", 12))
label.pack(pady=5)

entrada = tk.Entry(ventana, width=40)
entrada.pack(pady=5)

btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato, bg="lightgreen")
btn_agregar.pack(pady=5)

btn_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_dato, bg="lightcoral")
btn_limpiar.pack(pady=5)

lista_datos = tk.Listbox(ventana, width=50, height=10)
lista_datos.pack(pady=10)

# -----------------------
# Ejecutar aplicación
# -----------------------
ventana.mainloop()
