"""
Evaluador de Expresiones Aritméticas en Notación Posfija y Prefija
Utiliza una estructura de Pila (Stack) implementada manualmente

Edwin Geovanni Un Uicab Grupo 3SA
"""


# ─────────────────────────────────────────────
#  Implementación de la Pila
# ─────────────────────────────────────────────

class Pila:
    """Pila (Stack) implementada con una lista de Python."""

    def __init__(self):
        self._datos = []

    def apilar(self, elemento):
        """Agrega un elemento al tope de la pila."""
        self._datos.append(elemento)

    def desapilar(self):
        """Elimina y retorna el elemento en el tope de la pila."""
        if self.esta_vacia():
            raise IndexError("No se puede desapilar: la pila está vacía.")
        return self._datos.pop()

    def tope(self):
        """Retorna el elemento en el tope sin eliminarlo."""
        if self.esta_vacia():
            raise IndexError("La pila está vacía.")
        return self._datos[-1]

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamanio(self):
        return len(self._datos)

    def __repr__(self):
        return f"Pila({self._datos})"


# ─────────────────────────────────────────────
#  Utilidades comunes
# ─────────────────────────────────────────────

OPERADORES = {'+', '-', '*', '/', '**', '%'}


def es_operador(token: str) -> bool:
    return token in OPERADORES


def aplicar_operacion(op: str, a: float, b: float) -> float:
    """Aplica la operación binaria op sobre los operandos a y b."""
    if op == '+':  return a + b
    if op == '-':  return a - b
    if op == '*':  return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("División por cero.")
        return a / b
    if op == '**': return a ** b
    if op == '%':
        if b == 0:
            raise ZeroDivisionError("Módulo por cero.")
        return a % b
    raise ValueError(f"Operador desconocido: {op}")


def tokenizar(expresion: str) -> list[str]:
    """Divide la expresión en tokens."""
    return expresion.strip().split()


