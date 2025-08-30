from INVENTARIO import Inventario
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
      #La opcion 1 es para gregar producto
        if opcion == "1":
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")
       #Permite validar que el precio sea un número decimal
            try:
                cantidad = int(input("Cantidad (solo número): "))
                precio = float(input("Precio: "))
            except ValueError:
                print("Error: cantidad debe ser entero y el precio debe ser un número decimal.")
                continue

            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)
    #Opcion 2 la uso para eliminar un producto que no lo quiera ya en la lista
        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)
    #Opcion 3 es para actualizar un producto
        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ")
    #Me permite dejar vacio si no deseo cambiar algo
            cantidad_str = input("Nueva cantidad (dejar vacío si no cambia): ")
            cantidad = int(cantidad_str) if cantidad_str else None

            precio_str = input("Nuevo precio (dejar vacío si no cambia): ")
            precio = float(precio_str) if precio_str else None

            inventario.actualizar_producto(id_producto, cantidad, precio)
    #Opcion 4 me ayuda a buscar un producto
        elif opcion == "4":
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)
    #Opcion 5 me permite mostrar lo que tengo en inventario
        elif opcion == "5":
            inventario.mostrar_productos()
    #Opción 6 me permite salir
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
    #En caso de ser necesario que arroje al opcion inválida
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
