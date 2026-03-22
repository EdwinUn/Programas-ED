import os
from typing import Optional, List


# ==================== CLASE NODO INGREDIENTE ====================
class NodoIngrediente:
    """
    Representa un nodo en la lista vinculada de ingredientes.
    Cada nodo contiene el nombre del ingrediente y una referencia al siguiente nodo.
    """
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.siguiente: Optional['NodoIngrediente'] = None

    def __repr__(self) -> str:
        return f"NodoIngrediente({self.nombre})"


# ==================== CLASE POSTRE ====================
class Postre:
    """
    Representa un postre con su nombre y una lista vinculada de ingredientes.
    """
    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.lista_ingredientes: Optional[NodoIngrediente] = None

    def __repr__(self) -> str:
        cant_ingredientes = self._contar_ingredientes()
        return f"Postre({self.nombre}, {cant_ingredientes} ingredientes)"

    def _contar_ingredientes(self) -> int:
        """Cuenta la cantidad de ingredientes en la lista vinculada."""
        contador = 0
        nodo_actual = self.lista_ingredientes
        while nodo_actual is not None:
            contador += 1
            nodo_actual = nodo_actual.siguiente
        return contador

    def agregar_ingrediente_al_final(self, nombre_ingrediente: str) -> bool:
        """
        Agrega un ingrediente al final de la lista vinculada.
        Retorna True si se agregó, False si ya existe.
        """
        nombre_ingrediente = nombre_ingrediente.strip()
        if not nombre_ingrediente:
            return False

        # Verificar si ya existe
        if self._existe_ingrediente(nombre_ingrediente):
            return False

        nuevo_nodo = NodoIngrediente(nombre_ingrediente)

        # Si la lista está vacía, el nuevo nodo es el primero
        if self.lista_ingredientes is None:
            self.lista_ingredientes = nuevo_nodo
            return True

        # Buscar el último nodo
        nodo_actual = self.lista_ingredientes
        while nodo_actual.siguiente is not None:
            nodo_actual = nodo_actual.siguiente

        # Agregar el nuevo nodo al final
        nodo_actual.siguiente = nuevo_nodo
        return True

    def eliminar_ingrediente(self, nombre_ingrediente: str) -> bool:
        """
        Elimina un ingrediente de la lista vinculada.
        Retorna True si se eliminó, False si no existe.
        """
        nombre_ingrediente = nombre_ingrediente.strip()

        # Si el nodo a eliminar es el primero
        if self.lista_ingredientes is not None and \
           self.lista_ingredientes.nombre.lower() == nombre_ingrediente.lower():
            self.lista_ingredientes = self.lista_ingredientes.siguiente
            return True

        # Buscar el nodo anterior al que queremos eliminar
        nodo_actual = self.lista_ingredientes
        while nodo_actual is not None and nodo_actual.siguiente is not None:
            if nodo_actual.siguiente.nombre.lower() == nombre_ingrediente.lower():
                nodo_actual.siguiente = nodo_actual.siguiente.siguiente
                return True
            nodo_actual = nodo_actual.siguiente

        return False

    def _existe_ingrediente(self, nombre_ingrediente: str) -> bool:
        """Verifica si un ingrediente existe en la lista vinculada."""
        nodo_actual = self.lista_ingredientes
        while nodo_actual is not None:
            if nodo_actual.nombre.lower() == nombre_ingrediente.lower():
                return True
            nodo_actual = nodo_actual.siguiente
        return False

    def obtener_ingredientes(self) -> List[str]:
        """Retorna una lista con los nombres de todos los ingredientes."""
        ingredientes = []
        nodo_actual = self.lista_ingredientes
        while nodo_actual is not None:
            ingredientes.append(nodo_actual.nombre)
            nodo_actual = nodo_actual.siguiente
        return ingredientes


