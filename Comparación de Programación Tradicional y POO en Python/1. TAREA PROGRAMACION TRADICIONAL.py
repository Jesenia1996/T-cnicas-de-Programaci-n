# Programa para calcular el promedio semanal del clima utilizando la Programación TradicionalMore actions

def ingresar_temperaturas():
    """Solicita al usuario las temperaturas de los 7 días de las semana"""
    temperaturas = []
    dias_semana = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    for dia in dias_semana:
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """Calcula el promedio de una lista de temperaturas."""
    return round(sum(temperaturas) / len(temperaturas),2)

def main():
    print("== PROMEDIO SEMANAL DEL CLIMA ==")
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

# Ejecutar el programa
if __name__ == "__main__":
    main()