import os

class Node:
    def __init__(self, customer, quantity):
        self.customer = customer
        self.quantity = quantity
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0
        self.buffer_undo = None 

    def is_empty(self):
        return self.first is None

    def enqueue(self, customer, quantity):
        new_node = Node(customer, quantity)
        if self.is_empty():
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        self.buffer_undo = self.first
        self.first = self.first.next
        if self.first is None:
            self.last = None
        self.size -= 1
        return self.buffer_undo

    def remove_last(self):
        """Elimina el último nodo de la cola"""
        if self.is_empty():
            return None
        
        self.buffer_undo = self.last
        
        if self.size == 1:
            self.first = None
            self.last = None
        else:
            # Necesitamos buscar al penúltimo
            current = self.first
            while current.next != self.last:
                current = current.next
            
            # El penúltimo ahora es el último
            current.next = None
            self.last = current
            
        self.size -= 1
        return self.buffer_undo

    def remove_by_name(self, name):
        current = self.first
        prev = None
        while current is not None:
            if current.customer == name:
                self.buffer_undo = current
                if prev is None:
                    self.first = current.next
                else:
                    prev.next = current.next
                if current.next is None:
                    self.last = prev
                self.size -= 1
                return True
            prev = current
            current = current.next
        return False

    def undo(self):
        if self.buffer_undo:
            self.enqueue(self.buffer_undo.customer, self.buffer_undo.quantity)
            temp_name = self.buffer_undo.customer
            self.buffer_undo = None 
            return temp_name
        return None

    def dump(self):
        print("\n********* QUEUE DUMP *********")
        print(f"   Size: {self.size}")
        if self.is_empty():
            print("   (La cola está vacía)")
        else:
            current = self.first
            idx = 1
            while current:
                print(f"   ** Element {idx}")
                print(f"     Customer: {current.customer}")
                print(f"     Quantity: {current.quantity}")
                print(f"     ------------")
                current = current.next
                idx += 1
        print("******************************")

def run_app():
    q = LinkedListQueue()

    while True:
        q.dump()
        print("\nMENÚ DE GESTIÓN:")
        print("1. Agregar N clientes")
        print("2. Atender primero (Dequeue)")
        print("3. Eliminar cliente específico")
        print("4. Eliminar el ÚLTIMO de la cola")
        print("5. Deshacer última eliminación (Undo)")
        print("6. Salir")
        
        choice = input("\nSeleccione una opción: ")

        if choice == "1":
            try:
                n = int(input("¿Cuántos clientes desea agregar?: "))
                for i in range(n):
                    name = input(f"[{i+1}] Nombre del cliente: ")
                    qty = input(f"[{i+1}] Cantidad: ")
                    q.enqueue(name, qty)
            except ValueError:
                print("⚠️ Error: Ingrese un número válido.")
        
        elif choice == "2":
            if q.is_empty():
                print("\n❌ Error: Cola vacía.")
            else:
                res = q.dequeue()
                confirm = input(f"Se eliminará a '{res.customer}'. ¿Arrepentido? (s/n): ")
                if confirm.lower() == 's':
                    q.undo()
                    print("Operación revertida.")
        
        elif choice == "3":
            if q.is_empty():
                print("\n❌ Error: Cola vacía.")
            else:
                name = input("Nombre del cliente a eliminar: ")
                if q.remove_by_name(name):
                    confirm = input(f"¿Seguro que quieres borrar a {name}? (s/n): ")
                    if confirm.lower() != 's':
                        q.undo()
                        print("Eliminación revertida.")
                    else:
                        print(f"✅ '{name}' eliminado.")
                else:
                    print(f"❌ No encontrado.")

        elif choice == "4":
            if q.is_empty():
                print("\n❌ Error: No hay nadie al final para eliminar.")
            else:
                res = q.remove_last()
                confirm = input(f"Se eliminará el último: '{res.customer}'. ¿Arrepentido? (s/n): ")
                if confirm.lower() == 's':
                    q.undo()
                    print("Operación revertida.")
                else:
                    print(f"✅ Último elemento eliminado.")

        elif choice == "5":
            restored = q.undo()
            if restored:
                print(f"✅ Se ha restaurado a: {restored}")
            else:
                print("⚠️ Nada que deshacer.")

        elif choice == "6":
            break
        
        input("\nPresione Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    run_app()