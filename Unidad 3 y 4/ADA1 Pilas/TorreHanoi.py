"""
Edwin Geovanni Un Uicab Grupo 3SA
"""
import os
import time

# ══════════════════════════════════════════════════════════════
#  COLORES ANSI
# ══════════════════════════════════════════════════════════════
R  = "\033[0m"
B  = "\033[1m"
CY = "\033[96m"
GR = "\033[92m"
YL = "\033[93m"
RD = "\033[91m"
MG = "\033[95m"
DM = "\033[90m"
WH = "\033[97m"

DISCO_COLOR = {1: GR, 2: YL, 3: RD}


# ══════════════════════════════════════════════════════════════
#  CLASE PILA
# ══════════════════════════════════════════════════════════════
class Pila:
    def __init__(self, nombre):
        self.nombre = nombre
        self._datos = []

    def apilar(self, valor):
        self._datos.append(valor)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        return self._datos.pop()

    def tope(self):
        if self.esta_vacia():
            return None
        return self._datos[-1]

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamanio(self):
        return len(self._datos)

    def como_lista(self):
        return list(self._datos)


# ══════════════════════════════════════════════════════════════
#  LÓGICA TORRES DE HANOI
# ══════════════════════════════════════════════════════════════
def hanoi_movimientos(n, origen, destino, auxiliar):
    if n == 0:
        return []
    movs = []
    movs += hanoi_movimientos(n - 1, origen, auxiliar, destino)
    movs.append((origen, destino))
    movs += hanoi_movimientos(n - 1, auxiliar, destino, origen)
    return movs


# ══════════════════════════════════════════════════════════════
#  RENDERIZADO EN TERMINAL
# ══════════════════════════════════════════════════════════════
N_DISCOS = 3
ALTO     = N_DISCOS + 1
COL_W    = 15

def _render_disco(d):
    if d == 0:
        return f"{DM}│{R}", 1
    ancho = 1 + d * 2
    bloque = "█" * ancho
    color = DISCO_COLOR.get(d, WH)
    raw = f"{color}{B}[{bloque}]{R}"
    visible = 2 + ancho
    return raw, visible

def _centrar(raw, visible, ancho):
    pad = ancho - visible
    izq = pad // 2
    der = pad - izq
    return " " * izq + raw + " " * der

def dibujar(pilas, movimiento=None):
    limpiar()
    print(f"\n{CY}{B}  ╔══════════════════════════════════════╗")
    print(f"  ║     TORRES DE HANÓI  ·  3 DISCOS     ║")
    print(f"  ╚══════════════════════════════════════╝{R}\n")

    cols = []
    for pila in pilas:
        discos = pila.como_lista()
        columna = []
        for nivel in range(ALTO - 1, -1, -1):
            columna.append(discos[nivel] if nivel < len(discos) else 0)
        cols.append(columna)

    for fila in range(ALTO):
        linea = "  "
        for col in cols:
            d = col[fila]
            raw, visible = _render_disco(d)
            linea += _centrar(raw, visible, COL_W) + "   "
        print(linea)

    print(f"  {DM}{'▬' * (COL_W * 3 + 9)}{R}")

    etiquetas = "  "
    for p in pilas:
        label = f"{CY}{B}Torre {p.nombre}{R}"
        etiquetas += _centrar(label, 7, COL_W) + "   "
    print(etiquetas)

    if movimiento:
        print(f"\n  {GR}▶  {movimiento}{R}")
    print()


# ══════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausa(msg="  Presiona Enter para continuar..."):
    input(f"\n{DM}{msg}{R}")

def idx_a_nombre(i):
    return ["A", "B", "C"][i]


# ══════════════════════════════════════════════════════════════
#  MODOS DE JUEGO
# ══════════════════════════════════════════════════════════════
def iniciar_pilas():
    pilas = [Pila("A"), Pila("B"), Pila("C")]
    for d in range(N_DISCOS, 0, -1):
        pilas[0].apilar(d)
    return pilas


