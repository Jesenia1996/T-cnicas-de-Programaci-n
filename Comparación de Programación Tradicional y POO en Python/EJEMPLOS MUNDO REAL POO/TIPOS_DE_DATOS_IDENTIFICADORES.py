# Programa: Conversor de Temperaturas
# Descripción: Este programa convierte una temperatura ingresada en grados Celsius
# a grados Fahrenheit y Kelvin. Utiliza distintos tipos de datos y estructuras claras.

def celsius_a_fahrenheit(celsius: float) -> float:
    """Convierte de Celsius a Fahrenheit"""
    return (celsius * 9/5) + 32


def celsius_a_kelvin(celsius: float) -> float:
    """Convierte de Celsius a Kelvin"""
    return celsius + 273.15


# Solicita al usuario una temperatura en Celsius
temperatura_input = input("Ingrese la temperatura en grados Celsius: ")

# Convierte la entrada a tipo float
temperatura_celsius = float(temperatura_input)

# Realiza las conversiones
temperatura_fahrenheit = celsius_a_fahrenheit(temperatura_celsius)
temperatura_kelvin = celsius_a_kelvin(temperatura_celsius)

# Verifica si la temperatura es bajo cero (booleano)
es_bajo_cero = temperatura_celsius < 0

# Imprime los resultados
print("\n=== Conversión de Temperatura ===")
print(f"Temperatura en Celsius: {temperatura_celsius} °C")
print(f"Temperatura en Fahrenheit: {temperatura_fahrenheit} °F")
print(f"Temperatura en Kelvin: {temperatura_kelvin} K")
print("¿Está bajo cero?:", "Sí ❄️" if es_bajo_cero else "No 🌞")