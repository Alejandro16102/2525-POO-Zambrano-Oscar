# Programa POO - Constructores y Destructores

class Estudiante:

    def __init__(self, nombre, edad):
        print(f" CONSTRUCTOR: Creando estudiante {nombre}")
        self.nombre = nombre
        self.edad = edad
        print(f" Estudiante {nombre} creado correctamente")

    def __del__(self):

        print(f" DESTRUCTOR: Eliminando estudiante {self.nombre}")
        print(f" {self.nombre} eliminado del sistema")

    def mostrar_info(self):
        print(f"    {self.nombre}, {self.edad} años")


class Archivo:

    def __init__(self, nombre):

        print(f" CONSTRUCTOR: Abriendo archivo {nombre}")
        self.nombre = nombre
        self.archivo = open(nombre, 'w')
        self.archivo.write("=== ARCHIVO CREADO ===\n")
        print(f"  Archivo {nombre} abierto")

    def __del__(self):

        print(f" DESTRUCTOR: Cerrando archivo {self.nombre}")
        self.archivo.write("=== ARCHIVO CERRADO ===\n")
        self.archivo.close()
        print(f"  Archivo {self.nombre} cerrado")

    def escribir(self, texto):
        self.archivo.write(f"{texto}\n")
        print(f"  Escrito: {texto}")


def main():
    print("=" * 40)
    print("  CONSTRUCTORES Y DESTRUCTORES")
    print("=" * 40)

    print("\n1. CREANDO OBJETOS:")
    # Los constructores se ejecutan automáticamente
    estudiante1 = Estudiante("Ana", 20)
    estudiante2 = Estudiante("Carlos", 22)

    # Mostrar información
    estudiante1.mostrar_info()
    estudiante2.mostrar_info()

    print("\n2. TRABAJANDO CON ARCHIVO:")
    # Constructor abre el archivo
    archivo = Archivo("datos.txt")
    archivo.escribir("Estudiante Ana creado")
    archivo.escribir("Estudiante Carlos creado")

    print("\n3. ELIMINANDO OBJETO:")
    # Destructor se ejecuta explícitamente
    del estudiante1

    print("   Los destructores restantes se ejecutan automáticamente...")


if __name__ == "__main__":
    main()

