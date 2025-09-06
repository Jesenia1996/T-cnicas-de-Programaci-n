import json
import os

# ----------------------------
# CLASE LIBRO
# ----------------------------
class Libro:
    """
    Representa un libro de la biblioteca.
    Atributos:
        info (tuple): Tupla (titulo, autor) que no cambia.
        categoria (str): Categoría del libro.
        isbn (str): Identificador único del libro.
    """
    def __init__(self, titulo, autor, categoria, isbn):
        self.info = (titulo, autor)  # Tupla para título y autor (inmutable)
        self.categoria = categoria
        self.isbn = isbn

    def to_dict(self):
        """
        Convierte el libro a diccionario para guardar en JSON.
        """
        return {
            "titulo": self.info[0],
            "autor": self.info[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

# ----------------------------
# CLASE USUARIO
# ----------------------------
class Usuario:
    """
    Representa un usuario de la biblioteca.
    Atributos:
        nombre (str): Nombre del usuario.
        id_usuario (str): ID único del usuario.
    """
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario

    def to_dict(self):
        """
        Convierte el usuario a diccionario para guardar en JSON.
        """
        return {
            "nombre": self.nombre,
            "id_usuario": self.id_usuario
        }

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------
def crear_libro_desde_dict(data):
    """
    Crea un objeto Libro a partir de un diccionario.
    """
    return Libro(data["titulo"], data["autor"], data["categoria"], data["isbn"])

def crear_usuario_desde_dict(data):
    """
    Crea un objeto Usuario a partir de un diccionario.
    """
    return Usuario(data["nombre"], data["id_usuario"])

# ----------------------------
# CLASE BIBLIOTECA
# ----------------------------
class Biblioteca:
    """
    Gestiona libros, usuarios y préstamos de la biblioteca.
    Atributos:
        libros (dict): ISBN -> Libro
        usuarios (dict): ID -> Usuario
        prestamos (dict): ID -> [ISBN] (libros prestados por usuario)
    """
    def __init__(self):
        self.libros = {}       # Todos los libros de la biblioteca
        self.usuarios = {}     # Todos los usuarios registrados
        self.prestamos = {}    # Libros prestados por usuario
        self.cargar_datos()    # Carga los datos desde los JSON al iniciar

    # ------------------------
    # GUARDAR Y CARGAR DATOS CON TRY-EXCEPT
    # ------------------------
    def guardar_datos(self):
        """
        Guarda libros, usuarios y préstamos en archivos JSON.
        """
        try:
            with open("libros.json", "w") as f:
                json.dump({isbn: libro.to_dict() for isbn, libro in self.libros.items()}, f, indent=4)
            with open("usuarios.json", "w") as f:
                json.dump({uid: user.to_dict() for uid, user in self.usuarios.items()}, f, indent=4)
            with open("prestamos.json", "w") as f:
                json.dump(self.prestamos, f, indent=4)
        except Exception as e:
            print(f" Error al guardar los datos: {e}")

    def cargar_datos(self):
        """
        Carga libros, usuarios y préstamos desde archivos JSON si existen.
        """
        # Cargar libros
        try:
            if os.path.exists("libros.json"):
                with open("libros.json", "r") as f:
                    libros_dict = json.load(f)
                    for isbn, datos in libros_dict.items():
                        self.libros[isbn] = crear_libro_desde_dict(datos)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f" Error al cargar libros: {e}")

        # Cargar usuarios
        try:
            if os.path.exists("usuarios.json"):
                with open("usuarios.json", "r") as f:
                    usuarios_dict = json.load(f)
                    for uid, datos in usuarios_dict.items():
                        self.usuarios[uid] = crear_usuario_desde_dict(datos)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f" Error al cargar usuarios: {e}")

        # Cargar préstamos
        try:
            if os.path.exists("prestamos.json"):
                with open("prestamos.json", "r") as f:
                    self.prestamos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f" Error al cargar préstamos: {e}")

    # ------------------------
    # MÉTODOS DE LIBROS
    # ------------------------
    def agregar_libro(self, libro):
        """
        Agrega un libro nuevo a la biblioteca.
        """
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(" Libro agregado.")
            self.guardar_datos()
        else:
            print(" Libro ya existe.")

    def quitar_libro(self, isbn):
        """
        Elimina un libro de la biblioteca.
        No permite eliminar si está prestado.
        """
        try:
            prestado = any(isbn in libros for libros in self.prestamos.values())
            if isbn in self.libros:
                if prestado:
                    print(" No se puede eliminar. El libro está prestado.")
                else:
                    del self.libros[isbn]
                    print(" Libro eliminado.")
                    self.guardar_datos()
            else:
                print(" Libro no encontrado.")
        except Exception as e:
            print(f" Error al eliminar libro: {e}")

    def buscar_libros(self, criterio, valor):
        """
        Busca libros por título, autor o categoría.
        """
        try:
            encontrados = []
            for libro in self.libros.values():
                if criterio == "titulo" and valor.lower() in libro.info[0].lower():
                    encontrados.append(libro)
                elif criterio == "autor" and valor.lower() in libro.info[1].lower():
                    encontrados.append(libro)
                elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
                    encontrados.append(libro)
            if encontrados:
                print(" Libros encontrados:")
                for l in encontrados:
                    print(f"- {l.info[0]} de {l.info[1]} [{l.categoria}] - ISBN: {l.isbn}")
            else:
                print(" No se encontraron libros.")
        except Exception as e:
            print(f" Error al buscar libros: {e}")

    def listar_libros(self):
        """
        Lista todos los libros de la biblioteca.
        """
        try:
            if self.libros:
                print(" Libros en la biblioteca:")
                for l in self.libros.values():
                    print(f"- {l.info[0]} de {l.info[1]} [{l.categoria}] - ISBN: {l.isbn}")
            else:
                print(" No hay libros registrados.")
        except Exception as e:
            print(f" Error al listar libros: {e}")

    # ------------------------
    # MÉTODOS DE USUARIOS
    # ------------------------
    def registrar_usuario(self, usuario):
        """
        Registra un nuevo usuario.
        """
        try:
            if usuario.id_usuario in self.usuarios:
                print(" ID de usuario ya existe.")
            else:
                self.usuarios[usuario.id_usuario] = usuario
                print(" Usuario registrado.")
                self.guardar_datos()
        except Exception as e:
            print(f" Error al registrar usuario: {e}")

    def dar_baja_usuario(self, id_usuario):
        """
        Elimina un usuario solo si no tiene libros prestados.
        """
        try:
            if id_usuario in self.usuarios:
                if id_usuario in self.prestamos and self.prestamos[id_usuario]:
                    print(" Usuario tiene libros prestados. No se puede eliminar.")
                else:
                    self.usuarios.pop(id_usuario)
                    self.prestamos.pop(id_usuario, None)
                    print("🗑 Usuario eliminado.")
                    self.guardar_datos()
            else:
                print(" Usuario no encontrado.")
        except Exception as e:
            print(f" Error al dar de baja usuario: {e}")

    def listar_usuarios(self):
        """
        Lista todos los usuarios registrados.
        """
        try:
            if self.usuarios:
                print(" Usuarios registrados:")
                for u in self.usuarios.values():
                    print(f"- {u.nombre} | ID: {u.id_usuario}")
            else:
                print(" No hay usuarios registrados.")
        except Exception as e:
            print(f" Error al listar usuarios: {e}")

    # ------------------------
    # MÉTODOS DE PRÉSTAMOS
    # ------------------------
    def prestar_libro(self, id_usuario, isbn):
        """
        Presta un libro a un usuario.
        """
        try:
            if id_usuario not in self.usuarios:
                print(" Usuario no encontrado.")
            elif isbn not in self.libros:
                print(" Libro no encontrado.")
            else:
                if any(isbn in libros for libros in self.prestamos.values()):
                    print(" El libro ya está prestado.")
                else:
                    self.prestamos.setdefault(id_usuario, []).append(isbn)
                    print(" Libro prestado.")
                    self.guardar_datos()
        except Exception as e:
            print(f" Error al prestar libro: {e}")

    def devolver_libro(self, id_usuario, isbn):
        """
        Devuelve un libro prestado por un usuario.
        """
        try:
            if id_usuario in self.usuarios:
                if id_usuario in self.prestamos and isbn in self.prestamos[id_usuario]:
                    self.prestamos[id_usuario].remove(isbn)
                    print(" Libro devuelto.")
                    self.guardar_datos()
                else:
                    print(" Este usuario no tiene prestado ese libro.")
            else:
                print(" Usuario no encontrado.")
        except Exception as e:
            print(f" Error al devolver libro: {e}")

    def listar_libros_prestados_usuario(self, id_usuario):
        """
        Lista los libros prestados a un usuario específico.
        """
        try:
            if id_usuario in self.usuarios:
                libros_prestados = self.prestamos.get(id_usuario, [])
                if libros_prestados:
                    print(f" Libros prestados a {self.usuarios[id_usuario].nombre}:")
                    for isbn in libros_prestados:
                        libro = self.libros.get(isbn)
                        if libro:
                            print(f"- {libro.info[0]} de {libro.info[1]} - ISBN: {isbn}")
                        else:
                            print(f"- ISBN: {isbn}")
                else:
                    print(" Este usuario no tiene libros prestados.")
            else:
                print(" Usuario no encontrado.")
        except Exception as e:
            print(f" Error al listar libros prestados de usuario: {e}")

    def listar_libros_prestados_general(self):
        """
        Lista todos los libros actualmente prestados en la biblioteca.
        """
        try:
            any_prestado = False
            for id_usuario, lista in self.prestamos.items():
                if lista:
                    any_prestado = True
                    usuario = self.usuarios.get(id_usuario)
                    for isbn in lista:
                        libro = self.libros.get(isbn)
                        if libro:
                            print(f"- {libro.info[0]} de {libro.info[1]} prestado a {usuario.nombre}")
            if not any_prestado:
                print(" No hay libros prestados actualmente.")
        except Exception as e:
            print(f" Error al listar libros prestados generales: {e}")

