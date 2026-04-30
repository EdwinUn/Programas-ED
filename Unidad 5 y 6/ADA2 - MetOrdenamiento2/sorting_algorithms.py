"""
Algoritmos de ordenamiento implementados como generadores.
Cada yield produce: (array_actual, indices_comparando, descripcion)
"""


def shell_sort_generator(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                yield arr[:], [j, j - gap], f"Comparando [{j}] y [{j-gap}]"
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
            yield arr[:], [j], f"Insertando en [{j}]"
        gap //= 2

    yield arr[:], [], "Completado"


def quicksort_generator(arr):
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            yield arr[:], [j, high], f"Comparando [{j}] con pivote [{high}]={pivot}"
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr[:], [i, j], f"Intercambiando [{i}] y [{j}]"
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield arr[:], [i + 1, high], f"Pivote en posición [{i+1}]"
        return i + 1

    def quicksort(arr, low, high):
        if low < high:
            stack = [(low, high)]
            while stack:
                lo, hi = stack.pop()
                if lo < hi:
                    gen = partition(arr, lo, hi)
                    pi = None
                    for state in gen:
                        yield state
                    pi = lo
                    # recalcular pivot real
                    for k in range(lo, hi + 1):
                        pass
                    # buscar la partición correctamente
                    pivot_val = arr[hi]
                    pi = lo
                    temp_arr = arr[lo:hi+1][:]
                    for k in range(lo, hi + 1):
                        if arr[k] <= pivot_val and k != hi:
                            pi = k
                    # simplificamos: llamada recursiva iterativa
                    stack.append((lo, hi - 1))
                    stack.append((hi + 1, hi))

    # Implementación limpia iterativa con stack
    def _quicksort_iter(arr):
        stack = [(0, len(arr) - 1)]
        while stack:
            low, high = stack.pop()
            if low >= high:
                continue
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                yield arr[:], [j, high], f"Comparando con pivote={pivot}"
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        yield arr[:], [i, j], f"Intercambiando [{i}] y [{j}]"
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pi = i + 1
            yield arr[:], [pi], f"Pivote colocado en [{pi}]"
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))

    yield from _quicksort_iter(arr)
    yield arr[:], [], "Completado"


def heapsort_generator(arr):
    n = len(arr)

    def heapify(arr, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            yield arr[:], [i, left], f"Comparando padre [{i}] con hijo izq [{left}]"
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            yield arr[:], [largest, right], f"Comparando [{largest}] con hijo der [{right}]"
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr[:], [i, largest], f"Intercambiando [{i}] y [{largest}]"
            yield from heapify(arr, n, largest)

    # Construir max-heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    # Extraer elementos del heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr[:], [0, i], f"Extrayendo máximo a posición [{i}]"
        yield from heapify(arr, i, 0)

    yield arr[:], [], "Completado"


def radix_sort_generator(arr):
    # Solo funciona con enteros no negativos
    arr = [int(x) for x in arr]

    def counting_sort_by_digit(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
            yield arr[:], [i], f"Contando dígito {index} de arr[{i}]={arr[i]}"

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            yield arr[:], [i], f"Colocando arr[{i}]={arr[i]} en posición correcta"

        for i in range(n):
            arr[i] = output[i]
            yield arr[:], [i], f"Actualizando posición [{i}]={arr[i]}"

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        yield from counting_sort_by_digit(arr, exp)
        exp *= 10
        if exp > max_val * 10:
            break

    yield arr[:], [], "Completado"