"""
Visualizador de Métodos de Ordenamiento
Animación correcta con root.after() — sin threads ni time.sleep()
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from sorting_algorithms import (
    shell_sort_generator,
    quicksort_generator,
    heapsort_generator,
    radix_sort_generator,
)

# ── Paleta de colores ────────────────────────────────────────────────
BG_DARK    = "#1a1a2e"
BG_PANEL   = "#16213e"
BG_CARD    = "#0f3460"
COL_NORMAL = "#4cc9f0"
COL_CMP    = "#f72585"   # rojo/rosa  → comparando
COL_PIVOT  = "#ffd60a"   # amarillo   → pivote / elemento activo
COL_SORTED = "#06d6a0"   # verde      → ya ordenado
COL_TEXT   = "#e2e8f0"
COL_MUTED  = "#94a3b8"

ALGORITHMS = {
    "Shell Sort":  ("shell",  shell_sort_generator),
    "Quicksort":   ("quick",  quicksort_generator),
    "Heapsort":    ("heap",   heapsort_generator),
    "Radix Sort":  ("radix",  radix_sort_generator),
}


class SortingVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Visualizador de Métodos de Ordenamiento")
        self.root.geometry("1100x720")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(700, 500)

        # ── Estado ───────────────────────────────────────────────────
        self._original: list[float] = []   # copia sin tocar para Reset
        self.array:     list[float] = []
        self.sorted_indices: set[int] = set()
        self.highlight:  list[int]   = []   # índices resaltados ahora

        self._generator   = None            # generador activo
        self._after_id    = None            # id de root.after pendiente
        self._running     = False           # ¿animando?
        self._paused      = False
        self._steps       = 0

        self._build_ui()

    # ================================================================
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ================================================================
    def _build_ui(self):
        # ── Barra superior ──────────────────────────────────────────
        top = tk.Frame(self.root, bg=BG_PANEL, pady=8)
        top.pack(fill=tk.X, padx=0, pady=0)

        # Selector de algoritmo
        tk.Label(top, text="Algoritmo:", bg=BG_PANEL, fg=COL_TEXT,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(12, 4))

        self._algo_var = tk.StringVar(value="Shell Sort")
        algo_menu = ttk.Combobox(top, textvariable=self._algo_var,
                                 values=list(ALGORITHMS.keys()),
                                 state="readonly", width=14,
                                 font=("Segoe UI", 10))
        algo_menu.pack(side=tk.LEFT, padx=4)

        sep = tk.Frame(top, bg=COL_MUTED, width=1, height=30)
        sep.pack(side=tk.LEFT, padx=10)

        # Botones
        btn_cfg = dict(bg=BG_CARD, fg=COL_TEXT, relief=tk.FLAT,
                       font=("Segoe UI", 9, "bold"), padx=12, pady=5,
                       cursor="hand2", activebackground="#1e4080",
                       activeforeground="white")

        self._btn_load  = tk.Button(top, text="⬆ Cargar", command=self._load_numbers, **btn_cfg)
        self._btn_start = tk.Button(top, text="▶ Iniciar",  command=self._start,  **btn_cfg)
        self._btn_pause = tk.Button(top, text="⏸ Pausa",   command=self._pause,  **btn_cfg)
        self._btn_reset = tk.Button(top, text="↺ Reiniciar",command=self._reset,  **btn_cfg)

        for b in (self._btn_load, self._btn_start, self._btn_pause, self._btn_reset):
            b.pack(side=tk.LEFT, padx=4)

        # Velocidad
        sep2 = tk.Frame(top, bg=COL_MUTED, width=1, height=30)
        sep2.pack(side=tk.LEFT, padx=10)

        tk.Label(top, text="Velocidad:", bg=BG_PANEL, fg=COL_TEXT,
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 4))

        self._speed_var = tk.IntVar(value=50)
        speed_scale = tk.Scale(top, variable=self._speed_var,
                               from_=1, to=100, orient=tk.HORIZONTAL,
                               bg=BG_PANEL, fg=COL_TEXT, troughcolor=BG_CARD,
                               highlightthickness=0, bd=0, showvalue=False,
                               length=130, cursor="hand2")
        speed_scale.pack(side=tk.LEFT, padx=4)

        tk.Label(top, textvariable=self._speed_var, width=3,
                 bg=BG_PANEL, fg=COL_MUTED, font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # ── Barra de estado ─────────────────────────────────────────
        status_row = tk.Frame(self.root, bg=BG_DARK)
        status_row.pack(fill=tk.X, padx=12, pady=(6, 0))

        self._status_var = tk.StringVar(value="Carga un array para comenzar.")
        tk.Label(status_row, textvariable=self._status_var,
                 bg=BG_DARK, fg=COL_MUTED, font=("Segoe UI", 9),
                 anchor="w").pack(side=tk.LEFT)

        self._step_var = tk.StringVar(value="")
        tk.Label(status_row, textvariable=self._step_var,
                 bg=BG_DARK, fg=COL_MUTED, font=("Segoe UI", 9),
                 anchor="e").pack(side=tk.RIGHT)

        # ── Canvas ──────────────────────────────────────────────────
        canvas_frame = tk.Frame(self.root, bg=BG_DARK)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_DARK,
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

        # ── Leyenda ─────────────────────────────────────────────────
        legend = tk.Frame(self.root, bg=BG_PANEL, pady=6)
        legend.pack(fill=tk.X)

        for color, label in [
            (COL_NORMAL, "Normal"),
            (COL_CMP,    "Comparando"),
            (COL_PIVOT,  "Activo / Pivote"),
            (COL_SORTED, "Ordenado"),
        ]:
            dot = tk.Canvas(legend, width=14, height=14,
                            bg=BG_PANEL, highlightthickness=0)
            dot.create_oval(2, 2, 12, 12, fill=color, outline="")
            dot.pack(side=tk.LEFT, padx=(12, 2))
            tk.Label(legend, text=label, bg=BG_PANEL, fg=COL_MUTED,
                     font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(0, 8))

    # ================================================================
    #  DIBUJO DE BARRAS
    # ================================================================
    def _draw(self, highlight: list[int] | None = None):
        """Redibuja el canvas completo. highlight = índices activos."""
        self.canvas.delete("all")

        if not self.array:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                text="← Carga un array para visualizar",
                fill=COL_MUTED, font=("Segoe UI", 13)
            )
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 50 or h < 50:
            return

        n = len(self.array)
        pad_x = 14
        pad_top = 16
        pad_bot = 34          # espacio para etiquetas numéricas
        usable_w = w - 2 * pad_x
        usable_h = h - pad_top - pad_bot

        bar_w    = usable_w / n
        gap      = max(1, bar_w * 0.10)          # 10 % de separación
        inner_w  = bar_w - gap

        hi_set   = set(highlight) if highlight else set()

        mn = min(self.array)
        mx = max(self.array)
        span = mx - mn or 1
        min_bar_h = max(4, usable_h * 0.03)      # barra mínima visible

        for i, val in enumerate(self.array):
            x0 = pad_x + i * bar_w + gap / 2
            x1 = x0 + inner_w

            norm     = (val - mn) / span
            bar_h    = min_bar_h + norm * (usable_h - min_bar_h)
            y0       = h - pad_bot - bar_h
            y1       = h - pad_bot

            # Color
            if i in self.sorted_indices:
                color = COL_SORTED
            elif len(hi_set) > 0 and i == max(hi_set):
                color = COL_PIVOT
            elif i in hi_set:
                color = COL_CMP
            else:
                color = COL_NORMAL

            # Barra redondeada (radio pequeño)
            r = min(4, inner_w / 2)
            self._rounded_rect(x0, y0, x1, y1, r, color)

            # Valor numérico debajo
            show_val = int(val) if val == int(val) else round(val, 1)
            font_size = max(6, min(10, int(inner_w * 0.55)))
            self.canvas.create_text(
                (x0 + x1) / 2, h - pad_bot + 14,
                text=str(show_val),
                fill=COL_MUTED,
                font=("Segoe UI", font_size)
            )

    def _rounded_rect(self, x0, y0, x1, y1, r, color):
        """Dibuja un rectángulo con esquinas superiores redondeadas."""
        c = self.canvas
        # Cuerpo
        c.create_rectangle(x0, y0 + r, x1, y1, fill=color, outline="")
        # Top sin esquinas
        c.create_rectangle(x0 + r, y0, x1 - r, y0 + r, fill=color, outline="")
        # Arcos superiores
        c.create_arc(x0, y0, x0 + 2*r, y0 + 2*r,
                     start=90, extent=90, fill=color, outline="")
        c.create_arc(x1 - 2*r, y0, x1, y0 + 2*r,
                     start=0, extent=90, fill=color, outline="")

    # ================================================================
    #  CARGA DE DATOS
    # ================================================================
    def _load_numbers(self):
        if self._running and not self._paused:
            self._stop_animation()

        dlg = LoadNumbersDialog(self.root)
        self.root.wait_window(dlg.top)

        if dlg.result:
            self._original = dlg.result[:]
            self.array     = dlg.result[:]
            self.sorted_indices.clear()
            self.highlight  = []
            self._steps     = 0
            self._status_var.set(f"Array cargado ({len(self.array)} elementos): {self.array}")
            self._step_var.set("")
            self._draw()

    # ================================================================
    #  CONTROL DE ANIMACIÓN
    # ================================================================
    def _start(self):
        if not self.array:
            messagebox.showwarning("Sin datos", "Carga un array primero.")
            return

        if self._paused:
            # Reanudar
            self._paused  = False
            self._running = True
            self._btn_pause.config(text="⏸ Pausa")
            self._status_var.set(f"{self._algo_name} — reanudado")
            self._tick()
            return

        if self._running:
            return

        # Inicio limpio
        name, gen_fn = ALGORITHMS[self._algo_var.get()]
        self._algo_name = self._algo_var.get()
        self._generator = gen_fn(self.array[:])
        self.sorted_indices.clear()
        self._steps   = 0
        self._running = True
        self._paused  = False
        self._btn_pause.config(text="⏸ Pausa")
        self._status_var.set(f"▶ {self._algo_name} ejecutándose…")
        self._tick()

    def _tick(self):
        """Un paso de la animación, programado con after()."""
        if not self._running or self._paused:
            return

        try:
            state, comparing, desc = next(self._generator)
        except StopIteration:
            self._on_finished()
            return

        self.array      = state
        self._steps    += 1
        self._draw(highlight=comparing)
        self._step_var.set(f"Paso {self._steps}  |  {desc}")

        # Delay: speed 1 → ~500 ms, speed 100 → ~5 ms
        delay = max(5, int(505 - self._speed_var.get() * 5))
        self._after_id = self.root.after(delay, self._tick)

    def _on_finished(self):
        self._running = False
        self._paused  = False
        self.sorted_indices = set(range(len(self.array)))
        self._draw()
        self._status_var.set(f"✅ {self._algo_name} completado  ·  {self._steps} pasos  ·  Resultado: {[int(x) if x==int(x) else x for x in self.array]}")
        self._step_var.set("")

    def _pause(self):
        if not self._running and not self._paused:
            return
        if self._paused:
            # Reanudar desde botón Pausa
            self._start()
        else:
            self._paused = True
            if self._after_id:
                self.root.after_cancel(self._after_id)
                self._after_id = None
            self._btn_pause.config(text="▶ Reanudar")
            self._status_var.set(f"⏸ {self._algo_name} pausado — paso {self._steps}")

    def _reset(self):
        self._stop_animation()
        if self._original:
            self.array = self._original[:]
        self.sorted_indices.clear()
        self.highlight  = []
        self._steps     = 0
        self._btn_pause.config(text="⏸ Pausa")
        self._status_var.set(f"↺ Array restaurado: {self.array}")
        self._step_var.set("")
        self._draw()

    def _stop_animation(self):
        self._running = False
        self._paused  = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self._generator = None


# ====================================================================
#  DIÁLOGO DE CARGA
# ====================================================================
class LoadNumbersDialog:
    def __init__(self, parent):
        self.result = None

        self.top = tk.Toplevel(parent)
        self.top.title("Cargar Array")
        self.top.geometry("420x380")
        self.top.configure(bg=BG_PANEL)
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        # ── Cantidad ──────────────────────────────────────────────
        tk.Label(self.top, text="Cantidad de elementos",
                 bg=BG_PANEL, fg=COL_TEXT,
                 font=("Segoe UI", 11, "bold")).pack(pady=(18, 4))

        self._cant_var = tk.IntVar(value=12)
        row_cant = tk.Frame(self.top, bg=BG_PANEL)
        row_cant.pack()

        for n in (5, 8, 12, 16, 20, 30):
            tk.Radiobutton(row_cant, text=str(n), variable=self._cant_var,
                           value=n, bg=BG_PANEL, fg=COL_TEXT,
                           selectcolor=BG_CARD, activebackground=BG_PANEL,
                           font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)

        ttk.Separator(self.top).pack(fill="x", padx=20, pady=14)

        # ── Entrada manual ────────────────────────────────────────
        tk.Label(self.top, text="Ingresa los números separados por comas:",
                 bg=BG_PANEL, fg=COL_TEXT, font=("Segoe UI", 10)).pack(pady=(0, 4))

        self._manual_entry = tk.Entry(self.top, width=38, bg=BG_CARD, fg=COL_TEXT,
                                      insertbackground=COL_TEXT, relief=tk.FLAT,
                                      font=("Consolas", 10))
        self._manual_entry.pack(ipady=5)
        self._manual_entry.insert(0, "Ej: 34, 7, 21, 55, 13")

        tk.Button(self.top, text="Usar entrada manual",
                  command=self._use_manual,
                  bg=BG_CARD, fg=COL_TEXT, relief=tk.FLAT,
                  font=("Segoe UI", 9, "bold"), padx=14, pady=6,
                  cursor="hand2").pack(pady=8)

        ttk.Separator(self.top).pack(fill="x", padx=20, pady=8)

        # ── Aleatorio ─────────────────────────────────────────────
        tk.Label(self.top, text="O genera números aleatorios",
                 bg=BG_PANEL, fg=COL_TEXT,
                 font=("Segoe UI", 10, "bold")).pack()

        row_range = tk.Frame(self.top, bg=BG_PANEL)
        row_range.pack(pady=8)

        tk.Label(row_range, text="Min:", bg=BG_PANEL,
                 fg=COL_MUTED, font=("Segoe UI", 9)).grid(row=0, column=0, padx=6)
        self._min_e = tk.Entry(row_range, width=7, bg=BG_CARD, fg=COL_TEXT,
                               insertbackground=COL_TEXT, relief=tk.FLAT)
        self._min_e.grid(row=0, column=1, padx=4)
        self._min_e.insert(0, "10")

        tk.Label(row_range, text="Max:", bg=BG_PANEL,
                 fg=COL_MUTED, font=("Segoe UI", 9)).grid(row=0, column=2, padx=6)
        self._max_e = tk.Entry(row_range, width=7, bg=BG_CARD, fg=COL_TEXT,
                               insertbackground=COL_TEXT, relief=tk.FLAT)
        self._max_e.grid(row=0, column=3, padx=4)
        self._max_e.insert(0, "99")

        tk.Button(self.top, text="🎲 Generar aleatoriamente",
                  command=self._use_random,
                  bg=COL_SORTED, fg="#0a2e26", relief=tk.FLAT,
                  font=("Segoe UI", 9, "bold"), padx=14, pady=6,
                  cursor="hand2").pack(pady=4)

        tk.Button(self.top, text="Cancelar",
                  command=self.top.destroy,
                  bg=BG_DARK, fg=COL_MUTED, relief=tk.FLAT,
                  font=("Segoe UI", 9), padx=14, pady=4,
                  cursor="hand2").pack(pady=(10, 0))

    def _use_manual(self):
        raw = self._manual_entry.get().strip()
        try:
            nums = [float(x.strip()) for x in raw.split(",") if x.strip()]
            if len(nums) < 2:
                raise ValueError
            self.result = nums
            self.top.destroy()
        except ValueError:
            messagebox.showerror("Error",
                "Ingresa al menos 2 números separados por comas.\nEj: 34, 7, 21, 55",
                parent=self.top)

    def _use_random(self):
        try:
            mn  = int(self._min_e.get())
            mx  = int(self._max_e.get())
            cnt = self._cant_var.get()
            if mn >= mx:
                raise ValueError("min debe ser < max")
            if cnt < 2:
                raise ValueError("mínimo 2 elementos")
            self.result = [random.randint(mn, mx) for _ in range(cnt)]
            self.top.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self.top)


# ====================================================================
#  ENTRY POINT
# ====================================================================
def main():
    root = tk.Tk()
    try:
        root.tk.call("tk", "scaling", 1.2)
    except Exception:
        pass
    app = SortingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
