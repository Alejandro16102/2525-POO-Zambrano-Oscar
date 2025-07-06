# Programa de Programación Orientada a Objetos - Animales
# Demuestra herencia, encapsulación y polimorfismo

class Animal:
    """Clase padre que representa un animal"""

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.__edad = edad  # Atributo privado (encapsulación)

    # Método getter para acceder al atributo privado
    def get_edad(self):
        return self.__edad

    # Método setter para modificar el atributo privado
    def set_edad(self, edad):
        if edad > 0:
            self.__edad = edad

    # Método que será sobrescrito (polimorfismo)
    def hacer_sonido(self):
        return "El animal hace un sonido"

    def info(self):
        return f"{self.nombre} tiene {self.__edad} años"


class Perro(Animal):
    """Clase hija que hereda de Animal"""

    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)  # Llama al constructor de la clase padre
        self.raza = raza

    # Sobrescribe el método de la clase padre (polimorfismo)
    def hacer_sonido(self):
        return f"{self.nombre} dice: ¡Guau guau!"

    def jugar(self):
        return f"{self.nombre} está jugando con la pelota"


class Gato(Animal):
    """Clase derivada que hereda de Animal"""

    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color

    # Sobrescribe el método de la clase padre (polimorfismo)
    def hacer_sonido(self):
        return f"{self.nombre} dice: ¡Miau miau!"

    def dormir(self):
        return f"{self.nombre} está durmiendo"


# Función que demuestra polimorfismo con argumentos múltiples
def presentar_animales(*animales):
    """Función que acepta múltiples animales y muestra su información"""
    for animal in animales:
        print(f"- {animal.info()}")
        print(f"- {animal.hacer_sonido()}")
        print()


# Programa principal
if __name__ == "__main__":
    print("=== PROGRAMA DE ANIMALES - POO ===\n")

   # Crear instancias de las clases
    perro1 = Perro("Firulais", 3, "Labrador")
    gato1 = Gato("Otis", 2, "Negro")

    # Demostrar encapsulación

    print(f"Edad de {perro1.nombre}: {perro1.get_edad()} años")
    perro1.set_edad(4)
    print(f"Nueva edad de {perro1.nombre}: {perro1.get_edad()} años\n")

    # Demostrar herencia
    print("2. HERENCIA:")
    print(f"Información del perro: {perro1.info()}")
    print(f"Actividad especial: {perro1.jugar()}")
    print(f"Información del gato: {gato1.info()}")
    print(f"Actividad especial: {gato1.dormir()}\n")

    # Demostrar polimorfismo
    print("3. POLIMORFISMO:")
    print("Sonidos diferentes para cada animal:")
    print(f"- {perro1.hacer_sonido()}")
    print(f"- {gato1.hacer_sonido()}\n")

    # Polimorfismo con argumentos múltiples
    print("4. PRESENTACIÓN DE TODOS LOS ANIMALES:")
    presentar_animales(perro1, gato1)