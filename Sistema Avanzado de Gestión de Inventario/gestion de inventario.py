"""
Sistema avanzado de gestión de inventario con ID manual.
- POO: Clase Producto, Clase Inventario
- Uso de colecciones: dict, list, set, tuple
- Persistencia en JSON
- Menú interactivo en consola
"""

import json
from typing import Dict, List, Tuple, Optional, Set

DATA_FILENAME = "inventory.json"


class Producto:
    """
    Representa un producto del inventario.
    Atributos:
        id: str (único)
        nombre: str
        cantidad: int
        precio: float
    """

    def __init__(self, id_: str, nombre: str, cantidad: int, precio: float):
        self.id: str = id_
        self.nombre: str = nombre
        self.cantidad: int = int(cantidad)
        self.precio: float = float(precio)

    # Métodos getters y setters
    def get_id(self) -> str:
        return self.id

    def get_nombre(self) -> str:
        return self.nombre

    def set_nombre(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre

    def get_cantidad(self) -> int:
        return self.cantidad

    def set_cantidad(self, nueva_cantidad: int):
        self.cantidad = int(nueva_cantidad)

    def get_precio(self) -> float:
        return self.precio

    def set_precio(self, nuevo_precio: float):
        self.precio = float(nuevo_precio)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
        }

    @staticmethod
    def from_dict(d: Dict) -> "Producto":
        return Producto(id_=d["id"], nombre=d["nombre"], cantidad=d["cantidad"], precio=d["precio"])

    def __repr__(self) -> str:
        return f"Producto(ID={self.id}, Nombre={self.nombre}, Cantidad={self.cantidad}, Precio={self.precio:.2f})"


class Inventario:
    """
    Gestiona una colección de productos.
    Usa un diccionario {id: Producto} para acceso rápido.
    """

    def __init__(self):
        self._productos: Dict[str, Producto] = {}

    # CRUD
    def agregar_producto(self, producto: Producto) -> bool:
        if producto.get_id() in self._productos:
            return False
        self._productos[producto.get_id()] = producto
        return True

    def eliminar_producto(self, id_producto: str) -> bool:
        if id_producto in self._productos:
            del self._productos[id_producto]
            return True
        return False

    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> bool:
        if id_producto in self._productos:
            self._productos[id_producto].set_cantidad(nueva_cantidad)
            return True
        return False

    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> bool:
        if id_producto in self._productos:
            self._productos[id_producto].set_precio(nuevo_precio)
            return True
        return False

    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        termino = termino.lower().strip()
        return [p for p in self._productos.values() if termino in p.get_nombre().lower()]

    def mostrar_todos(self) -> List[Tuple[str, str, int, float]]:
        return [(p.get_id(), p.get_nombre(), p.get_cantidad(), p.get_precio()) for p in self._productos.values()]

    def nombres_unicos(self) -> Set[str]:
        return {p.get_nombre().lower() for p in self._productos.values()}

    def productos_por_rango_precio(self, minimo: float, maximo: float) -> List[Producto]:
        return [p for p in self._productos.values() if minimo <= p.get_precio() <= maximo]

    # Persistencia
    def guardar_a_archivo(self, filename: str = DATA_FILENAME) -> None:
        lista_dicts = [p.to_dict() for p in self._productos.values()]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(lista_dicts, f, ensure_ascii=False, indent=4)

    def cargar_desde_archivo(self, filename: str = DATA_FILENAME) -> None:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lista = json.load(f)
            self._productos = {item["id"]: Producto.from_dict(item) for item in lista}
        except FileNotFoundError:
            self._productos = {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Archivo {filename} contiene JSON inválido: {e}")

    def obtener_producto(self, id_producto: str) -> Optional[Producto]:
        return self._productos.get(id_producto)

    def cantidad_total_items(self) -> int:
        return sum(p.get_cantidad() for p in self._productos.values())


# ----- Interfaz de consola -----
def mostrar_menu():
    print("\n--- MENÚ INVENTARIO ---")
    print("1) Agregar producto")
    print("2) Eliminar producto por ID")
    print("3) Actualizar cantidad")
    print("4) Actualizar precio")
    print("5) Buscar por nombre")
    print("6) Mostrar todos")
    print("7) Guardar inventario")
    print("8) Cargar inventario")
    print("9) Estadísticas")
    print("0) Salir")


def pedir_producto_por_input() -> Producto:
    id_manual = input("ID del producto (único): ").strip()
    nombre = input("Nombre del producto: ").strip()
    cantidad = int(input("Cantidad: ").strip())
    precio = float(input("Precio: ").strip())
    return Producto(id_=id_manual, nombre=nombre, cantidad=cantidad, precio=precio)


def main():
    inv = Inventario()
    try:
        inv.cargar_desde_archivo()
        print(f"Inventario cargado. Productos: {len(inv.mostrar_todos())}")
    except Exception as e:
        print(f"No se pudo cargar inventario: {e}")

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            try:
                p = pedir_producto_por_input()
                if inv.agregar_producto(p):
                    print(f"Producto agregado con ID: {p.get_id()}")
                else:
                    print("Error: Ya existe un producto con ese ID.")
            except Exception as e:
                print(f"Error al agregar producto: {e}")

        elif opcion == "2":
            id_to_remove = input("ID del producto a eliminar: ").strip()
            if inv.eliminar_producto(id_to_remove):
                print("Producto eliminado.")
            else:
                print("ID no encontrado.")

        elif opcion == "3":
            id_to_update = input("ID para actualizar cantidad: ").strip()
            try:
                nueva_cant = int(input("Nueva cantidad: ").strip())
                if inv.actualizar_cantidad(id_to_update, nueva_cant):
                    print("Cantidad actualizada.")
                else:
                    print("ID no encontrado.")
            except ValueError:
                print("Cantidad inválida.")

        elif opcion == "4":
            id_to_update = input("ID para actualizar precio: ").strip()
            try:
                nuevo_precio = float(input("Nuevo precio: ").strip())
                if inv.actualizar_precio(id_to_update, nuevo_precio):
                    print("Precio actualizado.")
                else:
                    print("ID no encontrado.")
            except ValueError:
                print("Precio inválido.")

        elif opcion == "5":
            termino = input("Buscar por nombre: ").strip()
            resultados = inv.buscar_por_nombre(termino)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos.")

        elif opcion == "6":
            todos = inv.mostrar_todos()
            if todos:
                for id_, nombre, cant, precio in todos:
                    print(f"ID: {id_} | Nombre: {nombre} | Cantidad: {cant} | Precio: {precio:.2f}")
            else:
                print("Inventario vacío.")

        elif opcion == "7":
            try:
                inv.guardar_a_archivo()
                print("Inventario guardado.")
            except Exception as e:
                print(f"Error al guardar: {e}")

        elif opcion == "8":
            try:
                inv.cargar_desde_archivo()
                print("Inventario cargado.")
            except Exception as e:
                print(f"Error al cargar: {e}")

        elif opcion == "9":
            print(f"Productos distintos: {len(inv.mostrar_todos())}")
            print(f"Total unidades: {inv.cantidad_total_items()}")
            print(f"Nombres únicos: {inv.nombres_unicos()}")

        elif opcion == "0":
            if input("¿Guardar antes de salir? (s/n): ").strip().lower() == "s":
                inv.guardar_a_archivo()
                print("Inventario guardado.")
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
