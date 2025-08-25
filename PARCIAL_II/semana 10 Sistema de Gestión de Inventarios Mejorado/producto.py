class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        """Constructor de la clase Producto"""
        self.id_producto = id_producto      # identificador único del producto
        self.nombre = nombre                # Nombre del producto
        self.cantidad = cantidad            # Cantidad que tengo en mi inventario
        self.precio = precio                # Precio unitario por producto

    # Getters
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

    def __str__(self):
        """Lo utilizo para imprimir la información del producto y que sea más clara"""
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"

    def to_linea(self):
        """Convierte el producto en línea de texto para archivo"""
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}\n"

    @staticmethod
    def from_linea(linea):
        """Convierte una línea de archivo en objeto Producto"""
        try:
            id_producto, nombre, cantidad, precio = linea.strip().split(",")
            return Producto(id_producto, nombre, int(cantidad), float(precio))
        except ValueError:
            print(f"⚠️ Línea inválida en archivo: {linea}")
            return None