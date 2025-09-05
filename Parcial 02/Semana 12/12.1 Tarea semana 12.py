class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self._autor_titulo = (autor, titulo)  # Tupla inmutable
        self.categoria = categoria
        self.isbn = isbn
        self.prestado = False

    @property
    def autor(self): return self._autor_titulo[0]

    @property
    def titulo(self): return self._autor_titulo[1]

    def __str__(self):
        estado = "Prestado" if self.prestado else "Disponible"
        return f"'{self.titulo}' por {self.autor} - {self.categoria} [{estado}]"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista para préstamos

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_usuario}) - {len(self.libros_prestados)} libros"


class Biblioteca:
    def __init__(self, nombre="Biblioteca Digital"):
        self.nombre = nombre
        self.libros = {}  # Diccionario: ISBN -> Libro
        self.usuarios = {}  # Diccionario: ID -> Usuario
        self.ids_usuarios = set()  # Conjunto para IDs únicos

    # === LIBROS ===
    def agregar_libro(self, libro):
        if libro.isbn in self.libros:
            return print(f"Error: ISBN {libro.isbn} ya existe")
        self.libros[libro.isbn] = libro
        print(f"✓ Libro agregado: {libro.titulo}")

    def quitar_libro(self, isbn):
        if isbn not in self.libros or self.libros[isbn].prestado:
            return print("Error: Libro no existe o está prestado")
        del self.libros[isbn]
        print("✓ Libro quitado")

    def editar_categoria(self, isbn, nueva_categoria):
        if isbn not in self.libros:
            return print("Error: Libro no encontrado")
        self.libros[isbn].categoria = nueva_categoria
        print(f"✓ Categoría actualizada: {nueva_categoria}")

    # === USUARIOS ===
    def registrar_usuario(self, usuario):
        if usuario.id_usuario in self.ids_usuarios:
            return print(f"Error: ID {usuario.id_usuario} ya existe")
        self.usuarios[usuario.id_usuario] = usuario
        self.ids_usuarios.add(usuario.id_usuario)
        print(f"✓ Usuario registrado: {usuario.nombre}")

    def dar_baja_usuario(self, id_usuario):
        if id_usuario not in self.ids_usuarios or self.usuarios[id_usuario].libros_prestados:
            return print("Error: Usuario no existe o tiene libros prestados")
        del self.usuarios[id_usuario]
        self.ids_usuarios.remove(id_usuario)
        print("✓ Usuario dado de baja")

    def editar_nombre_usuario(self, id_usuario, nuevo_nombre):
        if id_usuario not in self.ids_usuarios:
            return print("Error: Usuario no encontrado")
        self.usuarios[id_usuario].nombre = nuevo_nombre
        print(f"✓ Nombre actualizado: {nuevo_nombre}")

    # === PRÉSTAMOS ===
    def prestar_libro(self, isbn, id_usuario):
        if (isbn not in self.libros or id_usuario not in self.ids_usuarios
                or self.libros[isbn].prestado):
            return print("Error: Libro/Usuario no existe o libro ya prestado")

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]
        libro.prestado = True
        usuario.libros_prestados.append(libro)
        print(f"✓ Prestado: '{libro.titulo}' a {usuario.nombre}")

    def devolver_libro(self, isbn, id_usuario):
        if (isbn not in self.libros or id_usuario not in self.ids_usuarios):
            return print("Error: Libro/Usuario no existe")

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]
        if libro not in usuario.libros_prestados:
            return print("Error: Usuario no tiene este libro")

        libro.prestado = False
        usuario.libros_prestados.remove(libro)
        print(f"✓ Devuelto: '{libro.titulo}'")

    def transferir_libro(self, isbn, id_origen, id_destino):
        self.devolver_libro(isbn, id_origen)
        self.prestar_libro(isbn, id_destino)

    # === BÚSQUEDAS ===
    def buscar(self, termino, tipo="titulo"):
        campo_map = {"titulo": "titulo", "autor": "autor", "categoria": "categoria"}
        if tipo not in campo_map:
            return []
        return [libro for libro in self.libros.values()
                if termino.lower() in getattr(libro, campo_map[tipo]).lower()]

    def obtener_libro(self, isbn):
        return self.libros.get(isbn)

    def obtener_usuario(self, id_usuario):
        return self.usuarios.get(id_usuario)

    # === LISTADOS ===
    def listar_libros_prestados_usuario(self, id_usuario):
        return self.usuarios.get(id_usuario, Usuario("", "")).libros_prestados

    def listar_por_estado(self, prestado=None):
        if prestado is None: return list(self.libros.values())
        return [libro for libro in self.libros.values() if libro.prestado == prestado]

    def estadisticas(self):
        total = len(self.libros)
        prestados = sum(1 for libro in self.libros.values() if libro.prestado)
        print(f"\n=== {self.nombre.upper()} ===")
        print(f"Libros: {total} | Disponibles: {total - prestados} | Prestados: {prestados}")
        print(f"Usuarios: {len(self.usuarios)}")