# ==================== CLASE SISTEMA POSTRES ====================
class SistemaPostres:
    """
    Gestiona un arreglo de postres (POSTRES) mantenido en orden alfabético.
    Cada postre contiene una lista vinculada de ingredientes.
    """
    def __init__(self) -> None:
        self.POSTRES: List[Postre] = []

    def buscar_postre(self, nombre: str) -> Optional[Postre]:
        """Busca un postre por nombre (case-insensitive)."""
        for postre in self.POSTRES:
            if postre.nombre.lower() == nombre.lower():
                return postre
        return None

    # ========== PUNTO A: IMPRIMIR INGREDIENTES ==========
    def imprimir_ingredientes(self, nombre_postre: str) -> None:
        """
        Busca el postre y recorre su lista vinculada para imprimir cada ingrediente.
        Implementación del punto (a).
        """
        postre = self.buscar_postre(nombre_postre)
        if postre is None:
            print(f"[ERROR] El postre '{nombre_postre}' no existe.")
            return

        ingredientes = postre.obtener_ingredientes()
        if not ingredientes:
            print(f"\n[ADVERTENCIA] El postre '{postre.nombre}' no tiene ingredientes.\n")
            return

        print(f"\n{'='*50}")
        print(f"Ingredientes de '{postre.nombre}':")
        print(f"{'='*50}")
        for i, ing in enumerate(ingredientes, 1):
            print(f"  {i}. {ing}")
        print(f"Total: {len(ingredientes)} ingrediente(s)")
        print(f"{'='*50}\n")

    # ========== PUNTO B: INSERTAR INGREDIENTE ==========
    def insertar_ingrediente(self, nombre_postre: str, nuevo_ingrediente: str) -> None:
        """
        Añade un ingrediente al final de la lista vinculada del postre.
        Implementación del punto (b).
        """
        postre = self.buscar_postre(nombre_postre)
        if postre is None:
            print(f"[ERROR] El postre '{nombre_postre}' no existe.")
            return

        if postre.agregar_ingrediente_al_final(nuevo_ingrediente):
            print(f"[OK] Ingrediente '{nuevo_ingrediente}' insertado en '{nombre_postre}'.")
        else:
            print(f"[ADVERTENCIA] Ingrediente '{nuevo_ingrediente}' ya existe o está vacío.")

    # ========== PUNTO C: ELIMINAR INGREDIENTE ==========
    def eliminar_ingrediente(self, nombre_postre: str, ingrediente: str) -> None:
        """
        Elimina un nodo específico de la lista de ingredientes del postre.
        Implementación del punto (c).
        """
        postre = self.buscar_postre(nombre_postre)
        if postre is None:
            print(f"[ERROR] El postre '{nombre_postre}' no existe.")
            return

        if postre.eliminar_ingrediente(ingrediente):
            print(f"[OK] Ingrediente '{ingrediente}' eliminado de '{nombre_postre}'.")
        else:
            print(f"[ERROR] Ingrediente '{ingrediente}' no estaba en '{nombre_postre}'.")

    # ========== PUNTO D: ALTA POSTRE ==========
    def alta_postre(self, nombre_postre: str, lista_nombres_ingredientes: Optional[List[str]] = None) -> None:
        """
        Inserta un objeto Postre en el arreglo POSTRES.
        El arreglo se mantiene ordenado alfabéticamente tras cada inserción.
        Implementación del punto (d).
        """
        nombre_postre = nombre_postre.strip()
        if not nombre_postre:
            print("[ERROR] El nombre del postre no puede estar vacío.")
            return

        if self.buscar_postre(nombre_postre) is not None:
            print(f"[ERROR] El postre '{nombre_postre}' ya existe.")
            return

        # Crear nuevo postre
        nuevo_postre = Postre(nombre_postre)

        # Agregar ingredientes si se proporcionan
        if lista_nombres_ingredientes:
            for ingrediente in lista_nombres_ingredientes:
                nuevo_postre.agregar_ingrediente_al_final(ingrediente)

        # Insertar en el arreglo manteniendo orden alfabético
        self.POSTRES.append(nuevo_postre)
        self.POSTRES.sort(key=lambda p: p.nombre.lower())
        print(f"[OK] Postre '{nombre_postre}' agregado correctamente.")

    # ========== PUNTO E: BAJA POSTRE ==========
    def baja_postre(self, nombre_postre: str) -> None:
        """
        Elimina el postre del arreglo POSTRES.
        Implementación del punto (e).
        """
        postre = self.buscar_postre(nombre_postre)
        if postre is None:
            print(f"[ERROR] El postre '{nombre_postre}' no existe.")
            return

        confirmacion = input(f"¿Eliminar postre '{nombre_postre}' y todos sus ingredientes? (S/N): ").lower()
        if confirmacion == 's':
            self.POSTRES.remove(postre)
            print(f"[OK] Postre '{nombre_postre}' eliminado.")
        else:
            print("[CANCELADO] Operación cancelada.")

    # ========== PUNTO EJERCICIO 2: ELIMINAR REPETIDOS ==========
    def eliminar_repetidos(self) -> None:
        if not self.POSTRES:
            print("[INFO] No hay postres para procesar.")
            return

        nombres_vistos = {}
        postres_a_eliminar = []

        # Identificar postres duplicados (por nombre)
        for postre in self.POSTRES:
            nombre_lower = postre.nombre.lower()
            if nombre_lower in nombres_vistos:
                postres_a_eliminar.append(postre)
            else:
                nombres_vistos[nombre_lower] = postre

        # Eliminar los duplicados
        if postres_a_eliminar:
            for postre in postres_a_eliminar:
                self.POSTRES.remove(postre)
                # En este punto, si no hay otras referencias a 'postre' ni a 'postre.lista_ingredientes',
                # Python libera automáticamente la memoria de toda la estructura
            print(f"[OK] Se eliminaron {len(postres_a_eliminar)} postre(s) repetido(s).")
        else:
            print("[INFO] No había postres repetidos.")

    def listar_todos_postres(self) -> None:
        """Lista todos los postres registrados con su cantidad de ingredientes."""
        if not self.POSTRES:
            print("\n[ADVERTENCIA] No hay postres registrados.\n")
            return

        print(f"\n{'='*50}")
        print(f"Total de postres registrados: {len(self.POSTRES)}")
        print(f"{'='*50}")
        for i, postre in enumerate(self.POSTRES, 1):
            cant_ing = postre._contar_ingredientes()
            print(f"  {i}. {postre.nombre} - {cant_ing} ingrediente(s)")
        print(f"{'='*50}\n")

    def estadisticas(self) -> None:
        """Muestra estadísticas del sistema."""
        if not self.POSTRES:
            print("\n[ADVERTENCIA] No hay datos para mostrar estadísticas.\n")
            return

        total_postres = len(self.POSTRES)
        total_ingredientes = sum(p._contar_ingredientes() for p in self.POSTRES)
        promedio = total_ingredientes / total_postres if total_postres > 0 else 0

        print(f"\n{'='*50}")
        print(f"ESTADÍSTICAS DEL SISTEMA")
        print(f"{'='*50}")
        print(f"  • Total de postres: {total_postres}")
        print(f"  • Total de ingredientes: {total_ingredientes}")
        print(f"  • Promedio por postre: {promedio:.2f}")
        if total_postres > 0:
            postre_max = max(self.POSTRES, key=lambda p: p._contar_ingredientes())
            print(f"  • Postre con más ingredientes: {postre_max.nombre} ({postre_max._contar_ingredientes()} ingredientes)")
        print(f"{'='*50}\n")


