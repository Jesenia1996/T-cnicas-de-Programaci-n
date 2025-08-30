# Programa: Gestión de una Persona, viaje y su Mascota

# Clase Persona
class Persona:
    def __init__(self, nombre, edad, mascota, viaje):
        self.nombre = nombre
        self.edad = edad
        self.mascota = mascota
        self.viaje = viaje
        print(f"[Persona creada] Nombre: {self.nombre}, Edad: {self.edad}")

    def presentar(self):
        print(f"Hola, mi nombre es {self.nombre}, tengo {self.edad} años.")
        self.mascota.mostrar_info()
        self.viaje.detalles_viaje()

    def __del__(self):
        print(f"[Persona eliminada] {self.nombre} ha sido borrado de la memoria.")


# Clase Mascota
class Mascota:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        print(f"[Mascota creada] Nombre: {self.nombre}, Tipo: {self.tipo}")

    def mostrar_info(self):
        print(f"Mi mascota se llama {self.nombre} y es un cachorro {self.tipo}.")

    def __del__(self):
        print(f"[Mascota eliminada] {self.nombre} ha sido borrada de la memoria.")


# Clase Viaje
class Viaje:
    def __init__(self, destino, duracion):
        self.destino = destino
        self.duracion = duracion
        print(f"[Viaje creado] Destino: {self.destino}, Duración: {self.duracion} días")

    def detalles_viaje(self):
        print(f"Viajará a {self.destino} durante {self.duracion} días.")

    def __del__(self):
        print(f"[Viaje finalizado] El viaje a {self.destino} ha terminado y fue eliminado.")


# Bloque principal
if __name__ == "__main__":
    # Crear una mascota
    mi_mascota = Mascota("Samanuel", "perro")

    # Crear un viaje a Galápagos
    viaje_galapagos = Viaje("Islas Galápagos", 15)

    # Crear una persona con su mascota y su viaje
    persona1 = Persona("Jhoel", 21, mi_mascota, viaje_galapagos)

    # Presentar a la persona
    persona1.presentar()

    # Eliminar objetos (para demostrar los destructores)
    del persona1
    del viaje_galapagos
    del mi_mascota
