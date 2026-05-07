import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# ─────────────────────────────────────────────────────────────────
#  PALETA
# ─────────────────────────────────────────────────────────────────
BG          = "#1e1e2e"
PANEL       = "#2a2a3e"
PANEL2      = "#23233a"
BAR_NORMAL  = "#6c63ff"
BAR_COMPARE = "#f5a623"
BAR_SORTED  = "#50fa7b"
BAR_ACTIVE  = "#ff5555"
TEXT_FG     = "#cdd6f4"
TEXT_DIM    = "#a6adc8"
BTN_BG      = "#3d3d5c"
BTN_ACT     = "#6c63ff"
SEP         = "#44445a"

# Colores por método (para la pestaña de comparación)
COLOR_MD = "#6c63ff"   # Mezcla Directa  — violeta
COLOR_IC = "#f5a623"   # Intercalación   — ámbar
COLOR_ME = "#50fa7b"   # Mezcla Equilibrada — verde

# ─────────────────────────────────────────────────────────────────
#  ALGORITMOS  (generadores de pasos)
# ─────────────────────────────────────────────────────────────────
def mezcla_directa_pasos(arr):
    pasos, a, n, width = [], arr[:], len(arr), 1
    comparaciones = [0]
    movimientos   = [0]
    pasadas       = [0]
    pasos.append((a[:], [], "Inicio — arreglo original"))
    while width < n:
        pasadas[0] += 1
        for i in range(0, n, 2 * width):
            left, mid, right = i, min(i+width, n), min(i+2*width, n)
            L, R, li, ri, ki = a[left:mid], a[mid:right], 0, 0, left
            pasos.append((a[:], list(range(left, right)),
                          f"Bloque [{left}..{right-1}] (ancho={width})"))
            while li < len(L) and ri < len(R):
                comparaciones[0] += 1
                pasos.append((a[:], [left+li, mid+ri],
                              f"Comparando {L[li]} vs {R[ri]}"))
                if L[li] <= R[ri]: a[ki] = L[li]; li += 1
                else:              a[ki] = R[ri]; ri += 1
                movimientos[0] += 1
                ki += 1
                pasos.append((a[:], [ki-1], f"Colocando {a[ki-1]}"))
            while li < len(L):
                a[ki] = L[li]; li += 1; ki += 1; movimientos[0] += 1
                pasos.append((a[:], [ki-1], f"Copiando {a[ki-1]}"))
            while ri < len(R):
                a[ki] = R[ri]; ri += 1; ki += 1; movimientos[0] += 1
                pasos.append((a[:], [ki-1], f"Copiando {a[ki-1]}"))
        width *= 2
        pasos.append((a[:], [], f"Pasada completa — ancho={width}"))
    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    stats = {"comparaciones": comparaciones[0],
             "movimientos":   movimientos[0],
             "pasadas":       pasadas[0]}
    return pasos, stats


def intercalacion_pasos(arr):
    pasos, a, n = [], arr[:], len(arr)
    comparaciones = [0]
    movimientos   = [0]
    pasos.append((a[:], [], "Inicio — arreglo original"))
    for i in range(1, n):
        key, j = a[i], i-1
        pasos.append((a[:], [i], f"Tomando elemento {key} (pos {i})"))
        while j >= 0 and a[j] > key:
            comparaciones[0] += 1
            pasos.append((a[:], [j, j+1], f"Comparando {a[j]} > {key} → desplazar"))
            a[j+1] = a[j]; j -= 1; movimientos[0] += 1
            pasos.append((a[:], [j+1], f"Desplazado a posición {j+1}"))
        if j >= 0: comparaciones[0] += 1   # la comparación que detuvo el while
        a[j+1] = key; movimientos[0] += 1
        pasos.append((a[:], [j+1], f"Insertando {key} en posición {j+1}"))
    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    stats = {"comparaciones": comparaciones[0],
             "movimientos":   movimientos[0],
             "pasadas":       n - 1}
    return pasos, stats


