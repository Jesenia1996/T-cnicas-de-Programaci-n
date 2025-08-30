import os
from producto import Producto

class Inventario:
    def __init__(self, archivo="inventario.txt"):
        """Constructor de inventario con almacenamiento en archivo"""
        self.productos = []
        self.archivo = archivo
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga de productos desde el archivo"""
        try:
            if not os.path.exists(self.archivo):
                open(self.archivo, "w").close()
                print("Archivo inventario.txt creado vacío.")
                return

            with open(self.archivo, "r") as f:
                lines = f.readlines()
                # Ignorar las 2 primeras líneas: encabezado y separación
                for line in lines[2:]:
                    line = line.strip()
                    if line:  # ignorar líneas vacías
                        try:
                            # Separar por espacios y quitar $
                            parts = line.split()
                            id_producto = parts[0]
                            nombre = parts[1]
                            cantidad = int(parts[2])
                            precio = float(parts[3].replace("$", ""))
                            producto = Producto(id_producto, nombre, cantidad, precio)
                            self.productos.append(producto)
                        except Exception as e:
                            print(f"Línea inválida en archivo: {line} ({e})")
            print("Inventario cargado correctamente desde archivo.")
        except PermissionError:
            print("Error: No tienes permisos para leer el archivo")

    def guardar_en_archivo(self):
        """Guardar productos en archivo con formato legible"""
        try:
            with open(self.archivo, "w") as f:
                # Encabezado
                f.write(f"{'ID':<5} {'Nombre':<15} {'Cantidad':<10} {'Precio':<10}\n")
                f.write("=" * 45 + "\n")
                # Productos
                for p in self.productos:
                    f.write(f"{p.get_id():<5} {p.get_nombre():<15} {p.get_cantidad():<10} ${p.get_precio():<10.2f}\n")
            print("Cambios guardados en inventario.txt (formato legible).")
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo")

    def agregar_producto(self, producto):
        """Añadir nuevo producto si el ID es único"""
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print("Producto ya existente.")
        else:
            self.productos.append(producto)
            self.guardar_en_archivo()
            print("Producto añadido con éxito.")

    def eliminar_producto(self, id_producto):
        """Eliminar producto por su ID."""
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                self.guardar_en_archivo()
                print("🗑️ Producto eliminado.")
                return
        print("No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualizar cantidad o precio de un producto"""
        for p in self.productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                self.guardar_en_archivo()
                print("Producto actualizado.")
                return
        print("No se encontró producto con ese ID.")

    def buscar_producto(self, nombre):
        """Buscar producto por nombre exacto"""
        encontrados = [p for p in self.productos if p.get_nombre() == nombre]
        if encontrados:
            print("\nProductos encontrados:")
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        """Mostrar productos del inventario"""
        if not self.productos:
            print("Inventario vacío.")
        else:
            print("\nLista de productos en inventario:")
            for p in self.productos:
                print(p)
