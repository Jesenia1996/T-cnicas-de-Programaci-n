import os

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    print(f"\nIntentando abrir: {ruta_script_absoluta}")
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            print("\n--- Resultado de la ejecución ---\n")
            exec(codigo, globals())
    except FileNotFoundError:
        print(" El archivo no se encontró.")
    except Exception as e:
        print(f"⚠ Ocurrió un error al leer o ejecutar el archivo: {e}")

def mostrar_menu():
    # Subimos dos niveles hasta el directorio raíz del proyecto
    ruta_base = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))

    opciones = {
        '1': ['Comparacion de Programacion Tradicional y POO en Python'
              '1.TAREA PROGRAMACION TRADICIONAL.py/'
              '2.TAREA POO.py'
              ],
        '2': ['Conceptos de POO en PYthon'
              'Clases, objetos, herencia, encamsulamiento y polimorfismo.py'
              ],
        '3': ['Constructores y Destructores'
              'Implementacios de constructores y destructores en python.py'
              ],
        '4': ['EJEMPLOS MUNDO REAL POO'
              'RESERVA_HOTEL_5_ESTRELLAS.py'
              'TIPOS_DE_DATOS_IDENTIFICADORES.py'
              ],
        '5': ['HILOS DE PROCESOS'
              'hilos_python.py'
              ],
        '6': ['TECNICAS DE PROGRAMACION'
              'ABSTRACION.py'
              'ENCAPSULACION.py'
              'HERENCIA.py'
              'POLIMORFISMO.py'
              ]
    }

    while True:
        print("\n Menú Principal - Dashboard")
        for key, value in opciones.items():
            label = f"{len(value)} archivos" if isinstance(value, list) else value
            print(f"{key} - {label}")
        print("0 - Salir")

        eleccion = input("Elige una opción para ver su(s) script(s) o '0' para salir: ")
        if eleccion == '0':
            print("¡Hasta luego!")
            break
        elif eleccion in opciones:
            rutas = opciones[eleccion]
            if isinstance(rutas, list):
                for ruta_relativa in rutas:
                    ruta_script = os.path.join(ruta_base, ruta_relativa)
                    mostrar_codigo(ruta_script)
            else:
                ruta_script = os.path.join(ruta_base, rutas)
                mostrar_codigo(ruta_script)
        else:
            print(" Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
