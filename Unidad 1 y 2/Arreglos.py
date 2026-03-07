import time
import numpy as np

# Parámetros
NUM_ALUMNOS = 500
NUM_MATERIAS = 6
OBJETIVO_ALUMNO = 321
OBJETIVO_MATERIA = 5

# Índices para búsqueda (n-1 porque empezamos en 0)
IDX_A = OBJETIVO_ALUMNO - 1
IDX_M = OBJETIVO_MATERIA - 1

# Datos
data_f1 = np.random.randint(0, 101, size=(NUM_MATERIAS, NUM_ALUMNOS))
data_f2 = np.random.randint(0, 101, size=(NUM_ALUMNOS, NUM_MATERIAS))

# --- Búsqueda Exhaustiva Forma 1 ---
start_b1 = time.perf_counter_ns()
valor_f1 = None
encontrado_f1 = False
for m in range(NUM_MATERIAS):
    for a in range(NUM_ALUMNOS):
        if m == IDX_M and a == IDX_A:
            valor_f1 = data_f1[m, a]
            encontrado_f1 = True
            break
    if encontrado_f1: break
end_b1 = time.perf_counter_ns()
tiempo_b1 = end_b1 - start_b1

# --- Búsqueda Exhaustiva Forma 2 ---
start_b2 = time.perf_counter_ns()
valor_f2 = None
encontrado_f2 = False
for a in range(NUM_ALUMNOS):
    for m in range(NUM_MATERIAS):
        if a == IDX_A and m == IDX_M:
            valor_f2 = data_f2[a, m]
            encontrado_f2 = True
            break
    if encontrado_f2: break
end_b2 = time.perf_counter_ns()
tiempo_b2 = end_b2 - start_b2

# --- Funciones de Impresión ---
def imprimir_forma_1():
    print(f"\n--- FORMA 1 (MATERIAS x ALUMNOS) ---")
    header = f"{'':12} |" + "|".join([f" A{i+1:03} " for i in range(NUM_ALUMNOS)]) + "|"
    print(header)
    for i in range(NUM_MATERIAS):
        fila = f" Materia {i+1} |" + "|".join([f"  {data_f1[i, j]:3}  " for j in range(NUM_ALUMNOS)]) + "|"
        print(fila)

def imprimir_forma_2():
    print(f"\n--- FORMA 2 (ALUMNOS x MATERIAS) ---")
    header = f"{'':12} |" + "|".join([f" Mat {i+1} " for i in range(NUM_MATERIAS)]) + "|"
    print(header)
    for i in range(NUM_ALUMNOS):
        fila = f" Alumno {i+1:3}  |" + "|".join([f"   {data_f2[i, j]:3}   " for j in range(NUM_MATERIAS)]) + "|"
        print(fila)

# Ejecutar impresiones de 500 registros
imprimir_forma_1()
imprimir_forma_2()

# Resultados finales
print("\n" + " RESULTADOS DE LA BÚSQUEDA ".center(60, "="))
print(f"Buscando: Alumno {OBJETIVO_ALUMNO}, Materia {OBJETIVO_MATERIA}")
print("-" * 60)
print(f"FORMA 1 (6x500):")
print(f"  - Valor encontrado: {valor_f1}")
print(f"  - Tiempo de búsqueda: {tiempo_b1} ns ({tiempo_b1 / 1_000_000:.6f} ms)")
print("-" * 60)
print(f"FORMA 2 (500x6):")
print(f"  - Valor encontrado: {valor_f2}")
print(f"  - Tiempo de búsqueda: {tiempo_b2} ns ({tiempo_b2 / 1_000_000:.6f} ms)")
print("=" * 60)