def mezcla_equilibrada_pasos(arr):
    pasos, a, n = [], arr[:], len(arr)
    comparaciones = [0]
    movimientos   = [0]
    pasadas       = [0]
    pasos.append((a[:], [], "Inicio — arreglo original"))

    def get_runs(lst):
        runs, i = [], 0
        while i < len(lst):
            j = i+1
            while j < len(lst) and lst[j] >= lst[j-1]: j += 1
            runs.append((i, j)); i = j
        return runs

    it = 0
    while True:
        runs = get_runs(a)
        pasadas[0] += 1
        pasos.append((a[:], [], f"Pasada {it+1} — {len(runs)} corrida(s)"))
        for s, e in runs:
            pasos.append((a[:], list(range(s, e)),
                          f"Corrida [{s}..{e-1}] = {a[s:e]}"))
        if len(runs) == 1: break
        i = 0
        while i < len(runs):
            if i+1 < len(runs):
                ls, le = runs[i]; rs, re = runs[i+1]
                L, R, li, ri, ki = a[ls:le], a[rs:re], 0, 0, ls
                pasos.append((a[:], list(range(ls, re)),
                              f"Mezclando [{ls}..{le-1}] y [{rs}..{re-1}]"))
                tmp = a[:]
                while li < len(L) and ri < len(R):
                    comparaciones[0] += 1
                    pasos.append((tmp[:], [ls+li, rs+ri],
                                  f"Comparando {L[li]} vs {R[ri]}"))
                    if L[li] <= R[ri]: tmp[ki] = L[li]; li += 1
                    else:              tmp[ki] = R[ri]; ri += 1
                    movimientos[0] += 1; ki += 1
                    pasos.append((tmp[:], [ki-1], f"Colocando {tmp[ki-1]}"))
                while li < len(L):
                    tmp[ki] = L[li]; li += 1; ki += 1; movimientos[0] += 1
                while ri < len(R):
                    tmp[ki] = R[ri]; ri += 1; ki += 1; movimientos[0] += 1
                for idx in range(ls, re): a[idx] = tmp[idx]
                i += 2
            else: i += 1
        it += 1
        pasos.append((a[:], [], f"Fin pasada {it}"))
    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    stats = {"comparaciones": comparaciones[0],
             "movimientos":   movimientos[0],
             "pasadas":       pasadas[0]}
    return pasos, stats


# ─────────────────────────────────────────────────────────────────
#  UTILIDADES DE DIBUJO
# ─────────────────────────────────────────────────────────────────
def dibujar_barras(canvas, arr, highlights, finalizado,
                   bar_color=BAR_NORMAL, w=None, h=None,
                   pad_x=20, pad_y=30, bot=20):
    if w is None: w = canvas.winfo_width()
    if h is None: h = canvas.winfo_height()
    if w < 10 or h < 10: return
    canvas.delete("all")
    n   = len(arr)
    mx  = max(arr) if arr else 1
    avw = w - 2*pad_x
    avh = h - pad_y - bot
    bw  = max(4, avw / n - 2)
    gap = (avw - bw * n) / (n + 1)

    for i, val in enumerate(arr):
        x1 = pad_x + gap + i * (bw + gap)
        bh = (val / mx) * avh
        y1 = h - bot - bh
        y2 = h - bot

        if finalizado:
            color = BAR_SORTED
        elif len(highlights) == 2 and i in highlights:
            color = BAR_COMPARE if i != highlights[0] else BAR_ACTIVE
        elif i in highlights:
            color = BAR_ACTIVE
        else:
            color = bar_color

        r = min(4, bw / 2)
        canvas.create_rectangle(x1, y1+r, x1+bw, y2, fill=color, outline="")
        canvas.create_arc(x1, y1, x1+2*r, y1+2*r,
                          start=90, extent=90, fill=color, outline="")
        canvas.create_arc(x1+bw-2*r, y1, x1+bw, y1+2*r,
                          start=0, extent=90, fill=color, outline="")
        canvas.create_rectangle(x1+r, y1, x1+bw-r, y1+r, fill=color, outline="")

        if bw >= 14:
            canvas.create_text(x1+bw/2, y1-5, text=str(val), fill=TEXT_FG,
                                font=("Segoe UI", max(7, min(10, int(bw*0.55)))))


