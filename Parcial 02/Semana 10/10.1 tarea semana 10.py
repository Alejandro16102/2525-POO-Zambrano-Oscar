import os
import json
from typing import List, Tuple, Optional


class Producto:
    """Clase que representa un producto en el inventario"""

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    def get_id(self):
        return self.__id_producto

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    def set_precio(self, precio):
        if precio >= 0:
            self.__precio = precio
        else:
            raise ValueError("El precio no puede ser negativo")

    def to_dict(self):
        """Convierte el producto a diccionario para serialización"""
        return {
            'id_producto': self.__id_producto,
            'nombre': self.__nombre,
            'cantidad': self.__cantidad,
            'precio': self.__precio
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario"""
        return cls(data['id_producto'], data['nombre'], data['cantidad'], data['precio'])

    def __str__(self):
        return f"ID: {self.__id_producto} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"


class Inventario:
    """Clase que gestiona el inventario de productos con persistencia en archivos"""

    def __init__(self, archivo_inventario="inventario.json"):
        self.__productos = []
        self.__archivo_inventario = archivo_inventario
        self.__cargar_inventario()

    def __buscar_por_id(self, id_producto):
        """Método privado para buscar un producto por ID"""
        for i, producto in enumerate(self.__productos):
            if producto.get_id() == id_producto:
                return i
        return -1

    def __cargar_inventario(self):
        """Carga los productos desde el archivo de inventario"""
        try:
            if os.path.exists(self.__archivo_inventario):
                with open(self.__archivo_inventario, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read().strip()
                    if contenido:  # Solo procesar si el archivo no está vacío
                        datos = json.loads(contenido)
                        for producto_data in datos:
                            producto = Producto.from_dict(producto_data)
                            self.__productos.append(producto)
                        print(f"✓ Inventario cargado exitosamente desde '{self.__archivo_inventario}'")
                        print(f"  Se cargaron {len(self.__productos)} productos")
                    else:
                        print(f"✓ Archivo '{self.__archivo_inventario}' existe pero está vacío")
            else:
                print(
                    f"ℹ Archivo '{self.__archivo_inventario}' no existe. Se creará automáticamente al añadir productos.")
        except FileNotFoundError:
            print(f"ℹ Archivo '{self.__archivo_inventario}' no encontrado. Se creará automáticamente.")
        except PermissionError:
            print(f" Error de permisos: No se puede leer el archivo '{self.__archivo_inventario}'")
            print("   Verifique que tenga permisos de lectura en el directorio.")
        except json.JSONDecodeError as e:
            print(f" Error al leer el archivo '{self.__archivo_inventario}': formato JSON inválido")
            print(f"   Detalles: {str(e)}")
            print("   El inventario iniciará vacío. Considere revisar o respaldar el archivo.")
        except Exception as e:
            print(f" Error inesperado al cargar inventario: {str(e)}")
            print("   El inventario iniciará vacío.")

    def __guardar_inventario(self):
        """Guarda todos los productos en el archivo de inventario"""
        try:
            datos = [producto.to_dict() for producto in self.__productos]

            # Crear el directorio si no existe
            directorio = os.path.dirname(self.__archivo_inventario)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)

            with open(self.__archivo_inventario, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            return True, f"Inventario guardado exitosamente en '{self.__archivo_inventario}'"
        except PermissionError:
            return False, f"Error de permisos: No se puede escribir en '{self.__archivo_inventario}'"
        except OSError as e:
            return False, f"Error del sistema al guardar: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado al guardar inventario: {str(e)}"

    def añadir_producto(self, id_producto, nombre, cantidad, precio):
        """Añade un nuevo producto al inventario y lo guarda en archivo"""
        # Verificar que el ID sea único
        if self.__buscar_por_id(id_producto) != -1:
            return False, "Error: Ya existe un producto con ese ID"

        try:
            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            self.__productos.append(nuevo_producto)

            # Guardar en archivo
            exito_guardado, mensaje_guardado = self.__guardar_inventario()
            if exito_guardado:
                return True, f"✓ Producto añadido exitosamente y guardado en archivo\n  {mensaje_guardado}"
            else:
                # Si no se pudo guardar, remover el producto de memoria
                self.__productos.pop()
                return False, f" Producto no añadido - Error al guardar: {mensaje_guardado}"

        except ValueError as e:
            return False, f"Error de validación: {str(e)}"

    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario por ID y actualiza el archivo"""
        indice = self.__buscar_por_id(id_producto)
        if indice == -1:
            return False, "Error: No se encontró un producto con ese ID"

        producto_eliminado = self.__productos.pop(indice)

        # Guardar cambios en archivo
        exito_guardado, mensaje_guardado = self.__guardar_inventario()
        if exito_guardado:
            return True, f"✓ Producto '{producto_eliminado.get_nombre()}' eliminado exitosamente\n  {mensaje_guardado}"
        else:
            # Si no se pudo guardar, restaurar el producto
            self.__productos.insert(indice, producto_eliminado)
            return False, f" Producto no eliminado - Error al guardar: {mensaje_guardado}"

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza la cantidad y/o precio de un producto por ID y guarda en archivo"""
        indice = self.__buscar_por_id(id_producto)
        if indice == -1:
            return False, "Error: No se encontró un producto con ese ID"

        producto = self.__productos[indice]

        # Guardar valores originales para posible rollback
        cantidad_original = producto.get_cantidad()
        precio_original = producto.get_precio()
        cambios = []

        try:
            if nueva_cantidad is not None:
                producto.set_cantidad(nueva_cantidad)
                cambios.append(f"cantidad: {nueva_cantidad}")

            if nuevo_precio is not None:
                producto.set_precio(nuevo_precio)
                cambios.append(f"precio: ${nuevo_precio:.2f}")

            if cambios:
                # Guardar cambios en archivo
                exito_guardado, mensaje_guardado = self.__guardar_inventario()
                if exito_guardado:
                    return True, f"✓ Producto actualizado: {', '.join(cambios)}\n  {mensaje_guardado}"
                else:
                    # Rollback si no se pudo guardar
                    producto.set_cantidad(cantidad_original)
                    producto.set_precio(precio_original)
                    return False, f" Producto no actualizado - Error al guardar: {mensaje_guardado}"
            else:
                return False, "No se especificaron cambios"

        except ValueError as e:
            # Rollback en caso de error de validación
            producto.set_cantidad(cantidad_original)
            producto.set_precio(precio_original)
            return False, f"Error de validación: {str(e)}"

    def buscar_por_nombre(self, nombre_busqueda):
        """Busca productos por nombre (búsqueda parcial, no sensible a mayúsculas)"""
        productos_encontrados = []
        nombre_busqueda = nombre_busqueda.lower()

        for producto in self.__productos:
            if nombre_busqueda in producto.get_nombre().lower():
                productos_encontrados.append(producto)

        return productos_encontrados

    def mostrar_todos(self):
        """Muestra todos los productos en el inventario"""
        if not self.__productos:
            return "El inventario está vacío"

        resultado = "=== INVENTARIO COMPLETO ===\n"
        for producto in self.__productos:
            resultado += str(producto) + "\n"
        resultado += f"Total de productos: {len(self.__productos)}\n"
        resultado += f"Archivo: {self.__archivo_inventario}"
        return resultado

    def get_total_productos(self):
        """Retorna el número total de productos"""
        return len(self.__productos)

    def crear_respaldo(self, archivo_respaldo=None):
        """Crea un respaldo del inventario actual"""
        if archivo_respaldo is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_respaldo = f"respaldo_inventario_{timestamp}.txt"

        try:
            datos = [producto.to_dict() for producto in self.__productos]
            with open(archivo_respaldo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            return True, f"✓ Respaldo creado exitosamente: '{archivo_respaldo}'"
        except Exception as e:
            return False, f" Error al crear respaldo: {str(e)}"


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 60)
    print("    SISTEMA DE GESTIÓN DE INVENTARIOS CON PERSISTENCIA")
    print("=" * 60)
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar productos por nombre")
    print("5. Mostrar todos los productos")
    print("6. Estadísticas del inventario")
    print("7. Crear respaldo del inventario")
    print("0. Salir")
    print("=" * 60)


def obtener_numero(mensaje, tipo=int, min_valor=None):
    """Función auxiliar para obtener números con validación"""
    while True:
        try:
            valor = tipo(input(mensaje))
            if min_valor is not None and valor < min_valor:
                print(f"Error: El valor debe ser mayor o igual a {min_valor}")
                continue
            return valor
        except ValueError:
            print("Error: Ingrese un número válido")


def main():
    """Función principal que ejecuta el programa"""
    print("=" * 60)
    print("    INICIALIZANDO SISTEMA DE GESTIÓN DE INVENTARIOS")
    print("=" * 60)

    inventario = Inventario()

    # Solo añadir datos de ejemplo si el inventario está vacío
    if inventario.get_total_productos() == 0:
        print("\nInventario vacío. Añadiendo datos de ejemplo...")
        inventario.añadir_producto(1, "Laptop Dell", 5, 650.99)
        inventario.añadir_producto(2, "Mouse Inalámbrico", 15, 25.50)
        inventario.añadir_producto(3, "Teclado Mecánico", 8, 30.00)
        print("✓ Datos de ejemplo añadidos")

    while True:
        mostrar_menu()

        try:
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                # Añadir producto
                print("\n--- AÑADIR NUEVO PRODUCTO ---")
                id_producto = obtener_numero("ID del producto: ", int, 1)
                nombre = input("Nombre del producto: ").strip()
                if not nombre:
                    print("Error: El nombre no puede estar vacío")
                    continue
                cantidad = obtener_numero("Cantidad: ", int, 0)
                precio = obtener_numero("Precio: $", float, 0)

                exito, mensaje = inventario.añadir_producto(id_producto, nombre, cantidad, precio)
                print(f"\n{mensaje}")

            elif opcion == "2":
                # Eliminar producto
                print("\n--- ELIMINAR PRODUCTO ---")
                id_producto = obtener_numero("ID del producto a eliminar: ", int, 1)

                exito, mensaje = inventario.eliminar_producto(id_producto)
                print(f"\n{mensaje}")

            elif opcion == "3":
                # Actualizar producto
                print("\n--- ACTUALIZAR PRODUCTO ---")
                id_producto = obtener_numero("ID del producto a actualizar: ", int, 1)

                print("Deje en blanco si no desea cambiar ese campo:")
                cantidad_input = input("Nueva cantidad (actual se mantiene si está vacío): ").strip()
                precio_input = input("Nuevo precio (actual se mantiene si está vacío): ").strip()

                nueva_cantidad = None
                nuevo_precio = None

                if cantidad_input:
                    try:
                        nueva_cantidad = int(cantidad_input)
                        if nueva_cantidad < 0:
                            print("Error: La cantidad no puede ser negativa")
                            continue
                    except ValueError:
                        print("Error: Cantidad inválida")
                        continue

                if precio_input:
                    try:
                        nuevo_precio = float(precio_input)
                        if nuevo_precio < 0:
                            print("Error: El precio no puede ser negativo")
                            continue
                    except ValueError:
                        print("Error: Precio inválido")
                        continue

                exito, mensaje = inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)
                print(f"\n{mensaje}")

            elif opcion == "4":
                # Buscar por nombre
                print("\n--- BUSCAR PRODUCTOS ---")
                nombre_busqueda = input("Ingrese el nombre a buscar: ").strip()

                if nombre_busqueda:
                    productos_encontrados = inventario.buscar_por_nombre(nombre_busqueda)

                    if productos_encontrados:
                        print(f"\nSe encontraron {len(productos_encontrados)} producto(s):")
                        for producto in productos_encontrados:
                            print(producto)
                    else:
                        print("No se encontraron productos con ese nombre")
                else:
                    print("Error: Debe ingresar un nombre para buscar")

            elif opcion == "5":
                # Mostrar todos
                print("\n" + inventario.mostrar_todos())

            elif opcion == "6":
                # Estadísticas
                print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
                total_productos = inventario.get_total_productos()
                print(f"Total de productos diferentes: {total_productos}")

                if total_productos > 0:
                    # Calcular valor total del inventario
                    valor_total = 0
                    cantidad_total = 0

                    # Obtener todos los productos para calcular estadísticas
                    todos_productos = inventario.buscar_por_nombre("")  # Truco para obtener todos

                    for producto in todos_productos:
                        valor_total += producto.get_precio() * producto.get_cantidad()
                        cantidad_total += producto.get_cantidad()

                    print(f"Cantidad total de items: {cantidad_total}")
                    print(f"Valor total del inventario: ${valor_total:.2f}")
                    print(
                        f"Valor promedio por producto: ${valor_total / cantidad_total:.2f}" if cantidad_total > 0 else "N/A")

            elif opcion == "7":
                # Crear respaldo
                print("\n--- CREAR RESPALDO DEL INVENTARIO ---")
                respuesta = input("¿Desea especificar el nombre del archivo de respaldo? (s/n): ").strip().lower()

                if respuesta == 's':
                    nombre_respaldo = input("Nombre del archivo de respaldo: ").strip()
                    if not nombre_respaldo.endswith('.json'):
                        nombre_respaldo += '.json'
                    exito, mensaje = inventario.crear_respaldo(nombre_respaldo)
                else:
                    exito, mensaje = inventario.crear_respaldo()

                print(f"\n{mensaje}")

            elif opcion == "0":
                # Salir
                print("\n¡Gracias por usar el Sistema de Gestión de Inventarios!")
                print("Todos los cambios han sido guardados automáticamente.")
                print("¡Hasta luego!")
                break

            else:
                print("Error: Opción no válida. Por favor seleccione una opción del 0 al 7.")

        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            print("Todos los cambios han sido guardados automáticamente.")
            print("¡Hasta luego!")
            break
        except Exception as e:
            print(f" Error inesperado: {e}")
            print("Por favor, intente nuevamente.")

        # Pausa para que el usuario pueda leer los mensajes
        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()