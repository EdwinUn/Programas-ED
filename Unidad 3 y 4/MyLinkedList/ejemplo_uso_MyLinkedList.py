"""
Ejemplos de uso de la biblioteca MyLinkedList
Demuestra todas las operaciones principales de la Lista Enlazada
"""

from MyLinkedList import MyLinkedList, merge_lists, has_cycle


def main():
    print("=" * 60)
    print("EJEMPLOS DE USO - MyLinkedList")
    print("=" * 60)
    
    # ============ CREACIÓN Y INSERCIÓN ============
    print("\n1. CREACIÓN E INSERCIÓN")
    print("-" * 60)
    
    lista = MyLinkedList()
    
    print("• Insertando 5, 3, 8 al final:")
    lista.insert_at_end(5)
    lista.insert_at_end(3)
    lista.insert_at_end(8)
    lista.display()
    
    print("\n• Insertando 10 al inicio:")
    lista.insert_at_beginning(10)
    lista.display()
    
    print("\n• Insertando 6 en la posición 2:")
    lista.insert_at_position(6, 2)
    lista.display()
    
    # ============ INFORMACIÓN ============
    print("\n2. INFORMACIÓN DE LA LISTA")
    print("-" * 60)
    print(f"• Tamaño: {lista.size()}")
    print(f"• ¿Está vacía?: {lista.is_empty()}")
    print(f"• Lista como Python list: {lista.to_list()}")
    print(f"• Usando __len__(): {len(lista)}")
    
    # ============ BÚSQUEDA ============
    print("\n3. BÚSQUEDA")
    print("-" * 60)
    print(f"• ¿Existe el valor 6?: {lista.search(6)}")
    print(f"• ¿Existe el valor 99?: {lista.search(99)}")
    print(f"• Posición del valor 8: {lista.find_position(8)}")
    print(f"• Posición del valor 3: {lista.find_position(3)}")
    
    # ============ ACCESO POR ÍNDICE ============
    print("\n4. ACCESO POR ÍNDICE")
    print("-" * 60)
    print(f"• Elemento en posición 0: {lista.get_at_position(0)}")
    print(f"• Elemento en posición 2: {lista.get_at_position(2)}")
    print(f"• Usando lista[1]: {lista[1]}")
    print(f"• Usando lista[3]: {lista[3]}")
    
    # ============ ITERACIÓN ============
    print("\n5. ITERACIÓN")
    print("-" * 60)
    print("• Iterando con for:")
    for elemento in lista:
        print(f"  - {elemento}")
    
    # ============ ELIMINACIÓN ============
    print("\n6. ELIMINACIÓN")
    print("-" * 60)
    
    print(f"• Lista actual: {lista}")
    print(f"• Tamaño: {lista.size()}")
    
    print("\n• Eliminando inicio (primera ocurrencia):")
    eliminado = lista.delete_at_beginning()
    print(f"  Eliminado: {eliminado}")
    lista.display()
    print(f"  Tamaño: {lista.size()}")
    
    print("\n• Eliminando final:")
    eliminado = lista.delete_at_end()
    print(f"  Eliminado: {eliminado}")
    lista.display()
    print(f"  Tamaño: {lista.size()}")
    
    print("\n• Eliminando en posición 1:")
    eliminado = lista.delete_at_position(1)
    print(f"  Eliminado: {eliminado}")
    lista.display()
    print(f"  Tamaño: {lista.size()}")
    
    print("\n• Eliminando por valor (6):")
    fue_eliminado = lista.delete_by_value(6)
    print(f"  ¿Se eliminó?: {fue_eliminado}")
    lista.display()
    
    # ============ OPERACIONES AVANZADAS ============
    print("\n7. OPERACIONES AVANZADAS")
    print("-" * 60)
    
    # Crear nueva lista para reversión
    lista_invertir = MyLinkedList()
    lista_invertir.insert_at_end(1)
    lista_invertir.insert_at_end(2)
    lista_invertir.insert_at_end(3)
    lista_invertir.insert_at_end(4)
    
    print(f"• Lista original: {lista_invertir}")
    lista_invertir.reverse()
    print(f"• Lista invertida: {lista_invertir}")
    
    # Copiar lista
    print("\n• Copiando lista:")
    lista_copia = lista_invertir.copy()
    print(f"  Original: {lista_invertir}")
    print(f"  Copia: {lista_copia}")
    lista_copia.insert_at_end(5)
    print(f"  Después de agregar 5 a copia:")
    print(f"    Original: {lista_invertir}")
    print(f"    Copia: {lista_copia}")
    
    # ============ FUSIÓN DE LISTAS ============
    print("\n8. FUSIÓN DE LISTAS")
    print("-" * 60)
    
    lista_a = MyLinkedList()
    lista_a.insert_at_end(1)
    lista_a.insert_at_end(2)
    lista_a.insert_at_end(3)
    
    lista_b = MyLinkedList()
    lista_b.insert_at_end(4)
    lista_b.insert_at_end(5)
    
    print(f"• Lista A: {lista_a}")
    print(f"• Lista B: {lista_b}")
    
    lista_fusionada = merge_lists(lista_a, lista_b)
    print(f"• Lista fusionada: {lista_fusionada}")
    
    # ============ DETECCIÓN DE CICLOS ============
    print("\n9. DETECCIÓN DE CICLOS")
    print("-" * 60)
    
    lista_sin_ciclo = MyLinkedList()
    lista_sin_ciclo.insert_at_end(1)
    lista_sin_ciclo.insert_at_end(2)
    lista_sin_ciclo.insert_at_end(3)
    
    print(f"• ¿Tiene ciclo?: {has_cycle(lista_sin_ciclo)}")
    
    # ============ LIMPIAR ============
    print("\n10. LIMPIAR LISTA")
    print("-" * 60)
    
    print(f"• Antes: {lista_fusionada} (tamaño: {len(lista_fusionada)})")
    lista_fusionada.clear()
    print(f"• Después: {lista_fusionada} (tamaño: {len(lista_fusionada)})")
    print(f"• ¿Está vacía?: {lista_fusionada.is_empty()}")
    
    print("\n" + "=" * 60)
    print("FIN DE LOS EJEMPLOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
