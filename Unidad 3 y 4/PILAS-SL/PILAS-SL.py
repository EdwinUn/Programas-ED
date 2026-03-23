# ============================================================
#  SIMULACIÓN DE PILA (STACK) - Interfaz Gráfica con Tkinter
#  Pestaña 1: Problema original (con errores)
#  Pestaña 2: Versión corregida (sin errores)
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

CAPACIDAD_MAXIMA = 8

# ── Colores y fuentes ────────────────────────────────────────
BG_DARK     = "#0f1117"
BG_PANEL    = "#1a1d27"
BG_CARD     = "#22263a"
ACCENT_BLUE = "#4f8ef7"
ACCENT_RED  = "#f75f4f"
ACCENT_GRN  = "#4fdb8a"
ACCENT_YLW  = "#f7c94f"
ACCENT_PRP  = "#c084fc"
TEXT_WHITE  = "#eaeaea"
TEXT_GRAY   = "#7a7f99"
BORDER      = "#2e3250"

FONT_TITLE  = ("Courier New", 15, "bold")
FONT_MONO   = ("Courier New", 12, "bold")
FONT_SMALL  = ("Courier New", 10)
FONT_LOG    = ("Courier New", 10)

SLOT_H = 38
SLOT_W = 130
MARGIN_X = 15
CANVAS_H = 360

COLORES_ELEM = [ACCENT_BLUE, ACCENT_GRN, ACCENT_YLW,
                "#c084fc", "#fb923c", "#38bdf8", "#f472b6", "#a3e635"]

# ── Operaciones originales del problema ──────────────────────
OPS_ORIGINAL = [
    ("insertar", "X"),
    ("insertar", "Y"),
    ("eliminar", "Z"),
    ("eliminar", "T"),
    ("eliminar", "U"),
    ("insertar", "V"),
    ("insertar", "W"),
    ("eliminar", "p"),
    ("insertar", "R"),
]

# ── Operaciones corregidas ───────────────────────────────────
# Cada Eliminar(X) verifica si X está en el tope.
# Si no está → se inserta X primero y luego se elimina.
#
# Análisis paso a paso:
#   a. Insertar X        → pila: [X]
#   b. Insertar Y        → pila: [X, Y]
#   c. Eliminar Z        → Z no es el tope (tope=Y) → insertar Z → [X,Y,Z] → eliminar Z → [X,Y]
#   d. Eliminar T        → T no es el tope (tope=Y) → insertar T → [X,Y,T] → eliminar T → [X,Y]
#   e. Eliminar U        → U no es el tope (tope=Y) → insertar U → [X,Y,U] → eliminar U → [X,Y]
#   f. Insertar V        → pila: [X, Y, V]
#   g. Insertar W        → pila: [X, Y, V, W]
#   h. Eliminar p        → p no es el tope (tope=W) → insertar p → [X,Y,V,W,p] → eliminar p → [X,Y,V,W]
#   i. Insertar R        → pila: [X, Y, V, W, R]

OPS_CORREGIDA = [
    # (tipo, elemento, descripcion)
    ("insertar", "X", "Insertar('X')"),
    ("insertar", "Y", "Insertar('Y')"),
    ("fix_ins",  "Z", "🔧 'Z' no está en tope → Insertar('Z') primero"),
    ("fix_del",  "Z", "🔧 Ahora Eliminar('Z') del tope"),
    ("fix_ins",  "T", "🔧 'T' no está en tope → Insertar('T') primero"),
    ("fix_del",  "T", "🔧 Ahora Eliminar('T') del tope"),
    ("fix_ins",  "U", "🔧 'U' no está en tope → Insertar('U') primero"),
    ("fix_del",  "U", "🔧 Ahora Eliminar('U') del tope"),
    ("insertar", "V", "Insertar('V')"),
    ("insertar", "W", "Insertar('W')"),
    ("fix_ins",  "p", "🔧 'p' no está en tope → Insertar('p') primero"),
    ("fix_del",  "p", "🔧 Ahora Eliminar('p') del tope"),
    ("insertar", "R", "Insertar('R')"),
]


# ╔══════════════════════════════════════════════════════════╗
#  CLASE QUE CONSTRUYE UNA PESTAÑA COMPLETA
# ╚══════════════════════════════════════════════════════════╝

