# Edwin Geovanni Un Uicab Grupo: 3SA

class NodoIngrediente:
    """Representa un nodo en la lista enlazada simple de ingredientes."""
    def __init__(self, ingrediente):
        self.info = ingrediente
        self.siguiente = None  # Apunta al siguiente nodo o a None (NIL)

# El arreglo principal "POSTRES".
POSTRES = []

# ==============================================================================
# FUNCIONES AUXILIARES (Para manipulación de las listas enlazadas)
# ==============================================================================

def buscar_postre(nombre_postre):
    """
    Busca un postre en el arreglo por su nombre.
    Retorna el índice si lo encuentra, -1 en caso contrario.
    """
    nombre_postre = nombre_postre.lower() # Normalizar para búsquedas
    for i in range(len(POSTRES)):
        if POSTRES[i]['nombre'].lower() == nombre_postre:
            return i
    return -1

def insertar_ingrediente_al_final(cabeza_lista, nuevo_ingrediente):
    """Inserta un nuevo nodo con el ingrediente al final de la lista enlazada."""
    nuevo_nodo = NodoIngrediente(nuevo_ingrediente)
    
    # Caso 1: La lista está vacía
    if cabeza_lista is None:
        return nuevo_nodo
    
    # Caso 2: Recorrer hasta el final
    actual = cabeza_lista
    while actual.siguiente is not None:
        # Verificación extra: evitar duplicar ingredientes en un mismo postre
        if actual.info.lower() == nuevo_ingrediente.lower():
            print(f"  Aviso: El ingrediente '{nuevo_ingrediente}' ya existe.")
            return cabeza_lista # No insertar
        actual = actual.siguiente
        
    # Doble verificación para el último elemento
    if actual.info.lower() == nuevo_ingrediente.lower():
        print(f"  Aviso: El ingrediente '{nuevo_ingrediente}' ya existe.")
        return cabeza_lista
        
    actual.siguiente = nuevo_nodo
    return cabeza_lista

def eliminar_ingrediente_de_lista(cabeza_lista, ingrediente_a_eliminar):
    """Elimina un ingrediente específico de la lista enlazada."""
    if cabeza_lista is None:
        print("  Error: La lista de ingredientes está vacía.")
        return None

    actual = cabeza_lista
    anterior = None
    encontrado = False

    # Buscar el nodo
    while actual is not None:
        if actual.info.lower() == ingrediente_a_eliminar.lower():
            encontrado = True
            break
        anterior = actual
        actual = actual.siguiente

    if not encontrado:
        print(f"  Error: El ingrediente '{ingrediente_a_eliminar}' no se encuentra en la lista.")
        return cabeza_lista

    # Proceder a la eliminación
    if anterior is None:
        # Es el primer nodo (la cabeza)
        print(f"  Ingrediente '{cabeza_lista.info}' eliminado con éxito (era la cabeza).")
        return actual.siguiente # La nueva cabeza es el siguiente elemento
    else:
        # Está en medio o al final
        print(f"  Ingrediente '{actual.info}' eliminado con éxito.")
        anterior.siguiente = actual.siguiente # Puente sobre el nodo a eliminar
        return cabeza_lista

# ==============================================================================
# PUNTO 1: PROGRAMA PRINCIPAL CON LAS OPERACIONES (A-E)
# ==============================================================================

def inicializar_datos_prueba():
    """Carga algunos datos para no empezar de cero."""
    # NOTA: Deben insertarse en orden alfabético para respetar la estructura
    dar_de_alta_postre("Flan", ["Leche", "Huevo", "Azúcar"])
    dar_de_alta_postre("Gelatina", ["Agua", "Polvo de sabor"])
    dar_de_alta_postre("Pastel", ["Harina", "Huevo", "Mantequilla", "Leche"])
    print("-" * 40)

# --- Operación a: Imprimir ingredientes ---
def imprimir_ingredientes(nombre_postre):
    print(f"\n--- Consultando ingredientes para: {nombre_postre} ---")
    
    # Verificación 1: Arreglo vacío
    if not POSTRES:
        print("Error: El arreglo de postres está totalmente vacío.")
        return

    indice = buscar_postre(nombre_postre)
    
    # Verificación 2: Postre no existe
    if indice == -1:
        print(f"Error: El postre '{nombre_postre}' no se encuentra registrado.")
        return

    # Si existe, recorrer la lista enlazada
    actual = POSTRES[indice]['cabeza']
    print(f"Ingredientes de {POSTRES[indice]['nombre']}:")
    
    # Verificación 3: Lista de ingredientes vacía
    if actual is None:
        print("  (La lista de ingredientes está vacía / NIL)")
        return

    while actual is not None:
        print(f"  - {actual.info}")
        actual = actual.siguiente

