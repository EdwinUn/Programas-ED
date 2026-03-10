# ── backend/cola_backend.py ──────────────────────────────────────
from collections import deque


class Cola:
    def __init__(self):
        self._datos = deque()

    def encolar(self, valor):
        self._datos.append(valor)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía.")
        return self._datos.popleft()

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamanio(self):
        return len(self._datos)

    def como_lista(self):
        return list(self._datos)

    def __str__(self):
        return " → ".join(str(x) for x in self._datos) or "(vacía)"


def sumar_colas(cola_a: Cola, cola_b: Cola) -> Cola:
    if cola_a.tamanio() != cola_b.tamanio():
        raise ValueError(
            f"Las colas deben tener el mismo tamaño "
            f"(Cola A: {cola_a.tamanio()}, Cola B: {cola_b.tamanio()})."
        )

    temp_a, temp_b, resultado = Cola(), Cola(), Cola()

    while not cola_a.esta_vacia():
        a = cola_a.desencolar()
        b = cola_b.desencolar()
        resultado.encolar(a + b)
        temp_a.encolar(a)
        temp_b.encolar(b)

    while not temp_a.esta_vacia():
        cola_a.encolar(temp_a.desencolar())
        cola_b.encolar(temp_b.desencolar())

    return resultado