def modo_automatico(paso_a_paso=False):
    pilas = iniciar_pilas()
    movs  = hanoi_movimientos(N_DISCOS, 0, 2, 1)
    total = len(movs)

    dibujar(pilas)
    if paso_a_paso:
        print(f"  {YL}Modo PASO A PASO — presiona Enter en cada movimiento{R}")
    else:
        print(f"  {CY}Modo AUTO — {total} movimientos en total{R}")
    pausa("  Presiona Enter para comenzar...")

    for num, (origen, destino) in enumerate(movs, 1):
        disco = pilas[origen].tope()
        pilas[origen].desapilar()
        pilas[destino].apilar(disco)

        msg = (f"Mov {num}/{total}  —  Disco {disco}: "
               f"Torre {idx_a_nombre(origen)} → Torre {idx_a_nombre(destino)}")
        dibujar(pilas, movimiento=msg)

        if paso_a_paso:
            pausa()
        else:
            time.sleep(0.7)

    print(f"  {GR}{B}🎉 ¡Resuelto en {total} movimientos (óptimo)!{R}\n")
    pausa("  Presiona Enter para volver al menú...")


def modo_manual():
    pilas    = iniciar_pilas()
    total    = 2**N_DISCOS - 1
    contador = 0

    while True:
        dibujar(pilas)

        # Victoria
        if pilas[2].tamanio() == N_DISCOS:
            extra = f"  {GR}¡En el mínimo posible! 🏆{R}" if contador == total else ""
            print(f"  {GR}{B} ¡Ganaste!{R}  Usaste {YL}{contador}{R} movimientos.{extra}\n")
            pausa("  Presiona Enter para volver al menú...")
            return

        print(f"  {WH}Movimientos: {YL}{contador}{WH}  |  Óptimo: {GR}{total}{R}")
        print(f"  {DM}Escribe origen y destino (ej: {WH}A C{DM})  o  {WH}salir{R}\n")

        entrada = input(f"  {CY}> {R}").strip().upper()

        if entrada == "SALIR":
            return

        partes = entrada.split()
        if len(partes) != 2 or partes[0] not in "ABC" or partes[1] not in "ABC":
            print(f"\n  {RD}Entrada inválida. Escribe dos letras: A, B o C.{R}")
            time.sleep(1.3)
            continue

        idx_o = "ABC".index(partes[0])
        idx_d = "ABC".index(partes[1])

        if idx_o == idx_d:
            print(f"\n  {RD}Origen y destino son la misma torre.{R}")
            time.sleep(1.2)
            continue

        if pilas[idx_o].esta_vacia():
            print(f"\n  {RD}La torre {partes[0]} está vacía.{R}")
            time.sleep(1.2)
            continue

        disco_o = pilas[idx_o].tope()
        disco_d = pilas[idx_d].tope()

        if disco_d is not None and disco_o > disco_d:
            print(f"\n  {RD}Inválido: disco {disco_o} no puede ir sobre disco {disco_d}.{R}")
            time.sleep(1.5)
            continue

        pilas[idx_o].desapilar()
        pilas[idx_d].apilar(disco_o)
        contador += 1


# ══════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════
def menu():
    while True:
        limpiar()
        print(f"\n{CY}{B}")
        print("  ╔══════════════════════════════════════╗")
        print("  ║       TORRES DE HANÓI — MENÚ         ║")
        print("  ╠══════════════════════════════════════╣")
        print(f"  ║  {GR}1.{CY} Jugar manualmente                  ║")
        print(f"  ║  {YL}2.{CY} Ver solución automática            ║")
        print(f"  ║  {MG}3.{CY} Solución paso a paso               ║")
        print(f"  ║  {RD}4.{CY} Salir                              ║")
        print("  ╚══════════════════════════════════════╝")
        print(R)

        op = input(f"  {CY}Elige una opción (1-4): {R}").strip()

        if op == "1":
            modo_manual()
        elif op == "2":
            modo_automatico(paso_a_paso=False)
        elif op == "3":
            modo_automatico(paso_a_paso=True)
        elif op == "4":
            limpiar()
            print(f"\n  {GR}¡Hasta luego!{R}\n")
            break
        else:
            print(f"  {RD}Opción inválida.{R}")
            time.sleep(0.8)


if __name__ == "__main__":
    menu()