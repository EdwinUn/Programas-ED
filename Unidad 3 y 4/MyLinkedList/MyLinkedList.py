"""
Biblioteca MyLinkedList - Implementación de Linked List en Python
Author: Custom Implementation
Descripción: Implementación completa de una Lista Enlazada Simple con operaciones CRUD
"""


class Node:
    """
    Clase que representa un nodo en la lista enlazada.
    
    Atributos:
        data: El valor almacenado en el nodo
        next: Referencia al siguiente nodo
    """
    def __init__(self, data):
        """
        Constructor del nodo.
        
        Args:
            data: El valor a almacenar en el nodo
        """
        self.data = data
        self.next = None
    
    def __str__(self):
        return str(self.data)


class MyLinkedList:
    """
    Clase que implementa una Lista Enlazada Simple.
    
    Operaciones disponibles:
        - Insertar elementos (inicio, final, posición específica)
        - Eliminar elementos (por valor, por posición, inicio, final)
        - Buscar elementos
        - Recorrer la lista
        - Acceder a elementos por índice
    """
    
    def __init__(self):
        """Constructor de la lista enlazada."""
        self.head = None
        self._size = 0
    
    # ============ INSERCIÓN ============
    
    def insert_at_beginning(self, data):
        """
        Inserta un elemento al inicio de la lista.
        
        Args:
            data: El valor a insertar
        
        Time Complexity: O(1)
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def insert_at_end(self, data):
        """
        Inserta un elemento al final de la lista.
        
        Args:
            data: El valor a insertar
        
        Time Complexity: O(n)
        """
        new_node = Node(data)
        self._size += 1
        
        if self.head is None:
            self.head = new_node
            return
        
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
    
    def insert_at_position(self, data, position):
        """
        Inserta un elemento en una posición específica.
        
        Args:
            data: El valor a insertar
            position: La posición (0-based). Si position >= tamaño, inserta al final
        
        Raises:
            ValueError: Si position es negativa
        
        Time Complexity: O(n)
        """
        if position < 0:
            raise ValueError("La posición no puede ser negativa")
        
        new_node = Node(data)
        
        if position == 0:
            self.insert_at_beginning(data)
            return
        
        current = self.head
        previous = None
        current_position = 0
        
        while current is not None and current_position < position:
            previous = current
            current = current.next
            current_position += 1
        
        new_node.next = current
        if previous is not None:
            previous.next = new_node
        self._size += 1
    
    # ============ ELIMINACIÓN ============
    
    def delete_at_beginning(self):
        """
        Elimina el primer elemento de la lista.
        
        Returns:
            El valor eliminado, o None si la lista está vacía
        
        Time Complexity: O(1)
        """
        if self.head is None:
            return None
        
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
    
    def delete_at_end(self):
        """
        Elimina el último elemento de la lista.
        
        Returns:
            El valor eliminado, o None si la lista está vacía
        
        Time Complexity: O(n)
        """
        if self.head is None:
            return None
        
        if self.head.next is None:
            data = self.head.data
            self.head = None
            self._size -= 1
            return data
        
        current = self.head
        while current.next.next is not None:
            current = current.next
        
        data = current.next.data
        current.next = None
        self._size -= 1
        return data
    
    def delete_at_position(self, position):
        """
        Elimina un elemento en una posición específica.
        
        Args:
            position: La posición del elemento a eliminar (0-based)
        
        Returns:
            El valor eliminado, o None si la posición no existe
        
        Raises:
            ValueError: Si position es negativa
        
        Time Complexity: O(n)
        """
        if position < 0:
            raise ValueError("La posición no puede ser negativa")
        
        if self.head is None:
            return None
        
        if position == 0:
            return self.delete_at_beginning()
        
        current = self.head
        previous = None
        current_position = 0
        
        while current is not None and current_position < position:
            previous = current
            current = current.next
            current_position += 1
        
        if current is None:
            return None
        
        data = current.data
        previous.next = current.next
        self._size -= 1
        return data
    
    def delete_by_value(self, value):
        """
        Elimina la primera ocurrencia de un valor.
        
        Args:
            value: El valor a eliminar
        
        Returns:
            True si se eliminó, False si no se encontró
        
        Time Complexity: O(n)
        """
        if self.head is None:
            return False
        
        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next is not None:
            if current.next.data == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    # ============ BÚSQUEDA ============
    
    def search(self, value):
        """
        Busca un valor en la lista.
        
        Args:
            value: El valor a buscar
        
        Returns:
            True si se encuentra, False en caso contrario
        
        Time Complexity: O(n)
        """
        current = self.head
        while current is not None:
            if current.data == value:
                return True
            current = current.next
        return False
    
    def find_position(self, value):
        """
        Encuentra la posición de un valor.
        
        Args:
            value: El valor a buscar
        
        Returns:
            La posición (0-based) del valor, o -1 si no se encuentra
        
        Time Complexity: O(n)
        """
        current = self.head
        position = 0
        while current is not None:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1
    
    # ============ ACCESO ============
    
    def get_at_position(self, position):
        """
        Obtiene el valor en una posición específica.
        
        Args:
            position: La posición del elemento (0-based)
        
        Returns:
            El valor, o None si la posición no existe
        
        Time Complexity: O(n)
        """
        if position < 0:
            return None
        
        current = self.head
        current_position = 0
        
        while current is not None:
            if current_position == position:
                return current.data
            current = current.next
            current_position += 1
        
        return None
    
    # ============ INFORMACIÓN ============
    
    def size(self):
        """
        Retorna el tamaño de la lista.
        
        Returns:
            El número de elementos en la lista
        
        Time Complexity: O(1)
        """
        return self._size
    
    def is_empty(self):
        """
        Verifica si la lista está vacía.
        
        Returns:
            True si está vacía, False en caso contrario
        
        Time Complexity: O(1)
        """
        return self._size == 0 or self.head is None
    
    # ============ RECORRIDO ============
    
    def display(self):
        """
        Muestra todos los elementos de la lista.
        Formato: elemento1 -> elemento2 -> elemento3 -> None
        
        Time Complexity: O(n)
        """
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")
    
    def to_list(self):
        """
        Convierte la lista enlazada a una lista de Python.
        
        Returns:
            Una lista de Python con todos los elementos
        
        Time Complexity: O(n)
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    
    def __str__(self):
        """Representación en string de la lista."""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) + " -> None"
    
    def __len__(self):
        """Retorna el tamaño usando len()."""
        return self._size
    
    def __iter__(self):
        """Permite iterar sobre la lista."""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next
    
    def __getitem__(self, index):
        """Permite acceso por índice usando lista[i]."""
        if index < 0 or index >= self._size:
            raise IndexError(f"Índice {index} fuera de rango")
        return self.get_at_position(index)
    
    # ============ OPERACIONES AVANZADAS ============
    
    def reverse(self):
        """
        Invierte el orden de la lista.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        prev = None
        current = self.head
        
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self.head = prev
    
    def clear(self):
        """
        Elimina todos los elementos de la lista.
        
        Time Complexity: O(1) - solo resetea referencias
        """
        self.head = None
        self._size = 0
    
    def copy(self):
        """
        Crea una copia de la lista.
        
        Returns:
            Una nueva lista enlazada con copia de los elementos
        
        Time Complexity: O(n)
        """
        new_list = MyLinkedList()
        for data in self:
            new_list.insert_at_end(data)
        return new_list


# ============ FUNCIONES AUXILIARES ============

def merge_lists(list1, list2):
    """
    Fusiona dos listas enlazadas manteniendo el orden.
    
    Args:
        list1: Primera lista enlazada
        list2: Segunda lista enlazada
    
    Returns:
        Una nueva lista que contiene todos los elementos
    
    Time Complexity: O(n + m) donde n y m son los tamaños
    """
    merged = list1.copy()
    for item in list2:
        merged.insert_at_end(item)
    return merged


def has_cycle(linked_list):
    """
    Detecta si la lista tiene un ciclo (usando Floyd's Cycle Detection).
    
    Args:
        linked_list: La lista a verificar
    
    Returns:
        True si hay un ciclo, False en caso contrario
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if linked_list.head is None:
        return False
    
    slow = linked_list.head
    fast = linked_list.head
    
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False