# --- Operación b: Insertar nuevos ingredientes ---
def insertar_nuevos_ingredientes(nombre_postre, lista_nuevos_ingredientes):
    print(f"\n--- Insertando ingredientes a: {nombre_postre} ---")
    
    indice = buscar_postre(nombre_postre)
    
    # Verificación: El postre debe existir para añadirle ingredientes
    if indice == -1:
        print(f"Error: No se puede insertar. El postre '{nombre_postre}' no existe.")
        return

    for ing in lista_nuevos_ingredientes:
        print(f"Intentando insertar: {ing}")
        POSTRES[indice]['cabeza'] = insertar_ingrediente_al_final(POSTRES[indice]['cabeza'], ing)

# --- Operación c: Eliminar ingrediente ---
def eliminar_un_ingrediente(nombre_postre, ingrediente_a_eliminar):
    print(f"\n--- Eliminando ingrediente '{ingrediente_a_eliminar}' de: {nombre_postre} ---")
    
    indice = buscar_postre(nombre_postre)
    if indice == -1:
        print(f"Error: El postre '{nombre_postre}' no existe.")
        return

    # La lógica detallada está en la función auxiliar
    POSTRES[indice]['cabeza'] = eliminar_ingrediente_de_lista(POSTRES[indice]['cabeza'], ingrediente_a_eliminar)

# --- Operación d: Dar de alta un postre ---
def dar_de_alta_postre(nombre_nuevo, lista_ingredientes_iniciales):
    print(f"\n--- Dando de alta postre: {nombre_nuevo} ---")
    
    # Verificación 1: El postre ya existe
    if buscar_postre(nombre_nuevo) != -1:
        print(f"Error: El postre '{nombre_nuevo}' ya existe en la estructura.")
        return

    # Crear la lista enlazada de ingredientes para este postre
    cabeza_ingredientes = None
    for ing in lista_ingredientes_iniciales:
        cabeza_ingredientes = insertar_ingrediente_al_final(cabeza_ingredientes, ing)

    nuevo_elemento = {
        'nombre': nombre_nuevo,
        'cabeza': cabeza_ingredientes
    }

    # Insertar manteniendo el ORDEN ALFABÉTICO (Crucial para esta estructura)
    # Se busca el índice correcto para insertar
    indice_insercion = 0
    while indice_insercion < len(POSTRES) and POSTRES[indice_insercion]['nombre'].lower() < nombre_nuevo.lower():
        indice_insercion += 1
    
    POSTRES.insert(indice_insercion, nuevo_elemento)
    print(f"Postre '{nombre_nuevo}' dado de alta exitosamente en la posición {indice_insercion}.")

# --- Operación e: Dar de baja un postre ---
def dar_de_baja_postre(nombre_postre):
    print(f"\n--- Dando de baja postre completo: {nombre_postre} ---")
    
    # Verificación 1: Arreglo vacío
    if not POSTRES:
        print("Error: No hay postres para dar de baja.")
        return

    indice = buscar_postre(nombre_postre)
    
    # Verificación 2: El postre no existe
    if indice == -1:
        print(f"Error: El postre '{nombre_postre}' no existe.")
        return

    # Antes de eliminar del arreglo, 'limpiamos' la memoria de la lista enlazada
    # (Aunque Python tiene recolector de basura, es buena práctica en E.D. simular la liberación)
    
    # Guardamos el nombre real (con mayúsculas/minúsculas originales) para el mensaje
    nombre_real = POSTRES[indice]['nombre']
    
    # "Eliminar" la lista enlazada (cortar la referencia a la cabeza)
    # Todos los nodos se vuelven inalcanzables.
    POSTRES[indice]['cabeza'] = None 
    print(f"  -> Lista de ingredientes de '{nombre_real}' liberada (NIL).")

    # Eliminar el elemento del arreglo principal
    eliminado = POSTRES.pop(indice)
    print(f"Postre '{eliminado['nombre']}' eliminado completamente del arreglo.")

def visualizar_estructura_completa():
    print("\n" + "="*50)
    print("      VISUALIZACIÓN DE LA ESTRUCTURA 'POSTRES'")
    print("="*50)
    if not POSTRES:
        print("[ Estructura totalmente vacía ]")
    else:
        for i, postre_dict in enumerate(POSTRES):
            print(f"[{i}] Postre: {postre_dict['nombre']}")
            actual = postre_dict['cabeza']
            print("    -> Lista Ingredientes: ", end="")
            if actual is None:
                print("NIL")
            else:
                while actual is not None:
                    print(f"[{actual.info}]", end=" -> ")
                    actual = actual.siguiente
                print("NIL")
    print("="*50 + "\n")

# ==============================================================================
# EJECUCIÓN DEL PUNTO 1
# ==============================================================================

# 1. Cargar datos base
inicializar_datos_prueba()
visualizar_estructura_completa()

