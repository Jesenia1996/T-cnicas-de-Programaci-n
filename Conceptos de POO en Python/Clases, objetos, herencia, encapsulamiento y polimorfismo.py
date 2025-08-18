# Aplicación de Programación Orientada a Objetos con Persona, Moto y Mascota

# Clase base: Persona
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre              # Atributo público
        self.__edad = edad                # Atributo privado (encapsulado)

    def mostrar_info(self):
        print(f"Persona: {self.nombre}, Edad: {self.__edad}")

    # Getter y setter para el atributo privado __edad
    def get_edad(self):
        return self.__edad

    def set_edad(self, nueva_edad):
        if nueva_edad > 0:
            self.__edad = nueva_edad
        else:
            print("Edad no válida.")

# Clase Moto (no hereda de Persona, es una clase independiente)
class Moto:
    def __init__(self, marca, cilindrada):
        self.marca = marca
        self.__cilindrada = cilindrada    # Atributo privado

    def mostrar_info(self):
        print(f"Moto: {self.marca}, Cilindrada: {self.__cilindrada}cc")

    def get_cilindrada(self):
        return self.__cilindrada

    def set_cilindrada(self, nueva_cilindrada):
        if nueva_cilindrada > 0:
            self.__cilindrada = nueva_cilindrada
        else:
            print("Cilindrada no válida.")

# Clase Mascota (derivada de Persona) - HERENCIA
class Mascota(Persona):
    def __init__(self, nombre, edad, tipo):
        super().__init__(nombre, edad)
        self.tipo = tipo  # perro, gato, etc.

    # POLIMORFISMO: sobrescribimos mostrar_info()
    def mostrar_info(self):
        print(f"Mascota: {self.nombre}, Edad: {self.get_edad()}, Tipo: {self.tipo}")

# Función que demuestra polimorfismo
def mostrar_detalle(objeto):
    objeto.mostrar_info()

# MAIN
if __name__ == "__main__":
    # Instancias de las clases
    persona1 = Persona("Marisol", 28)
    moto1 = Moto("Kawasaki Ninja", 649)
    mascota1 = Mascota("Mochi", 1, "Gata")

    print("\n--- Mostrar Información de Objetos ---")
    persona1.mostrar_info()
    moto1.mostrar_info()
    mascota1.mostrar_info()

    print("\n--- Encapsulación: Cambiar Edad y Cilindrada ---")
    persona1.set_edad(35)
    moto1.set_cilindrada(200)
    print(f"Edad actualizada: {persona1.get_edad()}")
    print(f"Cilindrada actualizada: {moto1.get_cilindrada()}cc")

    print("\n--- Polimorfismo con mostrar_detalle() ---")
    for obj in [persona1, moto1, mascota1]:
        mostrar_detalle(obj)
