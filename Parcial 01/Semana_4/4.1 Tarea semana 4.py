# EjemplosMundoReal_POO/sistema_biblioteca.py
"""
Sistema de Biblioteca - Ejemplo de Programación Orientada a Objetos
Modela una biblioteca con libros, usuarios y préstamos
"""

from datetime import datetime, timedelta


class Libro:
    """Clase que representa un libro en la biblioteca"""

    def __init__(self, titulo, autor, isbn):
        # Atributos privados del libro
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._disponible = True  # Estado del libro
        self._prestado_a = None  # Usuario que tiene el libro

    # Métodos getter (propiedades)
    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def disponible(self):
        return self._disponible

    def prestar(self, usuario):
        """Método para prestar el libro a un usuario"""
        if self._disponible:
            self._disponible = False
            self._prestado_a = usuario
            return True
        return False

    def devolver(self):
        """Método para devolver el libro"""
        self._disponible = True
        self._prestado_a = None

    def __str__(self):
        """Representación en cadena del libro"""
        estado = "Disponible" if self._disponible else f"Prestado a {self._prestado_a}"
        return f"'{self._titulo}' por {self._autor} - {estado}"


class Usuario:
    """Clase que representa un usuario de la biblioteca"""

    def __init__(self, nombre, id_usuario):
        # Atributos del usuario
        self._nombre = nombre
        self._id_usuario = id_usuario
        self._libros_prestados = []  # Lista de libros que tiene el usuario
        self._limite_libros = 3  # Límite máximo de libros

    @property
    def nombre(self):
        return self._nombre

    @property
    def id_usuario(self):
        return self._id_usuario

    def puede_pedir_prestamo(self):
        """Verifica si el usuario puede pedir más libros prestados"""
        return len(self._libros_prestados) < self._limite_libros

    def agregar_libro(self, libro):
        """Agrega un libro a la lista de libros prestados"""
        if self.puede_pedir_prestamo():
            self._libros_prestados.append(libro)
            return True
        return False

    def devolver_libro(self, libro):
        """Remueve un libro de la lista de libros prestados"""
        if libro in self._libros_prestados:
            self._libros_prestados.remove(libro)
            return True
        return False

    def __str__(self):
        """Representación en cadena del usuario"""
        return f"Usuario: {self._nombre} (ID: {self._id_usuario}) - {len(self._libros_prestados)} libros prestados"


class Biblioteca:
    """Clase principal que gestiona la biblioteca"""

    def __init__(self, nombre):
        # Atributos de la biblioteca
        self._nombre = nombre
        self._catalogo = []  # Lista de todos los libros
        self._usuarios = []  # Lista de usuarios registrados
        self._prestamos = []  # Historial de préstamos

    def agregar_libro(self, libro):
        """Añade un libro al catálogo de la biblioteca"""
        self._catalogo.append(libro)
        print(f"✓ Libro agregado: {libro.titulo}")

    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario en la biblioteca"""
        self._usuarios.append(usuario)
        print(f"✓ Usuario registrado: {usuario.nombre}")

    def buscar_libro(self, titulo):
        """Busca un libro por título en el catálogo"""
        for libro in self._catalogo:
            if titulo.lower() in libro.titulo.lower():
                return libro
        return None

    def prestar_libro(self, titulo, id_usuario):
        """Gestiona el préstamo de un libro a un usuario"""
        # Buscar el libro
        libro = self.buscar_libro(titulo)
        if not libro:
            print(f"❌ Libro '{titulo}' no encontrado")
            return False

        # Buscar el usuario
        usuario = self._buscar_usuario(id_usuario)
        if not usuario:
            print(f"❌ Usuario con ID {id_usuario} no encontrado")
            return False

        # Verificar disponibilidad y límites
        if not libro.disponible:
            print(f"❌ El libro '{libro.titulo}' no está disponible")
            return False

        if not usuario.puede_pedir_prestamo():
            print(f"❌ {usuario.nombre} ha alcanzado el límite de libros")
            return False

        # Realizar el préstamo
        if libro.prestar(usuario.nombre) and usuario.agregar_libro(libro):
            # Registrar el préstamo
            prestamo = {
                'libro': libro.titulo,
                'usuario': usuario.nombre,
                'fecha': datetime.now(),
                'devuelto': False
            }
            self._prestamos.append(prestamo)
            print(f"✓ Libro '{libro.titulo}' prestado a {usuario.nombre}")
            return True

        return False

    def devolver_libro(self, titulo, id_usuario):
        """Gestiona la devolución de un libro"""
        libro = self.buscar_libro(titulo)
        usuario = self._buscar_usuario(id_usuario)

        if libro and usuario:
            if usuario.devolver_libro(libro):
                libro.devolver()
                # Actualizar historial
                for prestamo in self._prestamos:
                    if (prestamo['libro'] == libro.titulo and
                            prestamo['usuario'] == usuario.nombre and
                            not prestamo['devuelto']):
                        prestamo['devuelto'] = True
                        break

                print(f"✓ Libro '{libro.titulo}' devuelto por {usuario.nombre}")
                return True

        print(f"❌ No se pudo procesar la devolución")
        return False

    def _buscar_usuario(self, id_usuario):
        """Método privado para buscar usuario por ID"""
        for usuario in self._usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    def mostrar_catalogo(self):
        """Muestra todos los libros del catálogo"""
        print(f"\n📚 Catálogo de {self._nombre}:")
        print("-" * 50)
        for libro in self._catalogo:
            print(f"  {libro}")

    def mostrar_usuarios(self):
        """Muestra todos los usuarios registrados"""
        print(f"\n👥 Usuarios de {self._nombre}:")
        print("-" * 40)
        for usuario in self._usuarios:
            print(f"  {usuario}")


# Ejemplo de uso del sistema
def main():
    """Función principal que demuestra el uso del sistema"""

    # Crear la biblioteca
    biblioteca = Biblioteca("Biblioteca Central")

    # Crear libros
    libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "978-0307474728")
    libro2 = Libro("1984", "George Orwell", "978-0451524935")
    libro3 = Libro("El Quijote", "Miguel de Cervantes", "978-8424116606")

    # Agregar libros a la biblioteca
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)

    # Crear usuarios
    usuario1 = Usuario("Oscar Zambrano", "U001")
    usuario2 = Usuario("Alejandro Bravo", "U002")

    # Registrar usuarios
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)

    # Mostrar estado inicial
    biblioteca.mostrar_catalogo()
    biblioteca.mostrar_usuarios()

    print("\n" + "=" * 60)
    print("OPERACIONES DE PRÉSTAMO")
    print("=" * 60)

    # Realizar préstamos
    biblioteca.prestar_libro("1984", "U001")
    biblioteca.prestar_libro("Cien años", "U002")
    biblioteca.prestar_libro("El Quijote", "U001")

    # Intentar préstamo de libro no disponible
    biblioteca.prestar_libro("1984", "U002")

    # Mostrar estado después de préstamos
    print("\n📊 Estado después de préstamos:")
    biblioteca.mostrar_catalogo()
    biblioteca.mostrar_usuarios()

    print("\n" + "=" * 60)
    print("OPERACIONES DE DEVOLUCIÓN")
    print("=" * 60)

    # Devolver libros
    biblioteca.devolver_libro("1984", "U001")

    # Mostrar estado final
    print("\n📊 Estado final:")
    biblioteca.mostrar_catalogo()
    biblioteca.mostrar_usuarios()


# Ejecutar el programa
if __name__ == "__main__":
    main()