class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        print(f"Hola, soy {self.nombre}")

class Estudiante(Persona):
    def estudiar(self):
        print(f"{self.nombre} está estudiando.")

# Uso
e = Estudiante("Ana")
e.saludar()
e.estudiar()
