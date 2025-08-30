class CuentaBancaria:
    def __init__(self, saldo):
        self.__saldo = saldo  # Atributo privado

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto

    def obtener_saldo(self):
        return self.__saldo

# Uso
cuenta = CuentaBancaria(100)
cuenta.depositar(50)
print(cuenta.obtener_saldo())  # 150