# ----------------------------
# MENÚ PRINCIPAL
# ----------------------------
def menu_biblioteca():
    """
    Menú interactivo para la gestión de la biblioteca digital.
    Incluye validaciones y manejo de errores.
    """
    biblioteca = Biblioteca()
    while True:
        print("\n----- MENÚ BIBLIOTECA DIGITAL -----")
        print("1. Agregar libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libros")
        print("8. Listar libros prestados de un usuario")
        print("9. Listar todos los usuarios")
        print("10. Listar todos los libros")
        print("11. Listar todos los libros prestados (general)")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()

        try:
            if opcion == "1":
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                categoria = input("Categoría: ").strip()
                isbn = input("ISBN: ").strip()
                if titulo and autor and categoria and isbn:
                    libro = Libro(titulo, autor, categoria, isbn)
                    biblioteca.agregar_libro(libro)
                else:
                    print(" Todos los campos son obligatorios.")

            elif opcion == "2":
                isbn = input("ISBN del libro a eliminar: ").strip()
                biblioteca.quitar_libro(isbn)

            elif opcion == "3":
                nombre = input("Nombre del usuario: ").strip()
                id_usuario = input("ID del usuario: ").strip()
                if nombre and id_usuario:
                    usuario = Usuario(nombre, id_usuario)
                    biblioteca.registrar_usuario(usuario)
                else:
                    print(" Todos los campos son obligatorios.")

            elif opcion == "4":
                id_usuario = input("ID del usuario a eliminar: ").strip()
                biblioteca.dar_baja_usuario(id_usuario)

            elif opcion == "5":
                id_usuario = input("ID del usuario: ").strip()
                isbn = input("ISBN del libro: ").strip()
                biblioteca.prestar_libro(id_usuario, isbn)

            elif opcion == "6":
                id_usuario = input("ID del usuario: ").strip()
                isbn = input("ISBN del libro a devolver: ").strip()
                biblioteca.devolver_libro(id_usuario, isbn)

            elif opcion == "7":
                criterio = input("Buscar por (titulo/autor/categoria): ").strip().lower()
                valor = input("Valor a buscar: ").strip()
                biblioteca.buscar_libros(criterio, valor)

            elif opcion == "8":
                id_usuario = input("ID del usuario: ").strip()
                biblioteca.listar_libros_prestados_usuario(id_usuario)

            elif opcion == "9":
                biblioteca.listar_usuarios()

            elif opcion == "10":
                biblioteca.listar_libros()

            elif opcion == "11":
                biblioteca.listar_libros_prestados_general()

            elif opcion == "0":
                print("Saliendo del sistema.")
                break

            else:
                print("Opción inválida. Intenta de nuevo.")
        except Exception as e:
                print(f"Ocurrió un error: {e}")

# ----------------------------
# EJECUTAR MENÚ
# ----------------------------
menu_biblioteca()