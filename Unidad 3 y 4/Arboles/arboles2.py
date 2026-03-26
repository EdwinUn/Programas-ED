import tkinter as tk
from tkinter import messagebox, simpledialog

# ------------------------
# CLASE NODO
# ------------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        # Coordenadas para detectar clics en el dibujo
        self.x = 0
        self.y = 0

# Variables globales
raiz = None
nodo_seleccionado = None

# ------------------------
# LÓGICA DEL ÁRBOL
# ------------------------
def obtener_valores(nodo):
    if nodo is None: return []
    return [nodo.valor] + obtener_valores(nodo.izq) + obtener_valores(nodo.der)

def buscar_por_coordenadas(nodo, px, py):
    if nodo is None: return None
    # Detectar si el clic está dentro del radio del círculo (18px)
    if (px - nodo.x)**2 + (py - nodo.y)**2 <= 18**2:
        return nodo
    return buscar_por_coordenadas(nodo.izq, px, py) or buscar_por_coordenadas(nodo.der, px, py)

def eliminar_nodo_recursivo(padre, actual, valor_a_borrar):
    if actual is None: return False
    if actual.valor == valor_a_borrar:
        if padre is None:
            global raiz
            raiz = None
        elif padre.izq == actual:
            padre.izq = None
        else:
            padre.der = None
        return True
    return eliminar_nodo_recursivo(actual, actual.izq, valor_a_borrar) or \
           eliminar_nodo_recursivo(actual, actual.der, valor_a_borrar)

# ------------------------
# FUNCIONES DE UI / BOTONES
# ------------------------
def seleccionar_nodo(event):
    global nodo_seleccionado
    nodo = buscar_por_coordenadas(raiz, event.x, event.y)
    if nodo:
        nodo_seleccionado = nodo
        status_label.config(text=f"Seleccionado: {nodo.valor}", fg="blue")
    else:
        nodo_seleccionado = None
        status_label.config(text="Haz clic en un círculo para seleccionar", fg="black")
    dibujar()

def insertar(lado):
    global raiz, nodo_seleccionado
    
    # MEJORA: Si no hay raíz, ignoramos "izq/der" y creamos el origen
    if raiz is None:
        valor = simpledialog.askinteger("Inicio", "El árbol está vacío. Ingresa el valor de la RAÍZ:")
        if valor is not None:
            raiz = Nodo(valor)
            dibujar()
        return

    # Si ya hay raíz, FORZAMOS a que seleccione un padre
    if nodo_seleccionado is None:
        messagebox.showwarning("Atención", "Haz clic en un nodo del dibujo para usarlo como padre.")
        return

    valor = simpledialog.askinteger("Nuevo Nodo", f"Valor para el hijo {lado} de {nodo_seleccionado.valor}:")
    if valor is None: return
    
    if valor in obtener_valores(raiz):
        messagebox.showerror("Error", "Ese valor ya existe.")
        return

    if lado == "izq":
        if nodo_seleccionado.izq: messagebox.showerror("Error", "Ya existe un hijo a la izquierda.")
        else: nodo_seleccionado.izq = Nodo(valor)
    else:
        if nodo_seleccionado.der: messagebox.showerror("Error", "Ya existe un hijo a la derecha.")
        else: nodo_seleccionado.der = Nodo(valor)
    
    dibujar()

def editar_nodo():
    if not nodo_seleccionado:
        messagebox.showwarning("Atención", "Selecciona un nodo para editar.")
        return
        
    nuevo_val = simpledialog.askinteger("Editar", "Nuevo valor:", initialvalue=nodo_seleccionado.valor)
    if nuevo_val is not None:
        todos = obtener_valores(raiz)
        if nuevo_val != nodo_seleccionado.valor and nuevo_val in todos:
            messagebox.showerror("Error", "Ese valor ya existe.")
        else:
            nodo_seleccionado.valor = nuevo_val
            dibujar()

def borrar_nodo():
    global nodo_seleccionado
    if not nodo_seleccionado:
        messagebox.showwarning("Atención", "Selecciona un nodo para borrar.")
        return
        
    if messagebox.askyesno("Confirmar", f"¿Borrar nodo {nodo_seleccionado.valor} y toda su rama?"):
        eliminar_nodo_recursivo(None, raiz, nodo_seleccionado.valor)
        nodo_seleccionado = None
        status_label.config(text="Nodo eliminado", fg="red")
        dibujar()