class PestañaPila:
    def __init__(self, notebook, titulo_tab, operaciones, modo_corregido=False):
        self.operaciones    = operaciones
        self.modo_corregido = modo_corregido
        self.pila           = []
        self.paso_actual    = 0

        self.frame = tk.Frame(notebook, bg=BG_DARK)
        notebook.add(self.frame, text=f"  {titulo_tab}  ")

        self._construir_ui()

    # ── Construcción de la UI ─────────────────────────────────
    def _construir_ui(self):
        f = self.frame
        main = tk.Frame(f, bg=BG_DARK)
        main.pack(padx=18, pady=10, fill="both")

        # Panel izquierdo — pila visual
        left = tk.Frame(main, bg=BG_PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.grid(row=0, column=0, padx=(0, 10), pady=4, sticky="nsew")

        tk.Label(left, text="PILA", font=FONT_MONO,
                 bg=BG_PANEL, fg=ACCENT_BLUE).pack(pady=(10, 4))

        self.canvas = tk.Canvas(left, width=160, height=CANVAS_H,
                                bg=BG_CARD, highlightthickness=0)
        self.canvas.pack(padx=14, pady=4)

        self.lbl_tope = tk.Label(left, text="TOPE = 0", font=FONT_MONO,
                                 bg=BG_PANEL, fg=ACCENT_YLW)
        self.lbl_tope.pack(pady=(6, 12))

        # Panel derecho — info + log
        right = tk.Frame(main, bg=BG_PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        right.grid(row=0, column=1, pady=4, sticky="nsew")

        tk.Label(right, text="OPERACIÓN ACTUAL", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(10, 2))

        self.lbl_operacion = tk.Label(right, text="—", font=FONT_MONO,
                                      bg=BG_CARD, fg=TEXT_WHITE,
                                      width=32, pady=8)
        self.lbl_operacion.pack(padx=14, pady=2)

        self.lbl_resultado = tk.Label(right, text="", font=FONT_SMALL,
                                      bg=BG_PANEL, fg=ACCENT_GRN,
                                      wraplength=310, justify="left")
        self.lbl_resultado.pack(padx=14, pady=4)

        tk.Label(right, text="SIGUIENTE OPERACIÓN", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(4, 2))

        self.lbl_siguiente = tk.Label(right, text="—", font=FONT_SMALL,
                                      bg=BG_CARD, fg=TEXT_GRAY,
                                      width=32, pady=6)
        self.lbl_siguiente.pack(padx=14, pady=2)

        tk.Label(right, text="HISTORIAL", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(8, 2))

        log_wrap = tk.Frame(right, bg=BG_CARD,
                            highlightbackground=BORDER, highlightthickness=1)
        log_wrap.pack(padx=14, pady=2, fill="both", expand=True)

        self.log_text = tk.Text(log_wrap, width=40, height=10,
                                bg=BG_CARD, fg=TEXT_WHITE,
                                font=FONT_LOG, bd=0, state="disabled")
        self.log_text.pack(padx=6, pady=6)

        self.lbl_progreso = tk.Label(right,
                                     text=f"Paso 0 / {len(self.operaciones)}",
                                     font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_GRAY)
        self.lbl_progreso.pack(pady=(4, 0))

        # Botones
        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(pady=12)

        def estilo(color):
            return dict(font=FONT_MONO, bg=color, fg=BG_DARK,
                        activebackground=color, activeforeground=BG_DARK,
                        relief="flat", padx=16, pady=8,
                        cursor="hand2", bd=0)

        self.btn_sig = tk.Button(btn_frame, text="▶  SIGUIENTE PASO",
                                 command=self.ejecutar_paso,
                                 **estilo(ACCENT_BLUE))
        self.btn_sig.grid(row=0, column=0, padx=8)

        tk.Button(btn_frame, text="⚡ AUTO COMPLETO",
                  command=self.auto_completo,
                  **estilo(ACCENT_YLW)).grid(row=0, column=1, padx=8)

        tk.Button(btn_frame, text="↺  REINICIAR",
                  command=self.reiniciar,
                  **estilo(ACCENT_RED)).grid(row=0, column=2, padx=8)

        self._dibujar_pila()
        self._actualizar_siguiente()

    # ── Lógica de la pila ─────────────────────────────────────
    def _insertar(self, elemento):
        if len(self.pila) >= CAPACIDAD_MAXIMA:
            return False, f"❌ DESBORDAMIENTO: pila llena, no se insertó '{elemento}'"
        self.pila.append(elemento)
        return True, f"✅ Insertar('{elemento}') → TOPE={len(self.pila)}"

    def _eliminar(self):
        if len(self.pila) == 0:
            return False, None, "❌ SUBDESBORDAMIENTO: pila vacía"
        elem = self.pila.pop()
        return True, elem, f"🗑  Eliminado '{elem}' → TOPE={len(self.pila)}"

    # ── Dibujar pila ──────────────────────────────────────────
    def _dibujar_pila(self):
        c = self.canvas
        c.delete("all")
        for i in range(CAPACIDAD_MAXIMA):
            y = CANVAS_H - (i + 1) * SLOT_H
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + SLOT_H - 2,
                                fill="#1c2033", outline=BORDER, width=1)
            c.create_text(MARGIN_X + SLOT_W + 16, y + SLOT_H // 2,
                          text=str(i), font=("Courier New", 8),
                          fill=TEXT_GRAY, anchor="w")
        for i, elem in enumerate(self.pila):
            y = CANVAS_H - (i + 1) * SLOT_H
            color = COLORES_ELEM[i % len(COLORES_ELEM)]
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + SLOT_H - 2,
                                fill=color, outline="white", width=1)
            c.create_text(MARGIN_X + SLOT_W // 2, y + SLOT_H // 2,
                          text=elem, font=FONT_MONO, fill=BG_DARK)
        if self.pila:
            y_arrow = CANVAS_H - len(self.pila) * SLOT_H + SLOT_H // 2
            c.create_text(MARGIN_X - 6, y_arrow,
                          text="◀", font=("Courier New", 14, "bold"),
                          fill=ACCENT_YLW, anchor="e")

    # ── Log ───────────────────────────────────────────────────
    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    # ── Label "siguiente" ─────────────────────────────────────
    def _actualizar_siguiente(self):
        if self.paso_actual >= len(self.operaciones):
            self.lbl_siguiente.config(text="— Fin de operaciones —", fg=TEXT_GRAY)
            return

        if not self.modo_corregido:
            tipo, val = self.operaciones[self.paso_actual]
            if tipo == "insertar":
                self.lbl_siguiente.config(text=f"Insertar('{val}')", fg=ACCENT_GRN)
            else:
                self.lbl_siguiente.config(text=f"Eliminar('{val}')", fg=ACCENT_RED)
        else:
            tipo, val, desc = self.operaciones[self.paso_actual]
            color = ACCENT_GRN if tipo == "insertar" else ACCENT_PRP
            self.lbl_siguiente.config(text=desc, fg=color)

    # ── Ejecutar un paso ──────────────────────────────────────
    def ejecutar_paso(self):
        total = len(self.operaciones)
        if self.paso_actual >= total:
            self._mostrar_resumen()
            return

        if not self.modo_corregido:
            # ── Pestaña 1: original ──────────────────────────
            tipo, val = self.operaciones[self.paso_actual]
            self.paso_actual += 1
            if tipo == "insertar":
                self.lbl_operacion.config(text=f"Insertar('{val}')", fg=ACCENT_BLUE)
                ok, msg = self._insertar(val)
                self.lbl_resultado.config(text=msg,
                                          fg=ACCENT_GRN if ok else ACCENT_RED)
            else:
                self.lbl_operacion.config(text=f"Eliminar('{val}')", fg=ACCENT_YLW)
                ok, _, msg = self._eliminar()
                self.lbl_resultado.config(text=msg,
                                          fg=ACCENT_YLW if ok else ACCENT_RED)
            self._log(f"[{self.paso_actual:02d}] {msg}")

        else:
            # ── Pestaña 2: corregida ─────────────────────────
            tipo, val, desc = self.operaciones[self.paso_actual]
            self.paso_actual += 1

            if tipo == "insertar":
                self.lbl_operacion.config(text=f"Insertar('{val}')", fg=ACCENT_BLUE)
                ok, msg = self._insertar(val)
                self.lbl_resultado.config(text=msg, fg=ACCENT_GRN if ok else ACCENT_RED)
                self._log(f"[{self.paso_actual:02d}] {msg}")

            elif tipo == "fix_ins":
                # El elemento pedido no está en el tope → insertarlo primero
                self.lbl_operacion.config(
                    text=f"🔧 Insertar('{val}') [corrección]", fg=ACCENT_PRP)
                ok, msg = self._insertar(val)
                detalle = (f"'{val}' no estaba en el tope.\n"
                           f"→ Se inserta '{val}' para poder eliminarlo.")
                self.lbl_resultado.config(text=detalle, fg=ACCENT_PRP)
                self._log(f"[{self.paso_actual:02d}] 🔧 CORRECCIÓN — {msg}")

            elif tipo == "fix_del":
                # Ahora el elemento está en el tope → eliminarlo
                self.lbl_operacion.config(
                    text=f"🔧 Eliminar('{val}') [corrección]", fg=ACCENT_PRP)
                ok, elem, msg = self._eliminar()
                self.lbl_resultado.config(text=msg, fg=ACCENT_PRP)
                self._log(f"[{self.paso_actual:02d}] 🔧 {msg}")

        self._dibujar_pila()
        self.lbl_tope.config(text=f"TOPE = {len(self.pila)}")
        self.lbl_progreso.config(text=f"Paso {self.paso_actual} / {total}")
        self._actualizar_siguiente()

        if self.paso_actual >= total:
            self.btn_sig.config(state="disabled", bg=TEXT_GRAY)
            self.frame.after(600, self._mostrar_resumen)

    # ── Auto completo ─────────────────────────────────────────
    def auto_completo(self):
        while self.paso_actual < len(self.operaciones):
            self.ejecutar_paso()
            self.frame.update()
            self.frame.after(300)

    # ── Reiniciar ─────────────────────────────────────────────
    def reiniciar(self):
        self.pila.clear()
        self.paso_actual = 0
        self._dibujar_pila()
        self.lbl_tope.config(text="TOPE = 0")
        self.lbl_operacion.config(text="—", fg=TEXT_WHITE)
        self.lbl_resultado.config(text="")
        self.lbl_progreso.config(text=f"Paso 0 / {len(self.operaciones)}")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.btn_sig.config(state="normal", bg=ACCENT_BLUE)
        self._actualizar_siguiente()

    # ── Resumen final ─────────────────────────────────────────
    def _mostrar_resumen(self):
        if not self.modo_corregido:
            texto = (
                f"✅ Operaciones completadas\n\n"
                f"📦 Elementos en la pila: {len(self.pila)}\n"
                f"📋 Contenido: {self.pila}\n"
                f"📍 TOPE final: {len(self.pila)}\n\n"
                f"⚠️  Error detectado:\n"
                f"   Paso 5 — Subdesbordamiento (Underflow)\n"
                f"   Pila vacía al intentar Eliminar('U')"
            )
            messagebox.showinfo("Resultado — Original", texto)
        else:
            texto = (
                f"✅ Versión corregida completada sin errores\n\n"
                f"📦 Elementos en la pila: {len(self.pila)}\n"
                f"📋 Contenido: {self.pila}\n"
                f"📍 TOPE final: {len(self.pila)}\n\n"
                f"🔧 Correcciones aplicadas (4 casos):\n"
                f"   c. Eliminar('Z') → Z no estaba → se insertó y eliminó\n"
                f"   d. Eliminar('T') → T no estaba → se insertó y eliminó\n"
                f"   e. Eliminar('U') → U no estaba → se insertó y eliminó\n"
                f"   h. Eliminar('p') → p no estaba → se insertó y eliminó"
            )
            messagebox.showinfo("Resultado — Corregido", texto)


