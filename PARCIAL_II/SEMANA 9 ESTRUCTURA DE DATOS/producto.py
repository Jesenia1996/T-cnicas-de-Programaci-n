# Clase que representa un producto en el inventario

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Crea un producto con ID único, nombre, cantidad y precio.
        El ID no se puede modificar después.
        """
        self.__id = id_producto  # Atributo privado (ID único)
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # ------ Getters ------
    def get_id(self):
        """Devuelve el ID del producto."""
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    # ------ Setters ------
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            print("❌ La cantidad no puede ser negativa.")

    def set_precio(self, precio):
        if precio >= 0:
            self.__precio = precio
        else:
            print("❌ El precio no puede ser negativo.")

    def __str__(self):
        """Texto legible al imprimir el producto."""
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"