# ─────────────────────────────────────────────────────────────────
#  PESTAÑA 1 — Visualización individual
# ─────────────────────────────────────────────────────────────────
class TabVisualizacion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.pasos       = []
        self.paso_actual = 0
        self.corriendo   = False
        self.datos       = []
        self._build()
        self._generar_datos()

    def _build(self):
        # ── Controles superiores ──
        top = tk.Frame(self, bg=PANEL, pady=8)
        top.pack(fill="x")

        tk.Label(top, text="Método:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(14,4))
        self.metodo_var = tk.StringVar(value="Mezcla Directa")
        cb = ttk.Combobox(top, textvariable=self.metodo_var, width=22,
                          values=["Mezcla Directa","Intercalación","Mezcla Equilibrada"],
                          state="readonly")
        cb.pack(side="left", padx=(0,16))
        cb.bind("<<ComboboxSelected>>", lambda e: self._reset())

        tk.Label(top, text="Elementos:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0,4))
        self.n_var = tk.IntVar(value=12)
        tk.Spinbox(top, from_=4, to=32, textvariable=self.n_var, width=5,
                   bg=BTN_BG, fg=TEXT_FG, buttonbackground=BTN_BG,
                   relief="flat", font=("Segoe UI", 10)).pack(side="left", padx=(0,14))

        tk.Button(top, text="⟳  Nuevo arreglo", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._generar_datos).pack(side="left", padx=(0,6))

        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        tk.Label(top, text="Velocidad:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0,4))
        self.vel_var = tk.DoubleVar(value=1.0)
        tk.Scale(top, variable=self.vel_var, from_=0.1, to=3.0,
                 resolution=0.1, orient="horizontal", length=110,
                 bg=PANEL, fg=TEXT_FG, troughcolor=BTN_BG,
                 highlightthickness=0, sliderrelief="flat",
                 activebackground=BTN_ACT, showvalue=True,
                 font=("Segoe UI", 8)).pack(side="left", padx=(0,16))

        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        self.btn_play = tk.Button(top, text="▶  Auto", bg=BTN_BG, fg=TEXT_FG,
                                   relief="flat", padx=10, activebackground=BTN_ACT,
                                   activeforeground="white", font=("Segoe UI", 9),
                                   command=self._toggle_auto)
        self.btn_play.pack(side="left", padx=(0,6))

        tk.Button(top, text="Siguiente →", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._siguiente).pack(side="left", padx=(0,6))

        tk.Button(top, text="← Anterior", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._anterior).pack(side="left", padx=(0,6))

        tk.Button(top, text="↺  Reset", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._reset).pack(side="left")

        # ── Canvas ──
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=(10,4))
        self.canvas.bind("<Configure>", lambda e: self._dibujar_paso(self.paso_actual))

        # ── Barra de estado ──
        bot = tk.Frame(self, bg=PANEL, pady=6)
        bot.pack(fill="x")
        self.lbl_paso = tk.Label(bot, text="Paso 0 / 0", bg=PANEL, fg=TEXT_FG,
                                  font=("Segoe UI", 9))
        self.lbl_paso.pack(side="left", padx=14)
        self.lbl_desc = tk.Label(bot, text="", bg=PANEL, fg=TEXT_DIM,
                                  font=("Segoe UI", 9), anchor="w")
        self.lbl_desc.pack(side="left", fill="x", expand=True)
        for color, label in [(BAR_NORMAL,"Normal"),(BAR_COMPARE,"Comparando"),
                              (BAR_ACTIVE,"Activo"),(BAR_SORTED,"Ordenado")]:
            tk.Frame(bot, bg=color, width=12, height=12).pack(side="right", padx=(0,2))
            tk.Label(bot, text=label, bg=PANEL, fg=TEXT_FG,
                     font=("Segoe UI", 8)).pack(side="right", padx=(0,8))

    # ── lógica ──────────────────────────────
    def _generar_datos(self):
        self._detener()
        n = max(4, min(32, self.n_var.get()))
        self.datos = random.sample(range(4, 100), n)
        self._reset()

    def _reset(self):
        self._detener()
        m = self.metodo_var.get()
        fn = {"Mezcla Directa": mezcla_directa_pasos,
              "Intercalación":  intercalacion_pasos,
              "Mezcla Equilibrada": mezcla_equilibrada_pasos}[m]
        self.pasos, _ = fn(self.datos[:])
        self.paso_actual = 0
        self._dibujar_paso(0)

    def _dibujar_paso(self, idx):
        if not self.pasos: return
        idx = max(0, min(idx, len(self.pasos)-1))
        arr, hi, desc = self.pasos[idx]
        dibujar_barras(self.canvas, arr, hi, idx == len(self.pasos)-1)
        self.lbl_paso.config(text=f"Paso {idx+1} / {len(self.pasos)}")
        self.lbl_desc.config(text=desc)
        self.paso_actual = idx

    def _siguiente(self):
        if self.paso_actual < len(self.pasos)-1:
            self._dibujar_paso(self.paso_actual+1)

    def _anterior(self):
        if self.paso_actual > 0:
            self._dibujar_paso(self.paso_actual-1)

    def _toggle_auto(self):
        if self.corriendo: self._detener()
        else:              self._iniciar_auto()

    def _iniciar_auto(self):
        self.corriendo = True
        self.btn_play.config(text="⏸  Pausa")
        threading.Thread(target=self._run_auto, daemon=True).start()

    def _detener(self):
        self.corriendo = False
        self.btn_play.config(text="▶  Auto")

    def _run_auto(self):
        while self.corriendo and self.paso_actual < len(self.pasos)-1:
            time.sleep(max(0.05, 0.6/self.vel_var.get()))
            if self.corriendo:
                self.after(0, self._siguiente)
        self.after(0, self._detener)


# ─────────────────────────────────────────────────────────────────
#  PESTAÑA 2 — Comparación side-by-side
# ─────────────────────────────────────────────────────────────────
class PanelMetodo(tk.Frame):
    """Un panel de comparación para un solo método."""
    def __init__(self, parent, nombre, color, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)
        self.nombre   = nombre
        self.color    = color
        self.pasos    = []
        self.idx      = 0
        self.terminado = False

        # Cabecera con nombre del método
        hdr = tk.Frame(self, bg=PANEL2, pady=4)
        hdr.pack(fill="x")
        dot = tk.Frame(hdr, bg=color, width=10, height=10)
        dot.pack(side="left", padx=(10,6))
        tk.Label(hdr, text=nombre, bg=PANEL2, fg=TEXT_FG,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        self.lbl_pasos = tk.Label(hdr, text="— pasos", bg=PANEL2, fg=TEXT_DIM,
                                   font=("Segoe UI", 9))
        self.lbl_pasos.pack(side="right", padx=10)

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=6, pady=4)
        self.canvas.bind("<Configure>", lambda e: self._dibujar())

        # Estado
        self.lbl_desc = tk.Label(self, text="", bg=PANEL, fg=TEXT_DIM,
                                  font=("Segoe UI", 8), anchor="w")
        self.lbl_desc.pack(fill="x", padx=6, pady=(0,4))

    def cargar(self, datos):
        fn = {"Mezcla Directa":      mezcla_directa_pasos,
              "Intercalación":       intercalacion_pasos,
              "Mezcla Equilibrada":  mezcla_equilibrada_pasos}[self.nombre]
        self.pasos, self.stats = fn(datos[:])
        self.idx       = 0
        self.terminado = False
        self.lbl_pasos.config(text=f"— {len(self.pasos)} pasos")
        self._dibujar()

    def avanzar(self):
        if self.idx < len(self.pasos)-1:
            self.idx += 1
        else:
            self.terminado = True
        self._dibujar()

    def reset(self):
        self.idx = 0
        self.terminado = False
        self._dibujar()

    def _dibujar(self):
        if not self.pasos: return
        arr, hi, desc = self.pasos[self.idx]
        dibujar_barras(self.canvas, arr, hi,
                       self.idx == len(self.pasos)-1,
                       bar_color=self.color, bot=6)
        self.lbl_desc.config(text=desc)


class TabComparacion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.datos     = []
        self.corriendo = False
        self._build()
        self._generar_datos()

    def _build(self):
        # ── Controles superiores ──
        top = tk.Frame(self, bg=PANEL, pady=8)
        top.pack(fill="x")

        tk.Label(top, text="Elementos:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(14,4))
        self.n_var = tk.IntVar(value=12)
        tk.Spinbox(top, from_=4, to=32, textvariable=self.n_var, width=5,
                   bg=BTN_BG, fg=TEXT_FG, buttonbackground=BTN_BG,
                   relief="flat", font=("Segoe UI", 10)).pack(side="left", padx=(0,14))

        tk.Button(top, text="⟳  Nuevo arreglo", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._generar_datos).pack(side="left", padx=(0,6))

        tk.Button(top, text="↺  Reset", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._reset).pack(side="left", padx=(0,16))

        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        tk.Label(top, text="Velocidad:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0,4))
        self.vel_var = tk.DoubleVar(value=1.0)
        tk.Scale(top, variable=self.vel_var, from_=0.1, to=3.0,
                 resolution=0.1, orient="horizontal", length=110,
                 bg=PANEL, fg=TEXT_FG, troughcolor=BTN_BG,
                 highlightthickness=0, sliderrelief="flat",
                 activebackground=BTN_ACT, showvalue=True,
                 font=("Segoe UI", 8)).pack(side="left", padx=(0,16))

        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        self.btn_play = tk.Button(top, text="▶  Comparar", bg=BTN_BG, fg=TEXT_FG,
                                   relief="flat", padx=12, activebackground=BTN_ACT,
                                   activeforeground="white", font=("Segoe UI", 9, "bold"),
                                   command=self._toggle_auto)
        self.btn_play.pack(side="left", padx=(0,6))

        tk.Button(top, text="Siguiente →", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._paso_manual).pack(side="left")

        # ── Tres paneles lado a lado ──
        contenedor = tk.Frame(self, bg=BG)
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)
        contenedor.columnconfigure(2, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self.panel_md = PanelMetodo(contenedor, "Mezcla Directa",     COLOR_MD)
        self.panel_ic = PanelMetodo(contenedor, "Intercalación",      COLOR_IC)
        self.panel_me = PanelMetodo(contenedor, "Mezcla Equilibrada", COLOR_ME)

        self.panel_md.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        self.panel_ic.grid(row=0, column=1, sticky="nsew", padx=4)
        self.panel_me.grid(row=0, column=2, sticky="nsew", padx=(4,0))

        # ── Barra inferior con resumen ──
        self.bot_frame = tk.Frame(self, bg=PANEL, pady=6)
        self.bot_frame.pack(fill="x")
        self.lbl_estado = tk.Label(self.bot_frame,
                                    text="Presiona '⟳ Nuevo arreglo' y luego '▶ Comparar'",
                                    bg=PANEL, fg=TEXT_DIM, font=("Segoe UI", 9))
        self.lbl_estado.pack(side="left", padx=14)

        # Leyenda de colores
        for color, label in [(COLOR_MD,"Mezcla Directa"),
                              (COLOR_IC,"Intercalación"),
                              (COLOR_ME,"Mezcla Equilibrada")]:
            tk.Frame(self.bot_frame, bg=color, width=12, height=12).pack(side="right", padx=(0,2))
            tk.Label(self.bot_frame, text=label, bg=PANEL, fg=TEXT_FG,
                     font=("Segoe UI", 8)).pack(side="right", padx=(0,8))

    # ── lógica ──────────────────────────────
    def _generar_datos(self):
        self._detener()
        self._modal_mostrado = False
        n = max(4, min(32, self.n_var.get()))
        self.datos = random.sample(range(4, 100), n)
        for p in (self.panel_md, self.panel_ic, self.panel_me):
            p.cargar(self.datos)
        self._actualizar_estado()

    def _reset(self):
        self._detener()
        self._modal_mostrado = False
        for p in (self.panel_md, self.panel_ic, self.panel_me):
            p.reset()
        self._actualizar_estado()

    def _paso_manual(self):
        if not any(p.pasos for p in (self.panel_md, self.panel_ic, self.panel_me)):
            return
        for p in (self.panel_md, self.panel_ic, self.panel_me):
            if not p.terminado:
                p.avanzar()
        self._actualizar_estado()

    def _toggle_auto(self):
        if self.corriendo: self._detener()
        else:              self._iniciar_auto()

    def _iniciar_auto(self):
        self.corriendo = True
        self.btn_play.config(text="⏸  Pausar")
        threading.Thread(target=self._run_auto, daemon=True).start()

    def _detener(self):
        self.corriendo = False
        self.btn_play.config(text="▶  Comparar")

    def _run_auto(self):
        paneles = [self.panel_md, self.panel_ic, self.panel_me]
        while self.corriendo and not all(p.terminado for p in paneles):
            time.sleep(max(0.04, 0.5 / self.vel_var.get()))
            if self.corriendo:
                self.after(0, self._paso_un_tick)
        self.after(0, self._detener)
        self.after(0, self._actualizar_estado)

    def _paso_un_tick(self):
        for p in (self.panel_md, self.panel_ic, self.panel_me):
            if not p.terminado:
                p.avanzar()
        self._actualizar_estado()

    def _actualizar_estado(self):
        paneles = [self.panel_md, self.panel_ic, self.panel_me]
        todos_listo = all(p.terminado for p in paneles)
        if todos_listo and all(p.pasos for p in paneles):
            total = [len(p.pasos) for p in paneles]
            nombres = ["M. Directa", "Intercalación", "M. Equilibrada"]
            ganador = nombres[total.index(min(total))]
            self.lbl_estado.config(
                text=f"¡Completado! Menos pasos: {ganador}  —  ver resultados detallados abajo",
                fg=BAR_SORTED)
            if not getattr(self, "_modal_mostrado", False):
                self._modal_mostrado = True
                self.after(400, self._mostrar_resultados)
        elif any(p.pasos for p in paneles):
            self._modal_mostrado = False
            idx_max = max(p.idx for p in paneles)
            self.lbl_estado.config(
                text=f"Paso {idx_max + 1}  —  todos parten del mismo arreglo",
                fg=TEXT_DIM)

    def _mostrar_resultados(self):
        paneles = [self.panel_md, self.panel_ic, self.panel_me]
        nombres  = ["Mezcla Directa", "Intercalación", "Mezcla Equilibrada"]
        colores  = [COLOR_MD, COLOR_IC, COLOR_ME]
        compl_t  = ["O(n log n)", "O(n²)", "O(n log n)"]
        compl_e  = ["O(n)", "O(1)", "O(n)"]
        descrip  = [
            "Divide en bloques de tamaño fijo que\nse duplican en cada pasada.",
            "Inserta cada elemento en su posición\ncorrecta dentro de la parte ordenada.",
            "Detecta corridas naturales y las\nmezcla en cada iteración.",
        ]

        stats = []
        for p in paneles:
            s = getattr(p, "stats", {})
            stats.append({
                "pasos":         len(p.pasos),
                "comparaciones": s.get("comparaciones", "—"),
                "movimientos":   s.get("movimientos",   "—"),
                "pasadas":       s.get("pasadas",       "—"),
            })

        totales_pasos = [s["pasos"] for s in stats]
        min_pasos = min(totales_pasos)
        ganador_idx = totales_pasos.index(min_pasos)

        # ── Ventana modal ──
        win = tk.Toplevel(self)
        win.title("Resultados de la comparación")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.grab_set()

        # Centrar sobre la ventana principal
        self.update_idletasks()
        rx = self.winfo_rootx(); ry = self.winfo_rooty()
        rw = self.winfo_width(); rh = self.winfo_height()
        ww, wh = 780, 560
        win.geometry(f"{ww}x{wh}+{rx + (rw-ww)//2}+{ry + (rh-wh)//2}")

        # ── Título ──
        tk.Label(win, text="Resultados de la comparación",
                 bg=BG, fg=TEXT_FG, font=("Segoe UI", 14, "bold")).pack(pady=(18,2))
        tk.Label(win, text=f"Arreglo de {len(self.datos)} elementos",
                 bg=BG, fg=TEXT_DIM, font=("Segoe UI", 9)).pack(pady=(0,14))

        # ── Tarjetas ──
        cards_frame = tk.Frame(win, bg=BG)
        cards_frame.pack(fill="x", padx=20)

        for i, (nombre, color, st, ct, ce, desc) in enumerate(
                zip(nombres, colores, stats, compl_t, compl_e, descrip)):
            es_ganador = (i == ganador_idx)

            card = tk.Frame(cards_frame, bg=PANEL,
                            highlightbackground=color if es_ganador else SEP,
                            highlightthickness=2 if es_ganador else 1)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)

            # Franja de color superior
            tk.Frame(card, bg=color, height=4).pack(fill="x")

            inner = tk.Frame(card, bg=PANEL, padx=12, pady=10)
            inner.pack(fill="both", expand=True)

            # Trofeo si ganó
            if es_ganador:
                tk.Label(inner, text="🏆 GANADOR", bg=PANEL,
                         fg=BAR_SORTED, font=("Segoe UI", 8, "bold")).pack(anchor="center")

            tk.Label(inner, text=nombre, bg=PANEL, fg=color,
                     font=("Segoe UI", 11, "bold"),
                     wraplength=200).pack(anchor="center", pady=(2,6))

            # Métricas
            filas = [
                ("Pasos totales",   st["pasos"]),
                ("Comparaciones",   st["comparaciones"]),
                ("Movimientos",     st["movimientos"]),
                ("Pasadas",         st["pasadas"]),
            ]
            for etiq, val in filas:
                fila = tk.Frame(inner, bg=PANEL)
                fila.pack(fill="x", pady=1)
                tk.Label(fila, text=etiq, bg=PANEL, fg=TEXT_DIM,
                         font=("Segoe UI", 8), anchor="w").pack(side="left")
                tk.Label(fila, text=str(val), bg=PANEL, fg=TEXT_FG,
                         font=("Segoe UI", 9, "bold"), anchor="e").pack(side="right")

            # Separador
            tk.Frame(inner, bg=SEP, height=1).pack(fill="x", pady=6)

            # Complejidad
            tk.Label(inner, text="Complejidad", bg=PANEL, fg=TEXT_DIM,
                     font=("Segoe UI", 8)).pack(anchor="w")
            comp_row = tk.Frame(inner, bg=PANEL)
            comp_row.pack(fill="x", pady=(2,0))
            tk.Label(comp_row, text=f"Tiempo: {ct}", bg=PANEL, fg=TEXT_FG,
                     font=("Segoe UI", 8)).pack(side="left")
            tk.Label(comp_row, text=f"Espacio: {ce}", bg=PANEL, fg=TEXT_FG,
                     font=("Segoe UI", 8)).pack(side="right")

            # Descripción
            tk.Frame(inner, bg=SEP, height=1).pack(fill="x", pady=6)
            tk.Label(inner, text=desc, bg=PANEL, fg=TEXT_DIM,
                     font=("Segoe UI", 8), justify="left",
                     wraplength=190).pack(anchor="w")

        # ── Tabla resumen comparativa ──
        tk.Frame(win, bg=SEP, height=1).pack(fill="x", padx=20, pady=(18,0))
        tk.Label(win, text="Resumen comparativo", bg=BG, fg=TEXT_DIM,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(8,4))

        tabla = tk.Frame(win, bg=PANEL2)
        tabla.pack(fill="x", padx=20)

        headers = ["Método", "Pasos", "Comparaciones", "Movimientos", "Pasadas",
                   "T. Tiempo", "T. Espacio"]
        for j, h_txt in enumerate(headers):
            tk.Label(tabla, text=h_txt, bg=PANEL2, fg=TEXT_DIM,
                     font=("Segoe UI", 8, "bold"),
                     padx=10, pady=4, anchor="center").grid(row=0, column=j, sticky="ew")
            tabla.columnconfigure(j, weight=1)

        tk.Frame(tabla, bg=SEP, height=1).grid(
            row=1, column=0, columnspan=len(headers), sticky="ew")

        for i, (nombre, st, ct, ce) in enumerate(zip(nombres, stats, compl_t, compl_e)):
            fila_bg  = PANEL if i % 2 == 0 else PANEL2
            es_gan   = (i == ganador_idx)
            fg_color = BAR_SORTED if es_gan else TEXT_FG
            fila_datos = [
                nombre,
                str(st["pasos"]),
                str(st["comparaciones"]),
                str(st["movimientos"]),
                str(st["pasadas"]),
                ct, ce,
            ]
            for j, val in enumerate(fila_datos):
                tk.Label(tabla, text=val, bg=fila_bg, fg=fg_color,
                         font=("Segoe UI", 8 if j > 0 else 9),
                         padx=10, pady=3, anchor="center").grid(
                    row=i+2, column=j, sticky="ew")

        # ── Nota y botón cerrar ──
        nota = tk.Frame(win, bg=BG)
        nota.pack(fill="x", padx=20, pady=(10,0))
        tk.Label(nota,
                 text="* Los pasos incluyen comparaciones, movimientos y mensajes de estado de la visualización.",
                 bg=BG, fg=TEXT_DIM, font=("Segoe UI", 8),
                 anchor="w").pack(side="left")

        tk.Button(win, text="  Cerrar  ", bg=BTN_ACT, fg="white",
                  relief="flat", padx=14, pady=6,
                  activebackground="#5550cc", activeforeground="white",
                  font=("Segoe UI", 9, "bold"),
                  command=win.destroy).pack(pady=14)


# ─────────────────────────────────────────────────────────────────
#  VENTANA PRINCIPAL
# ─────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Métodos de Ordenamiento")
        self.configure(bg=BG)
        self.geometry("1100x660")
        self.minsize(800, 520)

        # Estilo para el Notebook
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook",            background=PANEL, borderwidth=0)
        style.configure("TNotebook.Tab",        background=BTN_BG, foreground=TEXT_DIM,
                         padding=[16, 6], font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", TEXT_FG)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.tab_viz  = TabVisualizacion(nb)
        self.tab_cmp  = TabComparacion(nb)

        nb.add(self.tab_viz, text="  Visualización  ")
        nb.add(self.tab_cmp, text="  Comparación  ")


if __name__ == "__main__":
    App().mainloop()