# ╔══════════════════════════════════════════════════════════╗
#  VENTANA PRINCIPAL
# ╚══════════════════════════════════════════════════════════╝

root = tk.Tk()
root.title("Simulación de Pila — Estructura de Datos")
root.configure(bg=BG_DARK)
root.resizable(False, False)

tk.Label(root, text="🗂  SIMULACIÓN DE PILA",
         font=FONT_TITLE, bg=BG_DARK, fg=ACCENT_BLUE).pack(pady=(16, 2))
tk.Label(root, text=f"Capacidad máxima: {CAPACIDAD_MAXIMA} elementos  |  LIFO",
         font=FONT_SMALL, bg=BG_DARK, fg=TEXT_GRAY).pack(pady=(0, 8))

# Estilo de pestañas
style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG_DARK, borderwidth=0)
style.configure("TNotebook.Tab",
                background=BG_PANEL, foreground=TEXT_GRAY,
                font=("Courier New", 11, "bold"),
                padding=[14, 6], borderwidth=0)
style.map("TNotebook.Tab",
          background=[("selected", BG_CARD)],
          foreground=[("selected", ACCENT_BLUE)])

notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(padx=16, pady=4, fill="both", expand=True)

# Crear las dos pestañas
PestañaPila(notebook,
            "⚠️  Original (con errores)",
            OPS_ORIGINAL,
            modo_corregido=False)

