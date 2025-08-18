#from producto import Producto

# Clase Inventario
class Inventario:
    def __init__(self):
        """Inicializa el inventario con una lista vacía de productos"""
        self.productos = []

    def anadir_producto(self, producto):

        """
        Añade un nuevo producto al inventario.
        Se valida que el ID sea único.
        """
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: El ID ya existe. No se puede añadir el producto.")
                return
        self.productos.append(producto)
        print("✅ Producto añadido correctamente.")

    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID"""
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("✅ Producto eliminado.")
                return
        print("❌ Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza la cantidad o el precio de un producto por su ID"""
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("✅ Producto actualizado.")
                return
        print("❌ Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (pueden existir varios similares)"""
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("🔍 Resultados de la búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """Muestra todos los productos en el inventario"""
        if not self.productos:
            print("📦 El inventario está vacío.")
        else:
            print("📋 Productos en inventario:")
            for p in self.productos:
                print(p)
