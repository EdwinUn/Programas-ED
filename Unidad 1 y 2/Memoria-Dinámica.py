# Memoria dinámica en Python

frutas = []  # lista vacía (no tiene tamaño fijo)

frutas.append("Mango")
frutas.append("Manzana")
frutas.append("Banana")
frutas.append("Uvas")

print(frutas)

frutas.pop(0)   # elimina "Mango"
frutas.pop(1)   # elimina el elemento que ahora está en índice 1
frutas.append("sandia")

print(frutas)