# ------------------------
# VALIDACIONES ANALIZAR
# ------------------------
def contar(n): return 0 if n is None else 1 + contar(n.izq) + contar(n.der)
def altura(n): return 0 if n is None else 1 + max(altura(n.izq), altura(n.der))

def es_lleno(n):
    if n is None: return True
    if n.izq is None and n.der is None: return True
    if n.izq and n.der: return es_lleno(n.izq) and es_lleno(n.der)
    return False

def es_completo(n, i=0, total=None):
    if total is None: total = contar(n)
    if n is None: return True
    if i >= total: return False
    return es_completo(n.izq, 2*i+1, total) and es_completo(n.der, 2*i+2, total)

def es_bst(n, min_v=float("-inf"), max_v=float("inf")):
    if n is None: return True
    if not (min_v < n.valor < max_v): return False
    return es_bst(n.izq, min_v, n.valor) and es_bst(n.der, n.valor, max_v)

def analizar():
    if not raiz:
        resultado_label.config(text="Árbol vacío")
        return
    res = []
    if es_lleno(raiz): res.append("Lleno")
    if es_completo(raiz): res.append("Completo")
    if es_bst(raiz): res.append("BST")
    
    texto = ", ".join(res) if res else "Binario Genérico"
    resultado_label.config(text=f"Tipo(s): {texto}")

# ------------------------
# DIBUJO EN CANVAS
# ------------------------
def dibujar():
    canvas.delete("all")
    _dibujar_recursivo(raiz, 400, 50, 200)

def _dibujar_recursivo(nodo, x, y, dx):
    if nodo is None: return
    
    # Guardamos posición actual para el clic
    nodo.x, nodo.y = x, y
    
    # Si es el seleccionado, lo pintamos de amarillo
    color = "yellow" if nodo == nodo_seleccionado else "#AEEEEE"
    
    if nodo.izq:
        canvas.create_line(x, y, x-dx, y+60, width=2, fill="#555")
        _dibujar_recursivo(nodo.izq, x-dx, y+60, dx//2)
    if nodo.der:
        canvas.create_line(x, y, x+dx, y+60, width=2, fill="#555")
        _dibujar_recursivo(nodo.der, x+dx, y+60, dx//2)

    canvas.create_oval(x-18, y-18, x+18, y+18, fill=color, outline="black", width=2)
    canvas.create_text(x, y, text=str(nodo.valor), font=("Arial", 10, "bold"))

# ------------------------
# INTERFAZ PRINCIPAL
# ------------------------
root = tk.Tk()
root.title("Visualizador de Árboles Mejorado")

frame_btns = tk.Frame(root, pady=10)
frame_btns.pack()

# Botones con colores para identificar acciones
tk.Button(frame_btns, text="Hijo Izq", bg="#E1F5FE", command=lambda: insertar("izq")).grid(row=0, column=0, padx=5)
tk.Button(frame_btns, text="Hijo Der", bg="#E1F5FE", command=lambda: insertar("der")).grid(row=0, column=1, padx=5)
tk.Button(frame_btns, text="Editar Valor", bg="#FFF9C4", command=editar_nodo).grid(row=0, column=2, padx=5)
tk.Button(frame_btns, text="Eliminar Nodo", bg="#FFCDD2", command=borrar_nodo).grid(row=0, column=3, padx=5)
tk.Button(frame_btns, text="Analizar Tipo", bg="#C8E6C9", command=analizar).grid(row=0, column=4, padx=5)

status_label = tk.Label(root, text="Para empezar, inserta la raíz", font=("Arial", 9, "italic"))
status_label.pack()

resultado_label = tk.Label(root, text="Tipo(s): ", font=("Arial", 11, "bold"))
resultado_label.pack(pady=5)

canvas = tk.Canvas(root, width=800, height=450, bg="white", highlightthickness=1)
canvas.pack(padx=20, pady=20)

# El evento de clic en el canvas
canvas.bind("<Button-1>", seleccionar_nodo)

root.mainloop()