PestañaPila(notebook,
            "🔧  Corregido (sin errores)",
            OPS_CORREGIDA,
            modo_corregido=True)


# ╔══════════════════════════════════════════════════════════╗
#  PESTAÑA 3 — ELIMINAR ELEMENTO ESPECÍFICO (CON PASOS)
# ╚══════════════════════════════════════════════════════════╝

class PestañaEliminarEspecifico:
    """
    Pila inicial: [X, Y, V, W, R]  (X en el fondo, R en el tope)
    El usuario elige qué elemento quiere eliminar.
    El programa genera automáticamente los pasos:
      1. Sacar temporalmente los elementos que están ENCIMA del objetivo
      2. Eliminar el objetivo
      3. Reintroducir los elementos temporales en orden inverso
    Cada paso se ejecuta uno a uno con ▶ SIGUIENTE PASO.
    """

    PILA_INICIAL = ["X", "Y", "V", "W", "R"]

    def __init__(self, notebook):
        self.frame = tk.Frame(notebook, bg=BG_DARK)
        notebook.add(self.frame, text="  🎯  Eliminar específico  ")

        self.pila       = list(self.PILA_INICIAL)
        self.pasos      = []          # lista de (tipo, elemento, descripcion)
        self.paso_idx   = 0
        self.en_proceso = False       # True mientras se ejecutan pasos

        self._construir_ui()
        self._dibujar_pila()

    # ── UI ────────────────────────────────────────────────────
    def _construir_ui(self):
        f = self.frame

        def estilo(color):
            return dict(font=FONT_MONO, bg=color, fg=BG_DARK,
                        activebackground=color, activeforeground=BG_DARK,
                        relief="flat", padx=14, pady=7,
                        cursor="hand2", bd=0)

        # ── Fila 1: INSERTAR elemento ─────────────────────────
        ins_frame = tk.Frame(f, bg=BG_PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        ins_frame.pack(padx=18, pady=(12, 3), fill="x")

        tk.Label(ins_frame, text="Insertar elemento:",
                 font=FONT_MONO, bg=BG_PANEL, fg=ACCENT_GRN).pack(side="left", padx=14, pady=8)

        self.var_nuevo = tk.StringVar()
        self.entry_nuevo = tk.Entry(ins_frame, textvariable=self.var_nuevo,
                                    font=FONT_MONO, width=6,
                                    bg=BG_CARD, fg=TEXT_WHITE,
                                    insertbackground=TEXT_WHITE,
                                    relief="flat", bd=4)
        self.entry_nuevo.pack(side="left", padx=8)
        self.entry_nuevo.bind("<Return>", lambda e: self._insertar_elemento())

        self.btn_insertar = tk.Button(ins_frame, text="INSERTAR AL TOPE",
                                      command=self._insertar_elemento,
                                      **estilo(ACCENT_GRN))
        self.btn_insertar.pack(side="left", padx=8)

        self.lbl_ins_msg = tk.Label(ins_frame, text="", font=FONT_SMALL,
                                    bg=BG_PANEL, fg=ACCENT_GRN)
        self.lbl_ins_msg.pack(side="left", padx=10)

        # ── Fila 2: ELIMINAR elemento ─────────────────────────
        sel_frame = tk.Frame(f, bg=BG_PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        sel_frame.pack(padx=18, pady=(3, 6), fill="x")

        tk.Label(sel_frame, text="Eliminar elemento:",
                 font=FONT_MONO, bg=BG_PANEL, fg=ACCENT_RED).pack(side="left", padx=14, pady=8)

        self.var_elem = tk.StringVar(value=self.pila[-1])
        self.combo = ttk.Combobox(sel_frame, textvariable=self.var_elem,
                                  values=list(reversed(self.pila)),
                                  font=FONT_MONO, width=6, state="readonly")
        self.combo.pack(side="left", padx=8)

        tk.Button(sel_frame, text="GENERAR PASOS",
                  command=self._generar_pasos,
                  **estilo(ACCENT_YLW)).pack(side="left", padx=8)

        # ── Área principal ────────────────────────────────────
        main = tk.Frame(f, bg=BG_DARK)
        main.pack(padx=18, pady=4, fill="both")

        # Panel izquierdo — pila visual
        left = tk.Frame(main, bg=BG_PANEL,
                        highlightbackground=BORDER, highlightthickness=1)
        left.grid(row=0, column=0, padx=(0, 10), pady=4, sticky="nsew")

        tk.Label(left, text="PILA", font=FONT_MONO,
                 bg=BG_PANEL, fg=ACCENT_BLUE).pack(pady=(10, 4))

        self.canvas = tk.Canvas(left, width=160, height=CANVAS_H,
                                bg=BG_CARD, highlightthickness=0)
        self.canvas.pack(padx=14, pady=4)

        self.lbl_tope = tk.Label(left, text=f"TOPE = {len(self.pila)}",
                                 font=FONT_MONO, bg=BG_PANEL, fg=ACCENT_YLW)
        self.lbl_tope.pack(pady=(6, 4))

        # Pila temporal (elementos sacados)
        tk.Label(left, text="TEMPORAL", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(4, 2))

        self.canvas_tmp = tk.Canvas(left, width=160, height=120,
                                    bg=BG_CARD, highlightthickness=0)
        self.canvas_tmp.pack(padx=14, pady=(0, 10))

        # Panel derecho — info + log
        right = tk.Frame(main, bg=BG_PANEL,
                         highlightbackground=BORDER, highlightthickness=1)
        right.grid(row=0, column=1, pady=4, sticky="nsew")

        tk.Label(right, text="PASO ACTUAL", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(10, 2))

        self.lbl_operacion = tk.Label(right, text="— Elige un elemento y presiona GENERAR —",
                                      font=FONT_SMALL, bg=BG_CARD, fg=TEXT_WHITE,
                                      width=36, pady=8, wraplength=300)
        self.lbl_operacion.pack(padx=14, pady=2)

        self.lbl_resultado = tk.Label(right, text="", font=FONT_SMALL,
                                      bg=BG_PANEL, fg=ACCENT_GRN,
                                      wraplength=310, justify="left")
        self.lbl_resultado.pack(padx=14, pady=4)

        tk.Label(right, text="SIGUIENTE PASO", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(4, 2))

        self.lbl_siguiente = tk.Label(right, text="—", font=FONT_SMALL,
                                      bg=BG_CARD, fg=TEXT_GRAY,
                                      width=36, pady=6)
        self.lbl_siguiente.pack(padx=14, pady=2)

        tk.Label(right, text="HISTORIAL", font=FONT_SMALL,
                 bg=BG_PANEL, fg=TEXT_GRAY).pack(pady=(8, 2))

        log_wrap = tk.Frame(right, bg=BG_CARD,
                            highlightbackground=BORDER, highlightthickness=1)
        log_wrap.pack(padx=14, pady=2, fill="both", expand=True)

        self.log_text = tk.Text(log_wrap, width=40, height=9,
                                bg=BG_CARD, fg=TEXT_WHITE,
                                font=FONT_LOG, bd=0, state="disabled")
        self.log_text.pack(padx=6, pady=6)

        self.lbl_progreso = tk.Label(right, text="Paso 0 / 0",
                                     font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_GRAY)
        self.lbl_progreso.pack(pady=(4, 0))

        # ── Botones de ejecución ──────────────────────────────
        btn_frame = tk.Frame(f, bg=BG_DARK)
        btn_frame.pack(pady=10)

        self.btn_sig = tk.Button(btn_frame, text="▶  SIGUIENTE PASO",
                                 command=self._ejecutar_paso,
                                 **estilo(ACCENT_BLUE))
        self.btn_sig.grid(row=0, column=0, padx=8)

        self.btn_auto = tk.Button(btn_frame, text="⚡ AUTO COMPLETO",
                                  command=self._auto_completo,
                                  **estilo(ACCENT_YLW))
        self.btn_auto.grid(row=0, column=1, padx=8)

        tk.Button(btn_frame, text="↺  REINICIAR",
                  command=self._reiniciar,
                  **estilo(ACCENT_RED)).grid(row=0, column=2, padx=8)

        # Deshabilitar hasta que se generen pasos
        self.btn_sig.config(state="disabled", bg=TEXT_GRAY)
        self.btn_auto.config(state="disabled", bg=TEXT_GRAY)

    # ── Generar lista de pasos según elemento elegido ─────────
    # ── Insertar nuevo elemento al tope ──────────────────────
    def _insertar_elemento(self):
        val = self.var_nuevo.get().strip()
        if not val:
            self.lbl_ins_msg.config(text="Escribe un valor primero.", fg=ACCENT_RED)
            return
        if len(self.pila) >= CAPACIDAD_MAXIMA:
            self.lbl_ins_msg.config(text=f"Pila llena ({CAPACIDAD_MAXIMA} max).", fg=ACCENT_RED)
            return
        if self.pasos and self.paso_idx < len(self.pasos):
            self.lbl_ins_msg.config(text="Termina o reinicia el proceso actual.", fg=ACCENT_YLW)
            return

        self.pila.append(val)
        self.var_nuevo.set("")
        self._log(f"[+] Insertado '{val}' → pila: {self.pila}")
        self.lbl_ins_msg.config(text=f"'{val}' insertado al tope.", fg=ACCENT_GRN)
        self.frame.after(2000, lambda: self.lbl_ins_msg.config(text=""))
        self._actualizar_combo()
        self._dibujar_pila()
        self.lbl_tope.config(text=f"TOPE = {len(self.pila)}")

    def _actualizar_combo(self):
        vals = list(reversed(self.pila))
        self.combo.config(values=vals)
        if self.pila:
            self.var_elem.set(self.pila[-1])

    def _generar_pasos(self):
        objetivo = self.var_elem.get()

        if objetivo not in self.pila:
            messagebox.showwarning("No encontrado",
                                   f"'{objetivo}' no está en la pila actual.")
            return

        idx_objetivo = self.pila.index(objetivo)   # posición desde el fondo
        # Elementos que están ENCIMA del objetivo (del tope hacia abajo)
        encima = list(reversed(self.pila[idx_objetivo + 1:]))

        pasos = []

        # Fase 1: sacar los que están encima, uno a uno
        for elem in encima:
            pasos.append(("sacar",    elem,
                          f"📤 Sacar '{elem}' temporalmente (está encima de '{objetivo}')"))

        # Fase 2: eliminar el objetivo
        pasos.append(("eliminar", objetivo,
                      f"🗑  Eliminar '{objetivo}' — objetivo alcanzado"))

        # Fase 3: reintroducir en orden inverso (el último sacado entra primero)
        for elem in reversed(encima):
            pasos.append(("reinsertar", elem,
                          f"📥 Reinsertar '{elem}' de vuelta a la pila"))

        self.pasos    = pasos
        self.paso_idx = 0
        self.temporal = []   # pila auxiliar para los elementos sacados

        # Limpiar log
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

        # Actualizar UI
        total = len(pasos)
        self.lbl_progreso.config(text=f"Paso 0 / {total}")
        self.lbl_operacion.config(
            text=f"Listo para eliminar '{objetivo}' ({total} pasos generados)",
            fg=ACCENT_GRN)
        self.lbl_resultado.config(text="")
        self.btn_sig.config(state="normal", bg=ACCENT_BLUE)
        self.btn_auto.config(state="normal", bg=ACCENT_YLW)
        self._actualizar_siguiente()
        self._dibujar_pila()
        self._dibujar_temporal()

        self._actualizar_combo()

    # ── Ejecutar un paso ──────────────────────────────────────
    def _ejecutar_paso(self):
        if self.paso_idx >= len(self.pasos):
            return

        tipo, elem, desc = self.pasos[self.paso_idx]
        self.paso_idx += 1
        total = len(self.pasos)

        if tipo == "sacar":
            self.pila.pop()
            self.temporal.append(elem)
            self.lbl_operacion.config(text=f"📤 Sacar '{elem}'", fg=ACCENT_YLW)
            self.lbl_resultado.config(
                text=f"'{elem}' movido a pila temporal.\nPila: {self.pila}",
                fg=ACCENT_YLW)
            self._log(f"[{self.paso_idx:02d}] 📤 Sacar '{elem}' → temporal: {self.temporal}")

        elif tipo == "eliminar":
            self.pila.pop()
            self.lbl_operacion.config(text=f"🗑  Eliminar '{elem}'", fg=ACCENT_RED)
            self.lbl_resultado.config(
                text=f"'{elem}' eliminado de la pila.\nPila: {self.pila}",
                fg=ACCENT_RED)
            self._log(f"[{self.paso_idx:02d}] 🗑  Eliminado '{elem}' ✅")

        elif tipo == "reinsertar":
            val = self.temporal.pop()
            self.pila.append(val)
            self.lbl_operacion.config(text=f"📥 Reinsertar '{val}'", fg=ACCENT_GRN)
            self.lbl_resultado.config(
                text=f"'{val}' reinsertado en la pila.\nPila: {self.pila}",
                fg=ACCENT_GRN)
            self._log(f"[{self.paso_idx:02d}] 📥 Reinsertar '{val}' → pila: {self.pila}")

        self._dibujar_pila()
        self._dibujar_temporal()
        self.lbl_tope.config(text=f"TOPE = {len(self.pila)}")
        self.lbl_progreso.config(text=f"Paso {self.paso_idx} / {total}")
        self._actualizar_siguiente()

        self._actualizar_combo()

        if self.paso_idx >= total:
            self.btn_sig.config(state="disabled", bg=TEXT_GRAY)
            self.btn_auto.config(state="disabled", bg=TEXT_GRAY)
            self._log(f"─── Proceso completado ───")

    # ── Auto completo ─────────────────────────────────────────
    def _auto_completo(self):
        while self.paso_idx < len(self.pasos):
            self._ejecutar_paso()
            self.frame.update()
            self.frame.after(380)

    # ── Reiniciar a pila original ─────────────────────────────
    def _reiniciar(self):
        self.pila     = list(self.PILA_INICIAL)
        self.temporal = []
        self.pasos    = []
        self.paso_idx = 0
        self._dibujar_pila()
        self._dibujar_temporal()
        self.lbl_tope.config(text=f"TOPE = {len(self.pila)}")
        self.lbl_operacion.config(
            text="— Elige un elemento y presiona GENERAR —", fg=TEXT_WHITE)
        self.lbl_resultado.config(text="")
        self.lbl_siguiente.config(text="—", fg=TEXT_GRAY)
        self.lbl_progreso.config(text="Paso 0 / 0")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self.btn_sig.config(state="disabled", bg=TEXT_GRAY)
        self.btn_auto.config(state="disabled", bg=TEXT_GRAY)
        self.var_nuevo.set("")
        self.lbl_ins_msg.config(text="")
        self._actualizar_combo()

    # ── Actualizar label "siguiente" ──────────────────────────
    def _actualizar_siguiente(self):
        if not self.pasos or self.paso_idx >= len(self.pasos):
            self.lbl_siguiente.config(text="— Fin —", fg=TEXT_GRAY)
            return
        _, _, desc = self.pasos[self.paso_idx]
        colores = {"sacar": ACCENT_YLW, "eliminar": ACCENT_RED, "reinsertar": ACCENT_GRN}
        tipo = self.pasos[self.paso_idx][0]
        self.lbl_siguiente.config(text=desc, fg=colores.get(tipo, TEXT_WHITE))

    # ── Dibujar pila principal ────────────────────────────────
    def _dibujar_pila(self):
        c = self.canvas
        c.delete("all")
        for i in range(CAPACIDAD_MAXIMA):
            y = CANVAS_H - (i + 1) * SLOT_H
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + SLOT_H - 2,
                                fill="#1c2033", outline=BORDER, width=1)
            c.create_text(MARGIN_X + SLOT_W + 16, y + SLOT_H // 2,
                          text=str(i), font=("Courier New", 8),
                          fill=TEXT_GRAY, anchor="w")
        for i, elem in enumerate(self.pila):
            y = CANVAS_H - (i + 1) * SLOT_H
            # Resaltar el objetivo si los pasos están activos
            es_objetivo = (self.pasos and
                           self.paso_idx < len(self.pasos) and
                           self.pasos[self.paso_idx][0] == "eliminar" and
                           elem == self.pasos[self.paso_idx][1])
            color = ACCENT_RED if es_objetivo else COLORES_ELEM[i % len(COLORES_ELEM)]
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + SLOT_H - 2,
                                fill=color, outline="white", width=1)
            c.create_text(MARGIN_X + SLOT_W // 2, y + SLOT_H // 2,
                          text=elem, font=FONT_MONO, fill=BG_DARK)
        if self.pila:
            y_arrow = CANVAS_H - len(self.pila) * SLOT_H + SLOT_H // 2
            c.create_text(MARGIN_X - 6, y_arrow,
                          text="◀", font=("Courier New", 14, "bold"),
                          fill=ACCENT_YLW, anchor="e")

    # ── Dibujar pila temporal ─────────────────────────────────
    def _dibujar_temporal(self):
        c = self.canvas_tmp
        c.delete("all")
        max_tmp = 3
        slot_h  = 34
        for i in range(max_tmp):
            y = 120 - (i + 1) * slot_h
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + slot_h - 2,
                                fill="#1c2033", outline=BORDER, width=1)
        for i, elem in enumerate(self.temporal):
            y = 120 - (i + 1) * slot_h
            c.create_rectangle(MARGIN_X, y, MARGIN_X + SLOT_W, y + slot_h - 2,
                                fill=ACCENT_PRP, outline="white", width=1)
            c.create_text(MARGIN_X + SLOT_W // 2, y + slot_h // 2,
                          text=elem, font=FONT_MONO, fill=BG_DARK)

    # ── Log ───────────────────────────────────────────────────
    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")


# ── Instanciar pestaña 3 ─────────────────────────────────────
PestañaEliminarEspecifico(notebook)

root.mainloop()