# === INTERFAZ INTERACTIVA COMPACTA ===
def input_libro():
    return Libro(input("Título: "), input("Autor: "), input("Categoría: "), input("ISBN: "))


def input_usuario():
    return Usuario(input("Nombre: "), input("ID: "))


def mostrar_lista(items, titulo):
    if items:
        print(f"\n{titulo} ({len(items)}):")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
    else:
        print(f"No hay {titulo.lower()}")


def ejecutar_busqueda(biblioteca):
    print("\n1. Por título  2. Por autor  3. Por categoría  4. Por ISBN")
    tipo_map = {"1": "titulo", "2": "autor", "3": "categoria", "4": "isbn"}
    tipo = tipo_map.get(input("Tipo: "))

    if tipo == "isbn":
        libro = biblioteca.obtener_libro(input("ISBN: "))
        print(f"Resultado: {libro}" if libro else "No encontrado")
    else:
        resultados = biblioteca.buscar(input("Término: "), tipo)
        mostrar_lista(resultados, "Resultados")


def menu_principal():
    biblioteca = Biblioteca()

    # Datos de ejemplo
    biblioteca.agregar_libro(Libro("1984", "George Orwell", "Distopía", "001"))
    biblioteca.agregar_libro(Libro("El principito", "Saint-Exupéry", "Filosofía", "002"))
    biblioteca.registrar_usuario(Usuario("Oscar", "0123456789"))
    biblioteca.registrar_usuario(Usuario("Alejandro", "9876543210"))

    opciones = {
        "1": ("Libros", {
            "1": ("Agregar", lambda: biblioteca.agregar_libro(input_libro())),
            "2": ("Quitar", lambda: biblioteca.quitar_libro(input("ISBN: "))),
            "3": ("Editar categoría", lambda: biblioteca.editar_categoria(
                input("ISBN: "), input("Nueva categoría: "))),
            "4": ("Listar todos", lambda: mostrar_lista(biblioteca.listar_por_estado(), "Todos los libros"))
        }),

        "2": ("Usuarios", {
            "1": ("Registrar", lambda: biblioteca.registrar_usuario(input_usuario())),
            "2": ("Dar de baja", lambda: biblioteca.dar_baja_usuario(input("ID: "))),
            "3": ("Editar nombre", lambda: biblioteca.editar_nombre_usuario(
                input("ID: "), input("Nuevo nombre: "))),
            "4": ("Listar todos", lambda: mostrar_lista(list(biblioteca.usuarios.values()), "Todos los usuarios"))
        }),

        "3": ("Préstamos", {
            "1": ("Prestar", lambda: biblioteca.prestar_libro(input("ISBN: "), input("ID usuario: "))),
            "2": ("Devolver", lambda: biblioteca.devolver_libro(input("ISBN: "), input("ID usuario: "))),
            "3": ("Transferir", lambda: biblioteca.transferir_libro(
                input("ISBN: "), input("ID origen: "), input("ID destino: "))),
            "4": ("Libros de usuario", lambda: mostrar_lista(
                biblioteca.listar_libros_prestados_usuario(input("ID usuario: ")), "Libros prestados")),
            "5": ("Disponibles", lambda: mostrar_lista(biblioteca.listar_por_estado(False), "Libros disponibles")),
            "6": ("Prestados", lambda: mostrar_lista(biblioteca.listar_por_estado(True), "Libros prestados"))
        }),

        "4": ("Búsquedas", {
            "1": ("Buscar", lambda: ejecutar_busqueda(biblioteca))
        }),

        "5": ("Reportes", {
            "1": ("Estadísticas", biblioteca.estadisticas),
            "2": ("Todos los libros", lambda: mostrar_lista(biblioteca.listar_por_estado(), "Todos los libros")),
            "3": ("Todos los usuarios", lambda: mostrar_lista(list(biblioteca.usuarios.values()), "Todos los usuarios"))
        }),

        "6": ("Config", {
            "1": ("Cambiar nombre", lambda: setattr(biblioteca, 'nombre', input("Nuevo nombre: "))),
            "2": ("Info actual", lambda: print(f"Biblioteca: {biblioteca.nombre}"))
        })
    }

    while True:
        print("\n" + "=" * 40)
        print("BIBLIOTECA DIGITAL")
        print("=" * 40)
        for key, (titulo, _) in opciones.items():
            print(f"{key}. {titulo}")
        print("0. Salir")

        opcion = input("\nOpción: ")

        if opcion == "0":
            print("¡Adiós!")
            break
        elif opcion in opciones:
            titulo, submenus = opciones[opcion]

            while True:
                print(f"\n{titulo}")
                print("-" * 20)
                for sub_key, (sub_titulo, _) in submenus.items():
                    print(f"{sub_key}. {sub_titulo}")
                print("0. Volver")

                sub_opcion = input("\nSubopción: ")

                if sub_opcion == "0":
                    break
                elif sub_opcion in submenus:
                    try:
                        submenus[sub_opcion][1]()  # Ejecutar función
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Opción inválida")
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu_principal()