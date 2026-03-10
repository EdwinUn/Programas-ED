import os

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
BL = "\033[94m"
DM = "\033[90m"
WH = "\033[97m"


# ══════════════════════════════════════════════════════════════
#  CLASE COLA
# ══════════════════════════════════════════════════════════════
class Cola:
    def __init__(self, nombre):
        self.nombre = nombre
        self._datos = []
        self._contador = 0   # número correlativo de atención

    def encolar(self):
        """Agrega un cliente y retorna su número de atención."""
        self._contador += 1
        self._datos.append(self._contador)
        return self._contador

    def desencolar(self):
        """Atiende al primer cliente de la cola."""
        if self.esta_vacia():
            raise IndexError("Cola vacía.")
        return self._datos.pop(0)

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamanio(self):
        return len(self._datos)

    def como_lista(self):
        return list(self._datos)


# ══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE SERVICIOS
# ══════════════════════════════════════════════════════════════
SERVICIOS = {
    1: {"nombre": "General",      "color": CY, "icono": "●"},
    2: {"nombre": "Preferencial", "color": GR, "icono": "★"},
    3: {"nombre": "Empresas",     "color": MG, "icono": "◆"},
}

# Crear una cola por servicio
colas = {k: Cola(v["nombre"]) for k, v in SERVICIOS.items()}


# ══════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def separador(color=DM, char="─", largo=52):
    print(f"  {color}{char * largo}{R}")

def mostrar_estado():
    """Muestra el estado actual de todas las colas."""
    print(f"\n  {WH}{B}Estado actual de las colas:{R}")
    separador()
    for k, info in SERVICIOS.items():
        cola  = colas[k]
        color = info["color"]
        icono = info["icono"]
        nombre = info["nombre"]
        espera = cola.como_lista()

        if cola.esta_vacia():
            detalle = f"{DM}(vacía){R}"
        else:
            nums = "  ".join(f"{color}{B}#{n}{R}" for n in espera)
            detalle = f"{nums}  {DM}({cola.tamanio()} en espera){R}"

        print(f"  {color}{icono} [{k}] {B}{nombre:<14}{R}  {detalle}")
    separador()


# ══════════════════════════════════════════════════════════════
#  ACCIONES
# ══════════════════════════════════════════════════════════════
def cliente_llega(num_servicio):
    """C<num> — Un cliente llega y se le asigna número."""
    if num_servicio not in SERVICIOS:
        print(f"\n  {RD}✗ Servicio {num_servicio} no existe. Usa 1, 2 o 3.{R}")
        return

    info   = SERVICIOS[num_servicio]
    cola   = colas[num_servicio]
    numero = cola.encolar()
    color  = info["color"]
    nombre = info["nombre"]

    print(f"\n  {GR}{B}✔ Nuevo cliente en cola{R}")
    print(f"  {color}  Servicio : {B}{nombre}{R}")
    print(f"  {color}  N° asignado : {B}#{numero}{R}")
    print(f"  {DM}  Clientes esperando: {cola.tamanio()}{R}")


def atender_cliente(num_servicio):
    """A<num> — El personal atiende al siguiente cliente."""
    if num_servicio not in SERVICIOS:
        print(f"\n  {RD}✗ Servicio {num_servicio} no existe. Usa 1, 2 o 3.{R}")
        return

    info  = SERVICIOS[num_servicio]
    cola  = colas[num_servicio]
    color = info["color"]
    nombre = info["nombre"]

    if cola.esta_vacia():
        print(f"\n  {YL}⚠ La cola de {B}{nombre}{R}{YL} está vacía.{R}")
        print(f"  {DM}  No hay clientes esperando en este servicio.{R}")
        return

    numero = cola.desencolar()
    print(f"\n  {BL}{B}📢 ¡Llamando al cliente!{R}")
    print(f"  {color}  Servicio : {B}{nombre}{R}")
    print(f"  {color}  N° llamado : {B}#{numero}{R}")
    print(f"  {DM}  Clientes restantes: {cola.tamanio()}{R}")


# ══════════════════════════════════════════════════════════════
#  CABECERA
# ══════════════════════════════════════════════════════════════
def cabecera():
    limpiar()
    print(f"\n{CY}{B}")
    print("  ╔════════════════════════════════════════════════════╗")
    print("  ║      SISTEMA DE COLAS — COMPAÑÍA DE SEGUROS       ║")
    print("  ╠════════════════════════════════════════════════════╣")
    print(f"  ║  {GR}C<n>{CY}  →  Llega cliente al servicio n             ║")
    print(f"  ║  {BL}A<n>{CY}  →  Atender siguiente de la cola n          ║")
    print(f"  ║  {YL}E{CY}    →  Ver estado de las colas                  ║")
    print(f"  ║  {RD}S{CY}    →  Salir                                    ║")
    print("  ╠════════════════════════════════════════════════════╣")
    print(f"  ║  Servicios:  {CY}1{R}{CY}=General  {GR}2{R}{GR}=Preferencial  {MG}3{R}{MG}=Empresas{CY}  ║")
    print(f"  ╚════════════════════════════════════════════════════╝{R}")


# ══════════════════════════════════════════════════════════════
#  BUCLE PRINCIPAL
# ══════════════════════════════════════════════════════════════
def main():
    cabecera()
    mostrar_estado()

    while True:
        print()
        entrada = input(f"  {CY}{B}> {R}").strip().upper()

        if not entrada:
            continue

        # Salir
        if entrada == "S":
            limpiar()
            print(f"\n  {GR}¡Hasta luego!{R}\n")
            break

        # Ver estado
        elif entrada == "E":
            mostrar_estado()

        # Cliente llega: C1, C2, C3
        elif entrada.startswith("C") and len(entrada) == 2 and entrada[1].isdigit():
            cliente_llega(int(entrada[1]))
            mostrar_estado()

        # Atender cliente: A1, A2, A3
        elif entrada.startswith("A") and len(entrada) == 2 and entrada[1].isdigit():
            atender_cliente(int(entrada[1]))
            mostrar_estado()

        else:
            print(f"\n  {RD}✗ Comando no reconocido.{R}")
            print(f"  {DM}  Usa C1..C3, A1..A3, E o S{R}")


if __name__ == "__main__":
    main()