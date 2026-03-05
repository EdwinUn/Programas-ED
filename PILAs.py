import tkinter as tk
from tkinter import messagebox

class SimuladorPila:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pila (LIFO)")
        self.root.geometry("480x600") # Un poco más alto para los nuevos botones
        self.root.config(bg="#f0f0f0")

        # --- Propiedades de la Pila ---
        self.capacidad_maxima = 6
        self.pila = []

        # --- Interfaz Gráfica ---
        frame_controles = tk.Frame(root, bg="#f0f0f0")
        frame_controles.pack(pady=10)

        tk.Label(frame_controles, text="Elemento a insertar:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.entrada_elemento = tk.Entry(frame_controles, width=15)
        self.entrada_elemento.grid(row=0, column=1, padx=5)

        # Botones de Operaciones
        frame_botones = tk.Frame(root, bg="#f0f0f0")
        frame_botones.pack(pady=10)

        # Fila 0: Operaciones básicas
        tk.Button(frame_botones, text="Push (Insertar)", command=self.push, bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Pop (Quitar)", command=self.pop, bg="#F44336", fg="white", width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_botones, text="Peek (Ver Tope)", command=self.peek, bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5, pady=5)
        
        # Fila 1: Estados
        tk.Button(frame_botones, text="¿Está Llena?", command=self.is_full, bg="#FF9800", fg="white", width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="¿Está Vacía?", command=self.is_empty, bg="#9C27B0", fg="white", width=12).grid(row=1, column=1, padx=5, pady=5)
        
        # Fila 2: Nuevas funciones (Llenar y Vaciar)
        tk.Button(frame_botones, text="Llenar Pila", command=self.fill_stack, bg="#795548", fg="white", width=12).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Vaciar Pila", command=self.empty_stack, bg="#607D8B", fg="white", width=12).grid(row=2, column=1, padx=5, pady=5)

        # Canvas para dibujar la pila
        self.canvas = tk.Canvas(root, width=200, height=350, bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(pady=20)
        
        self.dibujar_pila()

    # --- Métodos de la Estructura PILA ---

    def push(self):
        elemento = self.entrada_elemento.get()
        if not elemento:
            messagebox.showwarning("Advertencia", "Por favor ingresa un elemento.")
            return

        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showerror("Error: Overflow", "La PILA ESTÁ LLENA. No puedes insertar más elementos.")
        else:
            self.pila.append(elemento)
            self.entrada_elemento.delete(0, tk.END)
            self.dibujar_pila()

    def pop(self):
        if len(self.pila) == 0:
            messagebox.showerror("Error: Underflow", "La PILA ESTÁ VACÍA. No hay nada que quitar.")
        else:
            elemento_removido = self.pila.pop()
            messagebox.showinfo("Pop", f"Elemento retirado: {elemento_removido}")
            self.dibujar_pila()

    def peek(self):
        if len(self.pila) == 0:
            messagebox.showinfo("Peek", "La pila está vacía, no hay tope.")
        else:
            tope = self.pila[-1]
            messagebox.showinfo("Peek (Tope)", f"El elemento en el tope es: {tope}")

    def is_full(self):
        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showinfo("Estado", "Sí, la pila está LLENA.")
        else:
            espacio = self.capacidad_maxima - len(self.pila)
            messagebox.showinfo("Estado", f"No, aún hay espacio para {espacio} elemento(s).")

    def is_empty(self):
        if len(self.pila) == 0:
            messagebox.showinfo("Estado", "Sí, la pila está VACÍA.")
        else:
            messagebox.showinfo("Estado", f"No, la pila tiene {len(self.pila)} elemento(s).")

    # --- Nuevos Métodos ---

    def fill_stack(self):
        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showinfo("Aviso", "La pila ya está llena.")
            return
        
        espacio_disponible = self.capacidad_maxima - len(self.pila)
        for i in range(espacio_disponible):
            # Genera un dato genérico para rellenar los huecos
            nuevo_dato = f"Auto {len(self.pila) + 1}"
            self.pila.append(nuevo_dato)
            
        self.dibujar_pila()
        messagebox.showinfo("Llenar Pila", "Se ha llenado la pila al máximo de su capacidad.")

    def empty_stack(self):
        if len(self.pila) == 0:
            messagebox.showinfo("Aviso", "La pila ya está vacía.")
            return
            
        # .clear() elimina todos los elementos de la lista en un solo paso
        self.pila.clear()
        self.dibujar_pila()
        messagebox.showinfo("Vaciar Pila", "Se han eliminado todos los elementos. La pila está vacía.")

    # --- Método para visualizar (Render) ---
    def dibujar_pila(self):
        self.canvas.delete("all")
        
        # Dibujar el contenedor
        self.canvas.create_line(10, 10, 10, 340, width=3) 
        self.canvas.create_line(10, 340, 190, 340, width=3) 
        self.canvas.create_line(190, 340, 190, 10, width=3) 

        # Dibujar los elementos apilados
        alto_bloque = 50
        ancho_bloque = 160
        x_inicial = 20
        y_base = 335

        for i, elemento in enumerate(self.pila):
            y_arriba = y_base - (i + 1) * alto_bloque
            y_abajo = y_base - i * alto_bloque
            
            self.canvas.create_rectangle(x_inicial, y_arriba, x_inicial + ancho_bloque, y_abajo, fill="#87CEFA", outline="black")
            self.canvas.create_text(x_inicial + (ancho_bloque/2), y_arriba + (alto_bloque/2), text=str(elemento), font=("Arial", 12, "bold"))

# --- Ejecución de la App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorPila(root)
    root.mainloop()