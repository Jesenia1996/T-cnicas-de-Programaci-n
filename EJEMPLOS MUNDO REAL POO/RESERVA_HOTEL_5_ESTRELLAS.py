# Clase Habitacion representa cada habitación del hotel
class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero              # Número de habitación
        self.tipo = tipo                  # Tipo: Individual, Doble, Suite
        self.precio = precio              # Precio por noche
        self.disponible = True            # Estado: disponible o reservada

    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        print(f"Habitación {self.numero} - Tipo: {self.tipo} - Precio: ${self.precio} por noche - Estado: {estado}")

    def reservar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def liberar(self):
        self.disponible = True


# Clase Cliente representa a una persona que hace la reserva
class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def mostrar_info(self):
        print(f"Cliente: {self.nombre} - Cédula: {self.cedula}")


# Clase Reserva representa la reserva de una habitación por un cliente
class Reserva:
    def __init__(self, cliente, habitacion, noches):
        self.cliente = cliente
        self.habitacion = habitacion
        self.noches = noches
        self.total = self.habitacion.precio * noches

    def mostrar_detalle(self):
        print(f"\n--- Detalle de la Reserva ---")
        self.cliente.mostrar_info()
        print(f"Habitación N° {self.habitacion.numero} - Tipo: {self.habitacion.tipo}")
        print(f"Noches: {self.noches} - Total a pagar: ${self.total}")


# Clase Hotel maneja el conjunto de habitaciones y reservas
class Hotel:
    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []
        self.reservas = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def mostrar_habitaciones(self):
        print(f"\n--- Habitaciones del Hotel {self.nombre} ---")
        for hab in self.habitaciones:
            hab.mostrar_info()

    def reservar_habitacion(self, cedula, nombre, tipo_habitacion, noches):
        for hab in self.habitaciones:
            if hab.tipo == tipo_habitacion and hab.disponible:
                cliente = Cliente(nombre, cedula)
                if hab.reservar():
                    reserva = Reserva(cliente, hab, noches)
                    self.reservas.append(reserva)
                    print("\n¡Reserva realizada con éxito!")
                    reserva.mostrar_detalle()
                    return
        print("\nNo hay habitaciones disponibles del tipo solicitado.")

    def mostrar_reservas(self):
        print(f"\n--- Reservas en el Hotel {self.nombre} ---")
        if not self.reservas:
            print("No hay reservas registradas.")
        for reserva in self.reservas:
            reserva.mostrar_detalle()


# Bloque principal para probar el sistema
if __name__ == "__main__":
    # Crear hotel
    hotel = Hotel("Hotel Estrella de Oro *****")

    # Agregar habitaciones
    hotel.agregar_habitacion(Habitacion(101, "Individual", 80))
    hotel.agregar_habitacion(Habitacion(102, "Doble", 120))
    hotel.agregar_habitacion(Habitacion(103, "Suite", 250))
    hotel.agregar_habitacion(Habitacion(104, "Doble", 120))
    hotel.agregar_habitacion(Habitacion(105, "Suite", 250))

    # Mostrar habitaciones disponibles
    hotel.mostrar_habitaciones()

    # Realizar reservas
    hotel.reservar_habitacion("1102345678", "Maite Solis", "Suite", 3)
    hotel.reservar_habitacion("1309276812", "Julio Vera", "Doble", 2)

    # Intentar reservar una habitación no disponible
    hotel.reservar_habitacion("0705632568", "Julio Vera", "Suite", 1)

    # Mostrar habitaciones después de las reservas
    hotel.mostrar_habitaciones()

    # Mostrar todas las reservas
    hotel.mostrar_reservas()
