# Programa para calcular el Promedio Semanal del Clima Utilizando la POOMore actions
from typing import Any


# Clase principal que contiene los datos y métodos generales
class ClimaSemanal:
    def __init__(self):
        # Lista protegida: solo puede ser usada por esta clase o sus hermanos
        self._dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        # Atributo privado con doble guion bajo (encapsulado). No debe ser accedido directamente desde fuera
        self.__temperaturas = []

    #metodo público para ingresar temperaturas
    def ingresar_temperaturas(self):
        for dia in self._dias:
            temp = float(input(f"Ingrese la temperatura del día {dia}: "))
            self.__temperaturas.append(temp)

    # Metodo protegido que devuelve la lista de temperaturas (forma segura de acceder al atributo privado)
    def _obtener_temperaturas(self) -> list[Any]:
        return self.__temperaturas

# Clase hija que hereda de ClimaBase (herencia)
class ClimaPromedio(ClimaSemanal):
    # Metodo para calcular el promedio usando las temperaturas de la clase base
    def calcular_promedio(self):
        datos = self._obtener_temperaturas()  # Acceso al atributo privado a través de un metodo protegido
        if len(datos) == 0:
            return 0
        promedio = sum(datos) / len(datos)
        return round(promedio, 2)

    # Metodo para mostrar el resultado final
    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        print(f"\nEl promedio semanal de temperatura es: {promedio}°C")

# Código principal del programa
if __name__ == "__main__":
    # Creamos una instancia de la clase hija (heredada)
    clima = ClimaPromedio()
    print("== PROMEDIO SEMANAL DEL CLIMA (POO) ==")
    clima.ingresar_temperaturas()   # Metodo heredado de ClimaBase
    clima.mostrar_resultado()       # Metodo propio de ClimaPromedio
