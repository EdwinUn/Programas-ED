"""
============================================================
  FIBONACCI: Solución Iterativa vs Recursiva en Python
  Comparación de tiempos de ejecución
============================================================
"""

import time
import sys

# Aumentar el límite de recursión para pruebas más grandes
sys.setrecursionlimit(10000)


# ──────────────────────────────────────────────
#  1. SOLUCIÓN RECURSIVA (sin memoización)
# ──────────────────────────────────────────────
def fibonacci_recursivo(n):
    """
    Calcula el n-ésimo número de Fibonacci de forma recursiva.
    
    Ventajas:
      - Código corto, limpio y fácil de entender.
      - Refleja directamente la definición matemática.
    
    Desventajas:
      - Muy lento para n grandes (complejidad O(2^n)).
      - Puede causar desbordamiento de pila (stack overflow).
      - Recalcula los mismos valores muchas veces.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


# ──────────────────────────────────────────────
#  2. SOLUCIÓN RECURSIVA CON MEMOIZACIÓN
# ──────────────────────────────────────────────
memo = {}

def fibonacci_recursivo_memo(n):
    """
    Versión recursiva optimizada con memoización (caché).
    
    Ventajas:
      - Mantiene la claridad del código recursivo.
      - Mucho más rápida: O(n) en tiempo.
      - Evita recalcular subproblemas ya resueltos.
    
    Desventajas:
      - Usa memoria adicional para el diccionario.
      - Aún limitada por el límite de recursión de Python.
    """
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        memo[n] = fibonacci_recursivo_memo(n - 1) + fibonacci_recursivo_memo(n - 2)
        return memo[n]


# ──────────────────────────────────────────────
#  3. SOLUCIÓN ITERATIVA
# ──────────────────────────────────────────────
def fibonacci_iterativo(n):
    """
    Calcula el n-ésimo número de Fibonacci de forma iterativa.
    
    Ventajas:
      - Muy eficiente: O(n) en tiempo y O(1) en espacio.
      - Sin límite de recursión.
      - Funciona correctamente para n muy grandes.
    
    Desventajas:
      - Menos "elegante" matemáticamente que la versión recursiva.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ──────────────────────────────────────────────
#  4. FUNCIÓN PARA MEDIR TIEMPO
# ──────────────────────────────────────────────
def medir_tiempo(funcion, n, nombre):
    """Ejecuta la función y mide el tiempo en milisegundos."""
    inicio = time.perf_counter()
    resultado = funcion(n)
    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    print(f"  {nombre:<35} -> F({n}) = {resultado}")
    print(f"  {'Tiempo de ejecución:':<35}    {tiempo_ms:.6f} ms\n")
    return resultado, tiempo_ms


# ──────────────────────────────────────────────
#  5. MENÚ INTERACTIVO
# ──────────────────────────────────────────────
def mostrar_ventajas():
    print("\n" + "="*60)
    print("  COMPARACIÓN DE VENTAJAS Y DESVENTAJAS")
    print("="*60)
    print("""
RECURSIVA (sin memoización)
    Código limpio y legible
    Refleja la definición matemática
    Lentísima para n > 35 (O(2^n))
    Puede causar stack overflow

RECURSIVA CON MEMOIZACIÓN
    Código recursivo legible
    Rápida gracias al caché (O(n))
    Evita cálculos repetidos
    Usa memoria extra
    Aún limitada por recursión de Python

ITERATIVA
    La más rápida y eficiente
    Sin límite de pila
    Usa O(1) en memoria
    Menos intuitiva matemáticamente
""")


def menu():
    print("\n" + "="*60)
    print("        FIBONACCI: ITERATIVO vs RECURSIVO")
    print("="*60)
    
    while True:
        print("\n  Opciones:")
        print("  [1] Calcular Fibonacci para un número")
        print("  [2] Comparar tiempos de ejecución")
        print("  [3] Ver ventajas y desventajas")
        print("  [4] Mostrar secuencia de Fibonacci")
        print("  [0] Salir")
        
        opcion = input("\n  Elige una opción: ").strip()
        
        if opcion == "1":
            try:
                n = int(input("  Ingresa n (0-40 para recursiva sin memo): "))
                if n < 0:
                    print("  Por favor ingresa un número >= 0")
                    continue
                print()
                if n <= 40:
                    medir_tiempo(fibonacci_recursivo, n, "Recursiva (sin memo)")
                else:
                    print("   n > 40: omitiendo recursiva sin memo (muy lenta)\n")
                memo.clear()
                medir_tiempo(fibonacci_recursivo_memo, n, "Recursiva (con memo)")
                medir_tiempo(fibonacci_iterativo, n, "Iterativa")
            except ValueError:
                print("   Ingresa un número entero válido.")

        elif opcion == "2":
            print("\n  Comparando tiempos para distintos valores de n...\n")
            valores = [10, 20, 30, 35]
            for n in valores:
                print(f"  ── n = {n} ──────────────────────────────")
                memo.clear()
                _, t1 = medir_tiempo(fibonacci_recursivo, n, "Recursiva (sin memo)")
                memo.clear()
                _, t2 = medir_tiempo(fibonacci_recursivo_memo, n, "Recursiva (con memo)")
                _, t3 = medir_tiempo(fibonacci_iterativo, n, "Iterativa")
                if t3 > 0:
                    print(f"  La recursiva sin memo es {t1/t3:.1f}x más lenta que la iterativa\n")

        elif opcion == "3":
            mostrar_ventajas()

        elif opcion == "4":
            try:
                n = int(input("  ¿Cuántos términos quieres ver? "))
                if n <= 0:
                    print(" Ingresa un número > 0")
                    continue
                secuencia = [fibonacci_iterativo(i) for i in range(n)]
                print(f"\n  Primeros {n} números de Fibonacci:")
                print(" ", secuencia)
            except ValueError:
                print(" Ingresa un número entero válido.")

        elif opcion == "0":
            print("\n  Cerrando programa\n")
            break
        else:
            print(" Opción no válida.")


# ──────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ──────────────────────────────────────────────
if __name__ == "__main__":
    menu()