# a. Consultar ingredientes (Caso normal y caso error)
imprimir_ingredientes("Flan")
imprimir_ingredientes("Tiramisú") # Error, no existe

# b. Insertar ingredientes (Caso normal y caso repetido)
insertar_nuevos_ingredientes("Flan", ["Vainilla", "Leche"]) # Leche está repetida, no debe entrar

# Verificamos
imprimir_ingredientes("Flan")

# c. Eliminar ingrediente (Caso cabeza, caso medio, caso no existe)
eliminar_un_ingrediente("Flan", "Leche")       # Es la cabeza original
eliminar_un_ingrediente("Gelatina", "Piedras") # No existe

# Verificamos
visualizar_estructura_completa()

# d. Dar de alta nuevo postre (Verificar orden alfabético)
# Crepas debe ir antes de Flan
dar_de_alta_postre("Crepas", ["Harina", "Leche", "Cajeta"]) 

# Verificamos el orden
visualizar_estructura_completa()

# e. Dar de baja un postre
dar_de_baja_postre("Pastel")

# Verificamos final
visualizar_estructura_completa()


# ==============================================================================
# PUNTO 2: SUBPROGRAMA DE ELIMINACIÓN DE REPETIDOS
# ==============================================================================

def eliminar_postres_repetidos_automaticamente():
    """
    Subprograma solicitado en el punto 2.
    Detecta postres con nombres duplicados en el arreglo y los elimina.
    
    Analizando la estructura: Al ser un arreglo ordenado alfabéticamente,
    los elementos repetidos SIEMPRE estarán contiguos (uno al lado del otro).
    Ejemplo: [... , "Flan", "Flan", "Gelatina", ...]
    """
    print("\n" + "#"*60)
    print("EJECUTANDO PUNTO 2: ELIMINACIÓN AUTOMÁTICA DE REPETIDOS")
    print("#"*60)
    
    if len(POSTRES) < 2:
        print("La estructura tiene menos de 2 elementos. No puede haber repetidos.")
        return

    # Usamos un índice para recorrer. Es mejor recorrer al revés cuando
    # se eliminan elementos de una lista mientras se itera para no saltarse índices.
    # O, en este caso, controlar manualmente el avance.
    
    i = 0
    eliminaciones_realizadas = 0
    
    # Recorremos hasta el penúltimo elemento
    while i < len(POSTRES) - 1:
        # Comparamos el actual con el siguiente (normalizando a minúsculas)
        nombre_actual = POSTRES[i]['nombre'].lower()
        nombre_siguiente = POSTRES[i+1]['nombre'].lower()
        
        if nombre_actual == nombre_siguiente:
            # Encontramos un duplicado contiguo.
            # Decidimos eliminar el elemento en i+1 (el segundo).
            print(f"Repetido detectado: Se encontró '{POSTRES[i+1]['nombre']}' en posiciones contiguas {i} y {i+1}.")
            
            # --- Aquí está la parte clave para la segunda pregunta ---
            # Antes de 'poppear' el elemento del arreglo, "desenganchamos" su lista enlazada.
            POSTRES[i+1]['cabeza'] = None
            print(f"  -> Lista de ingredientes del repetido liberada (NIL).")
            
            # Eliminamos del arreglo
            POSTRES.pop(i+1)
            eliminaciones_realizadas += 1
            
            # IMPORTANTE: NO incrementamos 'i'. En la próxima iteración,
            # el elemento en 'i' se comparará con el *nuevo* elemento que 
            # ocupó la posición 'i+1', por si había 3 repetidos seguidos.
        else:
            # No son iguales, avanzamos al siguiente par
            i += 1
            
    print(f"\nOperación finalizada. Se eliminaron {eliminaciones_realizadas} postres repetidos.")


print("\n(Forzando duplicados para la prueba del Punto 2)...")
# Duplicamos Gelatina (la lista de ingredientes es la misma referencia, para simplicidad de la prueba)
copia_gelatina = {'nombre': 'Gelatina', 'cabeza': POSTRES[buscar_postre("Gelatina")]['cabeza']}
POSTRES.insert(buscar_postre("Gelatina"), copia_gelatina)

# Duplicamos Flan (haciendo una copia real de la lista para mostrar que no importa)
original_flan_cabeza = POSTRES[buscar_postre("Flan")]['cabeza']
nueva_cabeza_flan = NodoIngrediente(original_flan_cabeza.info)
# (Saltamos copiar el resto de la lista para esta prueba rápida)
copia_flan = {'nombre': 'Flan', 'cabeza': nueva_cabeza_flan}
POSTRES.insert(buscar_postre("Flan"), copia_flan)

visualizar_estructura_completa() # Debería mostrar Flan y Gelatina repetidos

# Ejecutar el subprograma solicitado
eliminar_postres_repetidos_automaticamente()

# Verificación Final
visualizar_estructura_completa()