# ==================== FUNCIONES DE INTERFAZ ====================
def limpiar_pantalla() -> None:
    """Limpia la pantalla del terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu() -> None:
    """Muestra el menú principal."""
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE POSTRES (Lista de Listas)")
    print("="*50)
    print("1. Imprimir ingredientes de un postre")
    print("2. Insertar ingrediente a un postre")
    print("3. Eliminar ingrediente de un postre")
    print("4. Dar de alta un postre")
    print("5. Dar de baja un postre")
    print("6. Ver todos los postres")
    print("7. Ver estadísticas")
    print("8. Eliminar postres repetidos")
    print("9. Salir")
    print("="*50)


def cargar_datos_iniciales(sistema: SistemaPostres) -> None:
    """Carga datos iniciales en el sistema."""
    datos = [
        ("Brownie", ["Chocolate", "Harina", "Huevo", "Mantequilla", "Azúcar"]),
        ("Cheesecake", ["Queso Crema", "Galletas", "Mantequilla", "Azúcar", "Huevo"]),
        ("Flan", ["Azúcar", "Huevo", "Leche", "Vainilla"]),
        ("Helado", ["Crema de Leche", "Leche", "Azúcar", "Vainilla"]),
        ("Mousse de Chocolate", ["Chocolate", "Crema de Leche", "Huevo", "Azúcar"]),
        ("Tiramisu", ["Café", "Mascarpone", "Huevo", "Azúcar", "Cacao", "Galletas de Soda"]),
    ]

    for nombre_postre, ingredientes in datos:
        sistema.alta_postre(nombre_postre, ingredientes)

    print("\n[INFO] Datos iniciales cargados: 6 postres con ingredientes.\n")
    input("Presiona Enter para continuar...")


def menu_interactivo() -> None:
    """Menú interactivo principal."""
    sistema = SistemaPostres()

    # Cargar datos iniciales
    limpiar_pantalla()
    print("\n" + "="*50)
    print("Cargando datos iniciales...")
    print("="*50)
    cargar_datos_iniciales(sistema)

    # Funciones para cada opción del menú
    def opcion_1():
        """Imprimir ingredientes de un postre."""
        nombre = input("Nombre del postre: ").strip()
        sistema.imprimir_ingredientes(nombre)

    def opcion_2():
        """Insertar ingrediente a un postre."""
        nombre = input("Nombre del postre: ").strip()
        ingrediente = input("Nombre del ingrediente: ").strip()
        sistema.insertar_ingrediente(nombre, ingrediente)

    def opcion_3():
        """Eliminar ingrediente de un postre."""
        nombre = input("Nombre del postre: ").strip()
        ingrediente = input("Nombre del ingrediente a eliminar: ").strip()
        sistema.eliminar_ingrediente(nombre, ingrediente)

    def opcion_4():
        """Dar de alta un postre."""
        nombre = input("Nombre del nuevo postre: ").strip()
        print("Ingresa ingredientes (escribe 'listo' cuando termines):")
        ingredientes = []
        while True:
            ing = input("  Ingrediente: ").strip()
            if ing.lower() == 'listo':
                break
            if ing:
                ingredientes.append(ing)
        sistema.alta_postre(nombre, ingredientes if ingredientes else None)

    def opcion_5():
        """Dar de baja un postre."""
        nombre = input("Nombre del postre a eliminar: ").strip()
        sistema.baja_postre(nombre)

    def opcion_6():
        """Ver todos los postres."""
        sistema.listar_todos_postres()

    def opcion_7():
        """Ver estadísticas."""
        sistema.estadisticas()

    def opcion_8():
        """Eliminar postres repetidos."""
        sistema.eliminar_repetidos()

    # Mapeo de opciones a funciones
    opciones = {
        '1': opcion_1,
        '2': opcion_2,
        '3': opcion_3,
        '4': opcion_4,
        '5': opcion_5,
        '6': opcion_6,
        '7': opcion_7,
        '8': opcion_8,
    }

    # Loop principal
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Selecciona una opción (1-9): ").strip()

        if opcion == '9':
            limpiar_pantalla()
            print("\n[OK] ¡Hasta luego!\n")
            break
        
        if opcion in opciones:
            limpiar_pantalla()
            opciones[opcion]()
        else:
            print("[ERROR] Opción no válida.")
        
        input("Presiona Enter para continuar...")


# ==================== BLOQUE PRINCIPAL ====================
if __name__ == "__main__":
    menu_interactivo()
