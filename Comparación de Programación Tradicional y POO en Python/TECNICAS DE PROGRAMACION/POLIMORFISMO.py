class Ave:
    def hablar(self):
        print("Pío pío")

class Loro(Ave):
    def hablar(self):
        print("¡Hola!")

def hacer_hablar(ave):
    ave.hablar()

# Uso
hacer_hablar(Ave())
hacer_hablar(Loro())
