"""
Sistema de Gestión de Inventarios (archivo único ejecutable)

Este archivo contiene:
- Clase Producto
- Clase Inventario
- Interfaz de consola (menú interactivo)

Instrucciones:
- Puedes ejecutar este archivo tal cual en PyCharm (Run).
- Si prefieres organizar en archivos separados: extrae la clase Producto a product.py,
  la clase Inventario a inventory.py y deja la interfaz en main.py, importando las clases.

Diseño y supuestos:
- El ID de producto es un valor que identifica de forma única al producto (str recomendado).
- Búsqueda por nombre: coincidente por subcadena (case-insensitive).
- El inventario se mantiene en memoria (lista). No se persisten datos en disco en esta versión.

Comentarios: el código está comentado en español para facilitar su revisión y mantenimiento.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import sys


@dataclass
class Producto:
    """Representa un producto del inventario."""
    id: str
    nombre: str
    cantidad: int
    precio: float

    def __post_init__(self):
        # Validación básica de los atributos
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")

    # Getters y setters (opcional con dataclass, pero añadimos métodos para claridad)
    def get_id(self) -> str:
        return self.id

    def get_nombre(self) -> str:
        return self.nombre

    def get_cantidad(self) -> int:
        return self.cantidad

    def get_precio(self) -> float:
        return self.precio

    def set_nombre(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre

    def set_cantidad(self, nueva_cantidad: int):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio: float):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.precio = nuevo_precio


class Inventario:
    """Gestión de productos mediante una lista interna."""

    def __init__(self):
        # Lista que contiene instancias de Producto
        self.productos: List[Producto] = []

    def _buscar_indice_por_id(self, product_id: str) -> Optional[int]:
        """Devuelve el índice del producto con el ID dado o None si no existe."""
        for i, prod in enumerate(self.productos):
            if prod.id == product_id:
                return i
        return None

    def anadir_producto(self, producto: Producto) -> bool:
        """Añade un producto al inventario. Si el ID ya existe, no lo añade y devuelve False."""
        if self._buscar_indice_por_id(producto.id) is not None:
            # ID duplicado
            return False
        self.productos.append(producto)
        return True

    def eliminar_por_id(self, product_id: str) -> bool:
        """Elimina un producto por ID. Devuelve True si se eliminó, False si no se encontró."""
        indice = self._buscar_indice_por_id(product_id)
        if indice is None:
            return False
        del self.productos[indice]
        return True

    def actualizar_por_id(self, product_id: str, nueva_cantidad: Optional[int] = None, nuevo_precio: Optional[float] = None) -> bool:
        """Actualiza cantidad y/o precio del producto identificado por ID.

        Pasa None para los campos que no quieras cambiar.
        Devuelve True si se actualizó, False si no se encontró el producto.
        """
        indice = self._buscar_indice_por_id(product_id)
        if indice is None:
            return False
        prod = self.productos[indice]
        if nueva_cantidad is not None:
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            prod.set_cantidad(nueva_cantidad)
        if nuevo_precio is not None:
            if nuevo_precio < 0:
                raise ValueError("El precio no puede ser negativo")
            prod.set_precio(nuevo_precio)
        return True

    def buscar_por_nombre(self, nombre_query: str) -> List[Producto]:
        """Busca productos cuyo nombre contiene la subcadena nombre_query (case-insensitive)."""
        q = nombre_query.strip().lower()
        resultados = [p for p in self.productos if q in p.nombre.lower()]
        return resultados

    def listar_todos(self) -> List[Producto]:
        """Devuelve la lista completa de productos (copia superficial)."""
        return list(self.productos)


# ---------- Interfaz de consola ----------

def mostrar_menu():
    print("\n--- MENÚ DE INVENTARIO ---")
    print("1. Añadir producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar cantidad/precio por ID")
    print("4. Buscar productos por nombre")
    print("5. Mostrar todos los productos")
    print("6. Salir")


def leer_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        # Permitir salir con Ctrl+C o Ctrl+D
        print("\nInterrupción detectada. Saliendo...")
        sys.exit(0)


def crear_producto_desde_input() -> Producto:
    """Solicita datos al usuario y crea una instancia de Producto (lanza excepciones si datos inválidos)."""
    id = leer_input("ID (único): ").strip()
    nombre = leer_input("Nombre: ").strip()
    # Validar entero para cantidad
    try:
        cantidad_str = leer_input("Cantidad (entero): ").strip()
        cantidad = int(cantidad_str)
    except ValueError:
        raise ValueError("Cantidad debe ser un número entero")
    # Validar float para precio
    try:
        precio_str = leer_input("Precio (p. ej. 12.50): ").strip()
        precio = float(precio_str)
    except ValueError:
        raise ValueError("Precio debe ser un número (usar punto decimal si aplica)")

    return Producto(id=id, nombre=nombre, cantidad=cantidad, precio=precio)


def imprimir_producto(prod: Producto):
    print(f"ID: {prod.id} | Nombre: {prod.nombre} | Cantidad: {prod.cantidad} | Precio: {prod.precio:.2f}")


def main():
    inv = Inventario()

    # Datos de ejemplo para facilitar pruebas (puedes comentar estas líneas si lo deseas)
    inv.anadir_producto(Producto(id="P001", nombre="Lapicero azul", cantidad=100, precio=0.50))
    inv.anadir_producto(Producto(id="P002", nombre="Cuaderno A4", cantidad=50, precio=2.75))
    inv.anadir_producto(Producto(id="P003", nombre="Regla 30cm", cantidad=30, precio=1.20))

    while True:
        mostrar_menu()
        opcion = leer_input("Elige una opción (1-6): ").strip()

        if opcion == "1":
            try:
                nuevo = crear_producto_desde_input()
                ok = inv.anadir_producto(nuevo)
                if not ok:
                    print("No se pudo añadir: ya existe un producto con ese ID.")
                else:
                    print("Producto añadido correctamente.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "2":
            pid = leer_input("ID del producto a eliminar: ").strip()
            ok = inv.eliminar_por_id(pid)
            if ok:
                print("Producto eliminado correctamente.")
            else:
                print("No se encontró un producto con ese ID.")

        elif opcion == "3":
            pid = leer_input("ID del producto a actualizar: ").strip()
            # Preguntar si quiere cambiar cantidad y/o precio
            cambio_cantidad = leer_input("¿Cambiar cantidad? (s/n): ").strip().lower()
            nueva_cantidad = None
            if cambio_cantidad == "s":
                try:
                    nueva_cantidad = int(leer_input("Nueva cantidad (entero): ").strip())
                except ValueError:
                    print("Cantidad inválida: operación cancelada.")
                    continue
            cambio_precio = leer_input("¿Cambiar precio? (s/n): ").strip().lower()
            nuevo_precio = None
            if cambio_precio == "s":
                try:
                    nuevo_precio = float(leer_input("Nuevo precio: ").strip())
                except ValueError:
                    print("Precio inválido: operación cancelada.")
                    continue
            try:
                ok = inv.actualizar_por_id(pid, nueva_cantidad=nueva_cantidad, nuevo_precio=nuevo_precio)
                if ok:
                    print("Producto actualizado correctamente.")
                else:
                    print("No se encontró un producto con ese ID.")
            except Exception as e:
                print(f"Error al actualizar: {e}")

        elif opcion == "4":
            q = leer_input("Nombre (o parte del nombre) a buscar: ").strip()
            resultados = inv.buscar_por_nombre(q)
            if not resultados:
                print("No se encontraron productos que coincidan.")
            else:
                print(f"Se encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    imprimir_producto(p)

        elif opcion == "5":
            todos = inv.listar_todos()
            if not todos:
                print("El inventario está vacío.")
            else:
                print(f"Inventario ({len(todos)} productos):")
                for p in todos:
                    imprimir_producto(p)

        elif opcion == "6":
            print("Saliendo. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Elige 1-6.")


if __name__ == "__main__":
    main()


from inventario import Inventario
from producto import Producto

def menu():
    inventario = Inventario()
    while True:
        print("\n== SISTEMA DE GESTIÓN DE INVENTARIO ==")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")

            try:
                cantidad = int(input("Cantidad (solo número): "))
            except ValueError:
                print("Error: la cantidad debe ser un número entero.")
                continue

            try:
                precio = float(input("Precio: "))
            except ValueError:
                print("Error: el precio debe ser un número decimal.")
                continue

            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)

        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ")

            cantidad_str = input("Nueva cantidad (dejar vacío si no cambia): ")
            cantidad = int(cantidad_str) if cantidad_str else None

            precio_str = input("Nuevo precio (dejar vacío si no cambia): ")
            precio = float(precio_str) if precio_str else None

            inventario.actualizar_producto(id_producto, cantidad, precio)

        elif opcion == "4":
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()


    # CLASE PRODUCTO
    class Producto:
        def __init__(self, id_producto, nombre, cantidad, precio):
            self.id_producto = id_producto
            self.nombre = nombre
            self.cantidad = cantidad
            self.precio = precio

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
            return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"
