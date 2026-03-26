import tkinter as tk
import random

# ------------------------
# NODO BINARIO
# ------------------------
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

# ------------------------
# GENERADORES
# ------------------------

def arbol_completo():
    r = Nodo(1)
    r.izq = Nodo(2)
    r.der = Nodo(3)
    r.izq.izq = Nodo(4)
    r.izq.der = Nodo(5)
    r.der.izq = Nodo(6)
    return r

def arbol_lleno():
    r = Nodo(1)
    r.izq = Nodo(2)
    r.der = Nodo(3)
    r.izq.izq = Nodo(4)
    r.izq.der = Nodo(5)
    r.der.izq = Nodo(6)
    r.der.der = Nodo(7)
    return r

def arbol_degenerado():
    r = Nodo(1)
    actual = r
    for i in range(2, 7):
        actual.der = Nodo(i)
        actual = actual.der
    return r

def insertar_bst(raiz, v):
    if raiz is None:
        return Nodo(v)
    if v < raiz.valor:
        raiz.izq = insertar_bst(raiz.izq, v)
    else:
        raiz.der = insertar_bst(raiz.der, v)
    return raiz

def arbol_bst():
    valores = [8, 3, 10, 1, 6, 14]
    r = None
    for v in valores:
        r = insertar_bst(r, v)
    return r

def arbol_equilibrado():
    # manual equilibrado
    r = Nodo(4)
    r.izq = Nodo(2)
    r.der = Nodo(6)
    r.izq.izq = Nodo(1)
    r.izq.der = Nodo(3)
    r.der.izq = Nodo(5)
    r.der.der = Nodo(7)
    return r

# ------------------------
# DIBUJO
# ------------------------

def dibujar(canvas, nodo, x, y, dx):
    if nodo is None:
        return

    canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
    canvas.create_text(x, y, text=str(nodo.valor))

    if nodo.izq:
        canvas.create_line(x, y, x-dx, y+50)
        dibujar(canvas, nodo.izq, x-dx, y+50, dx//2)

    if nodo.der:
        canvas.create_line(x, y, x+dx, y+50)
        dibujar(canvas, nodo.der, x+dx, y+50, dx//2)

# ------------------------
# CASOS ESPECIALES
# ------------------------

def arboles_similares():
    # misma forma, distintos valores
    a = arbol_completo()
    b = arbol_completo()
    b.valor = 9
    b.izq.valor = 8
    return a, b

def arboles_distintos():
    return arbol_completo(), arbol_degenerado()

def arboles_equivalentes():
    # misma forma y valores
    return arbol_completo(), arbol_completo()

# ------------------------
# MULTICAMINO (visual fake simple)
# ------------------------

def dibujar_b(canvas):
    canvas.create_text(400, 50, text="[10 | 20 | 30]", font=("Arial", 12))
    canvas.create_line(400, 70, 200, 150)
    canvas.create_line(400, 70, 400, 150)
    canvas.create_line(400, 70, 600, 150)

    canvas.create_text(200, 150, text="[5 | 8]")
    canvas.create_text(400, 150, text="[15 | 18]")
    canvas.create_text(600, 150, text="[35 | 40]")

# ------------------------
# CONTROL
# ------------------------

def generar():
    canvas.delete("all")
    tipo = opcion.get()

    if tipo == "Completo":
        dibujar(canvas, arbol_completo(), 400, 50, 200)

    elif tipo == "Lleno":
        dibujar(canvas, arbol_lleno(), 400, 50, 200)

    elif tipo == "Degenerado":
        dibujar(canvas, arbol_degenerado(), 400, 50, 200)

    elif tipo == "BST":
        dibujar(canvas, arbol_bst(), 400, 50, 200)

    elif tipo == "Equilibrado":
        dibujar(canvas, arbol_equilibrado(), 400, 50, 200)

    elif tipo == "Similares":
        a, b = arboles_similares()
        dibujar(canvas, a, 200, 50, 100)
        dibujar(canvas, b, 600, 50, 100)

    elif tipo == "Distintos":
        a, b = arboles_distintos()
        dibujar(canvas, a, 200, 50, 100)
        dibujar(canvas, b, 600, 50, 100)

    elif tipo == "Equivalentes":
        a, b = arboles_equivalentes()
        dibujar(canvas, a, 200, 50, 100)
        dibujar(canvas, b, 600, 50, 100)

    elif tipo == "Arbol B / B+ / 2-4":
        dibujar_b(canvas)

# ------------------------
# UI
# ------------------------

root = tk.Tk()
root.title("Visualizador completo de árboles")

opcion = tk.StringVar()
opcion.set("Completo")

menu = tk.OptionMenu(root, opcion,
    "Completo",
    "Lleno",
    "Degenerado",
    "BST",
    "Equilibrado",
    "Similares",
    "Distintos",
    "Equivalentes",
    "Arbol B / B+ / 2-4"
)
menu.pack()

tk.Button(root, text="Generar", command=generar).pack()

canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack()

root.mainloop()