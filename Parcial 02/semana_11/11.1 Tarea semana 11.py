import json
import os
from typing import Dict, List, Optional


class Producto:
    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        self.id_producto = id_producto.strip().upper()
        self.nombre = nombre.strip().title()
        self.cantidad = max(0, int(cantidad))
        self.precio = max(0.0, float(precio))

    def valor_total(self) -> float:
        return self.cantidad * self.precio

    def to_dict(self) -> Dict:
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(data['id_producto'], data['nombre'], data['cantidad'], data['precio'])

    def __str__(self) -> str:
        return f"ID: {self.id_producto} | {self.nombre} | Cant: {self.cantidad} | ${self.precio:.2f} | Total: ${self.valor_total():.2f}"


class Inventario:
    def __init__(self, archivo: str = "inventario.json"):
        self._productos: Dict[str, Producto] = {}
        self._archivo = archivo
        self._cargar()

    def agregar(self, id_prod: str, nombre: str, cantidad: int, precio: float) -> bool:
        id_prod = id_prod.strip().upper()
        if id_prod in self._productos:
            return False
        self._productos[id_prod] = Producto(id_prod, nombre, cantidad, precio)
        self._guardar()
        return True

    def eliminar(self, id_prod: str) -> bool:
        id_prod = id_prod.strip().upper()
        if id_prod in self._productos:
            del self._productos[id_prod]
            self._guardar()
            return True
        return False

    def actualizar_cantidad(self, id_prod: str, cantidad: int) -> bool:
        producto = self.obtener(id_prod)
        if producto:
            producto.cantidad = max(0, int(cantidad))
            self._guardar()
            return True
        return False

    def actualizar_precio(self, id_prod: str, precio: float) -> bool:
        producto = self.obtener(id_prod)
        if producto:
            producto.precio = max(0.0, float(precio))
            self._guardar()
            return True
        return False

    def obtener(self, id_prod: str) -> Optional[Producto]:
        return self._productos.get(id_prod.strip().upper())

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        nombre = nombre.lower()
        return [p for p in self._productos.values() if nombre in p.nombre.lower()]

    def listar_todos(self) -> List[Producto]:
        return sorted(self._productos.values(), key=lambda p: p.id_producto)

    def sin_stock(self) -> List[Producto]:
        return [p for p in self._productos.values() if p.cantidad == 0]

    def valor_total(self) -> float:
        return sum(p.valor_total() for p in self._productos.values())

    def estadisticas(self) -> Dict:
        productos = list(self._productos.values())
        if not productos:
            return {'total_productos': 0, 'valor_total': 0.0, 'sin_stock': 0}

        return {
            'total_productos': len(productos),
            'total_items': sum(p.cantidad for p in productos),
            'valor_total': self.valor_total(),
            'sin_stock': len(self.sin_stock()),
            'precio_promedio': sum(p.precio for p in productos) / len(productos)
        }

    def _guardar(self):
        try:
            os.makedirs(os.path.dirname(self._archivo) if os.path.dirname(self._archivo) else '.', exist_ok=True)
            with open(self._archivo, 'w', encoding='utf-8') as f:
                json.dump({id_p: p.to_dict() for id_p, p in self._productos.items()}, f, indent=2)
        except Exception as e:
            print(f"Error al guardar: {e}")

    def _cargar(self):
        if os.path.exists(self._archivo):
            try:
                with open(self._archivo, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for id_prod, prod_data in data.items():
                        self._productos[id_prod] = Producto.from_dict(prod_data)
            except Exception as e:
                print(f"Error al cargar: {e}")


class Menu:
    def __init__(self):
        self.inventario = Inventario()

    def mostrar_menu(self):
        print("\n" + "=" * 50)
        print("🏪 SISTEMA DE GESTIÓN DE INVENTARIOS")
        print("=" * 50)
        print("1. ➕ Agregar producto")
        print("2. 🗑️  Eliminar producto")
        print("3. 📊 Actualizar cantidad")
        print("4. 💰 Actualizar precio")
        print("5. 🔍 Buscar por nombre")
        print("6. 📋 Mostrar todos")
        print("7. 📈 Estadísticas")
        print("8. ⚠️  Sin stock")
        print("0. 🚪 Salir")
        print("=" * 50)

    def ejecutar(self):
        while True:
            try:
                self.mostrar_menu()
                opcion = input("Opción: ").strip()

                if opcion == "0":
                    print("¡Hasta luego!")
                    break
                elif opcion == "1":
                    self._agregar_producto()
                elif opcion == "2":
                    self._eliminar_producto()
                elif opcion == "3":
                    self._actualizar_cantidad()
                elif opcion == "4":
                    self._actualizar_precio()
                elif opcion == "5":
                    self._buscar_productos()
                elif opcion == "6":
                    self._mostrar_todos()
                elif opcion == "7":
                    self._mostrar_estadisticas()
                elif opcion == "8":
                    self._mostrar_sin_stock()
                else:
                    print("❌ Opción inválida")

                input("\nPresione Enter para continuar...")
            except Exception as e:
                print(f"❌ Error: {e}")

    def _agregar_producto(self):
        print("\n➕ AGREGAR PRODUCTO")
        try:
            id_prod = input("ID: ").strip()
            if not id_prod:
                print("❌ ID requerido")
                return

            nombre = input("Nombre: ").strip()
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: $"))

            if self.inventario.agregar(id_prod, nombre, cantidad, precio):
                print("✅ Producto agregado")
            else:
                print("❌ ID ya existe")
        except ValueError:
            print("❌ Datos inválidos")

    def _eliminar_producto(self):
        print("\n🗑️ ELIMINAR PRODUCTO")
        id_prod = input("ID del producto: ").strip()

        producto = self.inventario.obtener(id_prod)
        if not producto:
            print("❌ Producto no encontrado")
            return

        print(f"Producto: {producto}")
        if input("¿Eliminar? (s/N): ").lower() == 's':
            if self.inventario.eliminar(id_prod):
                print("✅ Eliminado")
            else:
                print("❌ Error al eliminar")

    def _actualizar_cantidad(self):
        print("\n📊 ACTUALIZAR CANTIDAD")
        id_prod = input("ID: ").strip()

        producto = self.inventario.obtener(id_prod)
        if not producto:
            print("❌ No encontrado")
            return

        print(f"Actual: {producto}")
        try:
            cantidad = int(input("Nueva cantidad: "))
            if self.inventario.actualizar_cantidad(id_prod, cantidad):
                print("✅ Actualizado")
            else:
                print("❌ Error")
        except ValueError:
            print("❌ Número inválido")

    def _actualizar_precio(self):
        print("\n💰 ACTUALIZAR PRECIO")
        id_prod = input("ID: ").strip()

        producto = self.inventario.obtener(id_prod)
        if not producto:
            print("❌ No encontrado")
            return

        print(f"Actual: {producto}")
        try:
            precio = float(input("Nuevo precio: $"))
            if self.inventario.actualizar_precio(id_prod, precio):
                print("✅ Actualizado")
            else:
                print("❌ Error")
        except ValueError:
            print("❌ Precio inválido")

    def _buscar_productos(self):
        print("\n🔍 BUSCAR PRODUCTOS")
        nombre = input("Nombre: ").strip()
        productos = self.inventario.buscar_por_nombre(nombre)

        if productos:
            print(f"\n✅ {len(productos)} encontrado(s):")
            for i, p in enumerate(productos, 1):
                print(f"{i}. {p}")
        else:
            print("❌ No encontrado")

    def _mostrar_todos(self):
        print("\n📋 TODOS LOS PRODUCTOS")
        productos = self.inventario.listar_todos()

        if productos:
            for i, p in enumerate(productos, 1):
                print(f"{i:2d}. {p}")
            print(f"\nValor total: ${self.inventario.valor_total():.2f}")
        else:
            print("❌ Sin productos")

    def _mostrar_estadisticas(self):
        print("\n📈 ESTADÍSTICAS")
        stats = self.inventario.estadisticas()

        if stats['total_productos'] > 0:
            print(f"📦 Productos: {stats['total_productos']}")
            print(f"📊 Items totales: {stats['total_items']}")
            print(f"💰 Valor total: ${stats['valor_total']:.2f}")
            print(f"⚠️  Sin stock: {stats['sin_stock']}")
            print(f"💵 Precio promedio: ${stats['precio_promedio']:.2f}")
        else:
            print("❌ Sin datos")

    def _mostrar_sin_stock(self):
        print("\n⚠️ PRODUCTOS SIN STOCK")
        productos = self.inventario.sin_stock()

        if productos:
            for i, p in enumerate(productos, 1):
                print(f"{i}. {p}")
        else:
            print("✅ Todos tienen stock")


# Función principal
def main():
    try:
        menu = Menu()
        menu.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico: {e}")


if __name__ == "__main__":
    main()