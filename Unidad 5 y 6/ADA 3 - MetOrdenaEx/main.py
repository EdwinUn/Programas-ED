import tkinter as tk
from tkinter import ttk
import random
import time
import threading

# ─────────────────────────────────────────────
#  COLORES
# ─────────────────────────────────────────────
BG          = "#1e1e2e"
PANEL       = "#2a2a3e"
BAR_NORMAL  = "#6c63ff"
BAR_COMPARE = "#f5a623"
BAR_SORTED  = "#50fa7b"
BAR_ACTIVE  = "#ff5555"
TEXT_FG     = "#cdd6f4"
BTN_BG      = "#3d3d5c"
BTN_ACT     = "#6c63ff"
SEP         = "#44445a"

# ─────────────────────────────────────────────
#  GENERADOR DE PASOS — Mezcla Directa
# ─────────────────────────────────────────────
def mezcla_directa_pasos(arr):
    """
    Merge sort bottom-up (mezcla directa / straight merge).
    Genera pasos: (array_snapshot, indices_comparando, descripcion)
    """
    pasos = []
    n = len(arr)
    a = arr[:]
    width = 1

    pasos.append((a[:], [], f"Inicio — arreglo original"))

    while width < n:
        for i in range(0, n, 2 * width):
            left  = i
            mid   = min(i + width, n)
            right = min(i + 2 * width, n)

            L = a[left:mid]
            R = a[mid:right]

            li = ri = 0
            ki = left

            pasos.append((a[:], list(range(left, right)),
                          f"Mezcla directa — bloque [{left}..{right-1}] (ancho={width})"))

            while li < len(L) and ri < len(R):
                pasos.append((a[:], [left + li, mid + ri],
                              f"Comparando {L[li]} vs {R[ri]}"))
                if L[li] <= R[ri]:
                    a[ki] = L[li]; li += 1
                else:
                    a[ki] = R[ri]; ri += 1
                ki += 1
                pasos.append((a[:], [ki - 1], f"Colocando {a[ki-1]} en posición {ki-1}"))

            while li < len(L):
                a[ki] = L[li]; li += 1; ki += 1
                pasos.append((a[:], [ki - 1], f"Copiando restante {a[ki-1]}"))
            while ri < len(R):
                a[ki] = R[ri]; ri += 1; ki += 1
                pasos.append((a[:], [ki - 1], f"Copiando restante {a[ki-1]}"))

        width *= 2
        pasos.append((a[:], [], f"Pasada completa — ancho ahora = {width}"))

    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    return pasos


# ─────────────────────────────────────────────
#  GENERADOR DE PASOS — Intercalación (Insertion Sort)
# ─────────────────────────────────────────────
def intercalacion_pasos(arr):
    """
    Ordenamiento por intercalación (insertion sort).
    """
    pasos = []
    a = arr[:]
    n = len(a)

    pasos.append((a[:], [], "Inicio — arreglo original"))

    for i in range(1, n):
        key = a[i]
        j = i - 1
        pasos.append((a[:], [i], f"Intercalación — tomando elemento {key} (pos {i})"))

        while j >= 0 and a[j] > key:
            pasos.append((a[:], [j, j + 1], f"Comparando {a[j]} > {key} → desplazar"))
            a[j + 1] = a[j]
            j -= 1
            pasos.append((a[:], [j + 1], f"Desplazado a posición {j + 1}"))

        a[j + 1] = key
        pasos.append((a[:], [j + 1], f"Insertando {key} en posición {j + 1}"))

    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    return pasos


# ─────────────────────────────────────────────
#  GENERADOR DE PASOS — Mezcla Equilibrada (Natural Merge)
# ─────────────────────────────────────────────
def mezcla_equilibrada_pasos(arr):
    """
    Natural merge sort — detecta corridas naturales y las mezcla.
    """
    pasos = []
    a = arr[:]
    n = len(a)

    pasos.append((a[:], [], "Inicio — arreglo original"))

    def get_runs(lst):
        runs = []
        i = 0
        while i < len(lst):
            j = i + 1
            while j < len(lst) and lst[j] >= lst[j - 1]:
                j += 1
            runs.append((i, j))
            i = j
        return runs

    iteracion = 0
    while True:
        runs = get_runs(a)
        pasos.append((a[:], [], f"Pasada {iteracion + 1} — {len(runs)} corrida(s) detectada(s)"))

        for start, end in runs:
            pasos.append((a[:], list(range(start, end)),
                          f"Corrida natural: [{start}..{end-1}] = {a[start:end]}"))

        if len(runs) == 1:
            break

        new_a = [0] * n
        i = 0
        while i < len(runs):
            if i + 1 < len(runs):
                ls, le = runs[i]
                rs, re = runs[i + 1]
                L = a[ls:le]
                R = a[rs:re]
                li = ri = 0
                ki = ls

                pasos.append((a[:], list(range(ls, re)),
                              f"Mezclando corridas [{ls}..{le-1}] y [{rs}..{re-1}]"))

                tmp = a[:]
                while li < len(L) and ri < len(R):
                    pasos.append((tmp[:], [ls + li, rs + ri],
                                  f"Comparando {L[li]} vs {R[ri]}"))
                    if L[li] <= R[ri]:
                        tmp[ki] = L[li]; li += 1
                    else:
                        tmp[ki] = R[ri]; ri += 1
                    ki += 1
                    pasos.append((tmp[:], [ki - 1], f"Colocando {tmp[ki-1]}"))

                while li < len(L):
                    tmp[ki] = L[li]; li += 1; ki += 1
                while ri < len(R):
                    tmp[ki] = R[ri]; ri += 1; ki += 1

                for idx in range(ls, re):
                    a[idx] = tmp[idx]
                i += 2
            else:
                i += 1

        iteracion += 1
        pasos.append((a[:], [], f"Fin pasada {iteracion}"))

    pasos.append((a[:], list(range(n)), "¡Ordenado!"))
    return pasos


# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Métodos de Ordenamiento")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.geometry("980x640")
        self.minsize(700, 500)

        self.pasos      = []
        self.paso_actual = 0
        self.corriendo  = False
        self.hilo       = None
        self.datos      = []

        self._build_ui()
        self._generar_datos()

    # ── UI ──────────────────────────────────
    def _build_ui(self):
        # ── Barra superior de controles ──
        top = tk.Frame(self, bg=PANEL, pady=8)
        top.pack(fill="x", padx=0, pady=0)

        # Método
        tk.Label(top, text="Método:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(14, 4))
        self.metodo_var = tk.StringVar(value="Mezcla Directa")
        cb = ttk.Combobox(top, textvariable=self.metodo_var, width=22,
                          values=["Mezcla Directa", "Intercalación", "Mezcla Equilibrada"],
                          state="readonly")
        cb.pack(side="left", padx=(0, 18))
        cb.bind("<<ComboboxSelected>>", lambda e: self._reset())

        # Cantidad
        tk.Label(top, text="Elementos:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 4))
        self.n_var = tk.IntVar(value=12)
        sp = tk.Spinbox(top, from_=4, to=32, textvariable=self.n_var,
                        width=5, bg=BTN_BG, fg=TEXT_FG,
                        buttonbackground=BTN_BG, relief="flat",
                        font=("Segoe UI", 10))
        sp.pack(side="left", padx=(0, 18))

        # Botón nuevo arreglo
        tk.Button(top, text="⟳  Nuevo arreglo", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10, activebackground=BTN_ACT,
                  activeforeground="white", font=("Segoe UI", 9),
                  command=self._generar_datos).pack(side="left", padx=(0, 6))

        # Separador visual
        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        # Velocidad
        tk.Label(top, text="Velocidad:", bg=PANEL, fg=TEXT_FG,
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 4))
        self.vel_var = tk.DoubleVar(value=1.0)
        sc = tk.Scale(top, variable=self.vel_var, from_=0.1, to=3.0,
                      resolution=0.1, orient="horizontal", length=120,
                      bg=PANEL, fg=TEXT_FG, troughcolor=BTN_BG,
                      highlightthickness=0, sliderrelief="flat",
                      activebackground=BTN_ACT, showvalue=True,
                      font=("Segoe UI", 8))
        sc.pack(side="left", padx=(0, 18))

        # Separador
        tk.Frame(top, bg=SEP, width=1, height=28).pack(side="left", padx=10)

        # Botones de control
        self.btn_play = tk.Button(top, text="▶  Auto", bg=BTN_BG, fg=TEXT_FG,
                                   relief="flat", padx=10,
                                   activebackground=BTN_ACT, activeforeground="white",
                                   font=("Segoe UI", 9), command=self._toggle_auto)
        self.btn_play.pack(side="left", padx=(0, 6))

        self.btn_next = tk.Button(top, text="Siguiente →", bg=BTN_BG, fg=TEXT_FG,
                                   relief="flat", padx=10,
                                   activebackground=BTN_ACT, activeforeground="white",
                                   font=("Segoe UI", 9), command=self._siguiente)
        self.btn_next.pack(side="left", padx=(0, 6))

        self.btn_prev = tk.Button(top, text="← Anterior", bg=BTN_BG, fg=TEXT_FG,
                                   relief="flat", padx=10,
                                   activebackground=BTN_ACT, activeforeground="white",
                                   font=("Segoe UI", 9), command=self._anterior)
        self.btn_prev.pack(side="left", padx=(0, 6))

        tk.Button(top, text="↺  Reset", bg=BTN_BG, fg=TEXT_FG,
                  relief="flat", padx=10,
                  activebackground=BTN_ACT, activeforeground="white",
                  font=("Segoe UI", 9), command=self._reset).pack(side="left")

        # ── Canvas ──
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=16, pady=(10, 4))

        # ── Barra inferior de estado ──
        bot = tk.Frame(self, bg=PANEL, pady=6)
        bot.pack(fill="x")

        self.lbl_paso = tk.Label(bot, text="Paso 0 / 0", bg=PANEL, fg=TEXT_FG,
                                  font=("Segoe UI", 9))
        self.lbl_paso.pack(side="left", padx=14)

        self.lbl_desc = tk.Label(bot, text="", bg=PANEL, fg="#a6adc8",
                                  font=("Segoe UI", 9), anchor="w")
        self.lbl_desc.pack(side="left", fill="x", expand=True, padx=6)

        # Leyenda
        for color, etiqueta in [(BAR_NORMAL, "Normal"), (BAR_COMPARE, "Comparando"),
                                 (BAR_ACTIVE, "Activo"), (BAR_SORTED, "Ordenado")]:
            tk.Frame(bot, bg=color, width=12, height=12).pack(side="right", padx=(0, 2))
            tk.Label(bot, text=etiqueta, bg=PANEL, fg=TEXT_FG,
                     font=("Segoe UI", 8)).pack(side="right", padx=(0, 8))

    # ── Datos y pasos ────────────────────────
    def _generar_datos(self):
        self._detener()
        n = max(4, min(32, self.n_var.get()))
        self.datos = random.sample(range(4, 100), n)
        self._reset()

    def _reset(self):
        self._detener()
        metodo = self.metodo_var.get()
        if metodo == "Mezcla Directa":
            self.pasos = mezcla_directa_pasos(self.datos[:])
        elif metodo == "Intercalación":
            self.pasos = intercalacion_pasos(self.datos[:])
        else:
            self.pasos = mezcla_equilibrada_pasos(self.datos[:])
        self.paso_actual = 0
        self._dibujar_paso(0)

    # ── Dibujo ──────────────────────────────
    def _dibujar_paso(self, idx):
        if not self.pasos:
            return
        idx = max(0, min(idx, len(self.pasos) - 1))
        arr, highlights, desc = self.pasos[idx]

        es_final = (idx == len(self.pasos) - 1)

        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            self.after(50, lambda: self._dibujar_paso(idx))
            return

        n     = len(arr)
        mx    = max(arr) if arr else 1
        pad_x = 20
        pad_y = 30
        avail_w = w - 2 * pad_x
        avail_h = h - pad_y - 20
        bar_w   = max(4, avail_w / n - 2)
        gap     = (avail_w - bar_w * n) / (n + 1)

        for i, val in enumerate(arr):
            x1 = pad_x + gap + i * (bar_w + gap)
            bh = (val / mx) * avail_h
            y1 = h - 20 - bh
            y2 = h - 20

            if es_final:
                color = BAR_SORTED
            elif len(highlights) == 2 and i in highlights:
                color = BAR_COMPARE if i != highlights[0] else BAR_ACTIVE
            elif i in highlights:
                color = BAR_ACTIVE
            else:
                color = BAR_NORMAL

            # Barra con esquinas superiores redondeadas (simulado)
            r = min(4, bar_w / 2)
            self.canvas.create_rectangle(x1, y1 + r, x1 + bar_w, y2,
                                          fill=color, outline="", width=0)
            self.canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r,
                                    start=90, extent=90, fill=color, outline="")
            self.canvas.create_arc(x1 + bar_w - 2*r, y1, x1 + bar_w, y1 + 2*r,
                                    start=0, extent=90, fill=color, outline="")
            self.canvas.create_rectangle(x1 + r, y1, x1 + bar_w - r, y1 + r,
                                          fill=color, outline="")

            # Valor encima si hay espacio
            if bar_w >= 14:
                self.canvas.create_text(x1 + bar_w / 2, y1 - 5,
                                         text=str(val), fill=TEXT_FG,
                                         font=("Segoe UI", max(7, min(10, int(bar_w * 0.55)))))

        # Actualizar etiquetas
        self.lbl_paso.config(text=f"Paso {idx + 1} / {len(self.pasos)}")
        self.lbl_desc.config(text=desc)
        self.paso_actual = idx

    # ── Navegación ──────────────────────────
    def _siguiente(self):
        if self.paso_actual < len(self.pasos) - 1:
            self._dibujar_paso(self.paso_actual + 1)

    def _anterior(self):
        if self.paso_actual > 0:
            self._dibujar_paso(self.paso_actual - 1)

    def _toggle_auto(self):
        if self.corriendo:
            self._detener()
        else:
            self._iniciar_auto()

    def _iniciar_auto(self):
        self.corriendo = True
        self.btn_play.config(text="⏸  Pausa")
        self.hilo = threading.Thread(target=self._run_auto, daemon=True)
        self.hilo.start()

    def _detener(self):
        self.corriendo = False
        self.btn_play.config(text="▶  Auto")

    def _run_auto(self):
        while self.corriendo and self.paso_actual < len(self.pasos) - 1:
            delay = max(0.05, 0.6 / self.vel_var.get())
            time.sleep(delay)
            if self.corriendo:
                self.after(0, self._siguiente)
        self.after(0, self._detener)

    # ── Resize ──────────────────────────────
    def _on_resize(self, event):
        self._dibujar_paso(self.paso_actual)


if __name__ == "__main__":
    app = App()
    app.canvas.bind("<Configure>", app._on_resize)
    app.mainloop()