def es_numero(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


# ─────────────────────────────────────────────
#  Evaluación POSFIJA  (ej: 3 4 + 2 *)
# ─────────────────────────────────────────────

def evaluar_posfija(expresion: str) -> float:
    """
    Evalúa una expresión en notación posfija (RPN).

    Algoritmo:
      - Recorre los tokens de izquierda a derecha.
      - Si es un número → apilarlo.
      - Si es un operador → desapilar dos operandos,
        aplicar la operación y apilar el resultado.
      - Al finalizar, el resultado es el único elemento en la pila.
    """
    pila = Pila()
    tokens = tokenizar(expresion)

    for token in tokens:
        if es_numero(token):
            pila.apilar(float(token))
        elif es_operador(token):
            if pila.tamanio() < 2:
                raise ValueError(
                    f"Expresión posfija inválida: operador '{token}' "
                    "sin suficientes operandos."
                )
            b = pila.desapilar()   # segundo operando
            a = pila.desapilar()   # primer operando
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
        else:
            raise ValueError(f"Token no reconocido: '{token}'")

    if pila.tamanio() != 1:
        raise ValueError(
            "Expresión posfija inválida: quedaron elementos en la pila "
            f"({pila.tamanio()} en lugar de 1)."
        )

    return pila.desapilar()


# ─────────────────────────────────────────────
#  Evaluación PREFIJA  (ej: * + 3 4 2)
# ─────────────────────────────────────────────

def evaluar_prefija(expresion: str) -> float:
    """
    Evalúa una expresión en notación prefija (polaca).

    Algoritmo:
      - Recorre los tokens de DERECHA a IZQUIERDA.
      - Si es un número → apilarlo.
      - Si es un operador → desapilar dos operandos,
        aplicar la operación y apilar el resultado.
      - Al finalizar, el resultado es el único elemento en la pila.
    """
    pila = Pila()
    tokens = tokenizar(expresion)

    for token in reversed(tokens):
        if es_numero(token):
            pila.apilar(float(token))
        elif es_operador(token):
            if pila.tamanio() < 2:
                raise ValueError(
                    f"Expresión prefija inválida: operador '{token}' "
                    "sin suficientes operandos."
                )
            a = pila.desapilar()   # primer operando
            b = pila.desapilar()   # segundo operando
            resultado = aplicar_operacion(token, a, b)
            pila.apilar(resultado)
        else:
            raise ValueError(f"Token no reconocido: '{token}'")

    if pila.tamanio() != 1:
        raise ValueError(
            "Expresión prefija inválida: quedaron elementos en la pila "
            f"({pila.tamanio()} en lugar de 1)."
        )

    return pila.desapilar()


# ─────────────────────────────────────────────
#  Interfaz de línea de comandos
# ─────────────────────────────────────────────

EJEMPLOS = {
    "posfija": [
        ("3 4 +",           "3 + 4 = 7"),
        ("5 1 2 + 4 * + 3 -", "5 + (1+2)*4 - 3 = 14"),
        ("2 3 ** 4 *",      "2³ × 4 = 32"),
        ("10 2 8 * + 3 -",  "10 + 2×8 - 3 = 23"),
        ("15 7 1 1 + - / 3 * 2 1 1 + + -", "((15/(7-(1+1)))*3)-((2+(1+1))) = 5"),
    ],
    "prefija": [
        ("+ 3 4",            "3 + 4 = 7"),
        ("+ 5 * - 1 2 4",    "5 + (1-2)*4 = 1"),   # 5 + (-1)*4 = 1
        ("* ** 2 3 4",       "2³ × 4 = 32"),
        ("- + 10 * 2 8 3",   "10 + 2×8 - 3 = 23"),
        ("- * / 15 - 7 + 1 1 3 + 2 + 1 1", "((15/(7-(1+1)))*3)-((2+(1+1))) = 5"),
    ],
}

COLORES = {
    "verde":    "\033[92m",
    "rojo":     "\033[91m",
    "amarillo": "\033[93m",
    "cyan":     "\033[96m",
    "azul":     "\033[94m",
    "blanco":   "\033[97m",
    "gris":     "\033[90m",
    "reset":    "\033[0m",
    "negrita":  "\033[1m",
}

def c(texto, color):
    return f"{COLORES[color]}{texto}{COLORES['reset']}"


def separador(ancho=62, car="─"):
    print(c(car * ancho, "gris"))


def mostrar_banner():
    print()
    separador(62, "═")
    print(c("  EVALUADOR DE EXPRESIONES ARITMÉTICAS CON PILA", "cyan") + "  ")
    print(c("  Notación Posfija (RPN) y Prefija (Polaca)", "azul"))
    separador(62, "═")
    print()


def mostrar_ayuda():
    print(c("\n  OPERADORES SOPORTADOS:", "amarillo"))
    ops = [
        ("+",  "Suma"),
        ("-",  "Resta"),
        ("*",  "Multiplicación"),
        ("/",  "División"),
        ("**", "Potencia"),
        ("%",  "Módulo"),
    ]
    for op, nombre in ops:
        print(f"    {c(op.center(4), 'blanco')}  {nombre}")

    print(c("\n  EJEMPLOS POSFIJA:", "amarillo"))
    for expr, desc in EJEMPLOS["posfija"][:3]:
        print(f"    {c(expr, 'verde')}  →  {c(desc, 'gris')}")

    print(c("\n  EJEMPLOS PREFIJA:", "amarillo"))
    for expr, desc in EJEMPLOS["prefija"][:3]:
        print(f"    {c(expr, 'cyan')}  →  {c(desc, 'gris')}")

    print(c("\n  NOTAS:", "amarillo"))
    print("    • Separe cada token (número u operador) con UN espacio.")
    print("    • Los números decimales usan punto: 3.14")
    print("    • Comandos: 'ejemplos', 'ayuda', 'salir'\n")


def ejecutar_ejemplos():
    print(c("\n  ── Ejemplos predefinidos ──", "negrita"))
    for notacion in ("posfija", "prefija"):
        fn = evaluar_posfija if notacion == "posfija" else evaluar_prefija
        color = "verde" if notacion == "posfija" else "cyan"
        print(c(f"\n  {notacion.upper()}", color))
        for expr, desc in EJEMPLOS[notacion]:
            try:
                res = fn(expr)
                res_str = f"{res:.6g}"
                print(f"    {c(expr, color)}")
                print(f"    = {c(res_str, 'blanco')}   {c('# ' + desc, 'gris')}")
                print()
            except Exception as e:
                print(f"    {c('ERROR: ' + str(e), 'rojo')}\n")


def pedir_notacion() -> str:
    while True:
        print(c("\n  Seleccione notación:", "amarillo"))
        print(f"    {c('[1]', 'blanco')} Posfija  (ej: 3 4 + 2 *)")
        print(f"    {c('[2]', 'blanco')} Prefija  (ej: * + 3 4 2)")
        opcion = input(c("  → ", "gris")).strip()
        if opcion in ("1", "posfija", "pos", "postfija"):
            return "posfija"
        if opcion in ("2", "prefija", "pre"):
            return "prefija"
        print(c("  Opción inválida. Ingrese 1 o 2.", "rojo"))


def main():
    mostrar_banner()
    mostrar_ayuda()

    while True:
        separador()
        print(c("  Comandos: ayuda | ejemplos | salir  —  o elija notación:", "gris"))
        print(c("    [1] Posfija   [2] Prefija", "amarillo"))
        entrada = input(c("  → ", "gris")).strip().lower()

        if not entrada:
            continue
        if entrada == "salir":
            print(c("\n  ¡Hasta luego!\n", "cyan"))
            break
        if entrada == "ayuda":
            mostrar_ayuda()
            continue
        if entrada == "ejemplos":
            ejecutar_ejemplos()
            continue

        if entrada in ("1", "posfija", "pos", "postfija"):
            notacion = "posfija"
        elif entrada in ("2", "prefija", "pre"):
            notacion = "prefija"
        else:
            print(c("  Opción no reconocida. Ingrese 1, 2, ayuda, ejemplos o salir.", "rojo"))
            continue

        fn = evaluar_posfija if notacion == "posfija" else evaluar_prefija
        color = "verde" if notacion == "posfija" else "cyan"

        print(c(f"\n  Ingrese expresión en notación {notacion}:", "amarillo"))
        expresion = input(c("  → ", "gris")).strip()

        if not expresion:
            print(c("  Expresión vacía.", "rojo"))
            continue

        try:
            resultado = fn(expresion)
            resultado_str = f"{resultado:.10g}"
            print(c(f"\n  Resultado: {resultado_str}", "blanco"))
        except ZeroDivisionError as e:
            print(c(f"\n  Error matemático: {e}", "rojo"))
        except ValueError as e:
            print(c(f"\n  Error de sintaxis: {e}", "rojo"))
        except Exception as e:
            print(c(f"\n  Error inesperado: {e}", "rojo"))


if __name__ == "__main__":
    main()