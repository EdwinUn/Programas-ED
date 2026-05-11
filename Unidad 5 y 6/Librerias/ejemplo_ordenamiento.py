"""
Ejemplo interactivo y gráfico de ordenación interna y externa.

Permite al usuario:
  - Ingresar su propio arreglo, generar uno aleatorio o elegir un preset.
  - Seleccionar cualquier algoritmo de ordenación interna o externa.
  - Ver el resultado de la ordenación con barras coloreadas.
  - Ver métricas como tiempo y comparaciones.

Dependencias: tkinter (estándar), ordenamiento_interno.py, ordenamiento_externo.py
"""

from __future__ import annotations
import os
import sys
import random
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from ordenamiento_interno import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)
from ordenamiento_externo import external_merge_sort

# ---------------------------------------------------------------------------
# Wrappers para usar las librerías directamente
# ---------------------------------------------------------------------------

def bubble_sort_wrapper(data: list[int]) -> list[int]:
    resultado = bubble_sort(data)
    return resultado.arreglo

def insertion_sort_wrapper(data: list[int]) -> list[int]:
    resultado = insertion_sort(data)
    return resultado.arreglo

def selection_sort_wrapper(data: list[int]) -> list[int]:
    resultado = selection_sort(data)
    return resultado.arreglo

def merge_sort_wrapper(data: list[int]) -> list[int]:
    resultado = merge_sort(data)
    return resultado.arreglo

def quick_sort_wrapper(data: list[int]) -> list[int]:
    resultado = quick_sort(data)
    return resultado.arreglo

def heap_sort_wrapper(data: list[int]) -> list[int]:
    resultado = heap_sort(data)
    return resultado.arreglo

def external_merge_sort_wrapper(data: list[int]) -> list[int]:
    with tempfile.TemporaryDirectory(prefix="ext_demo_") as tmp:
        out = os.path.join(tmp, "result.txt")
        external_merge_sort(data, out, chunk_size=max(2, len(data) // 3))
        with open(out, "r", encoding="utf-8") as f:
            sorted_arr = [int(line.strip()) for line in f if line.strip()]
    return sorted_arr

ALGORITHMS = {
    "Bubble Sort":          bubble_sort_wrapper,
    "Insertion Sort":       insertion_sort_wrapper,
    "Selection Sort":       selection_sort_wrapper,
    "Merge Sort":           merge_sort_wrapper,
    "Quicksort":            quick_sort_wrapper,
    "Heapsort":             heap_sort_wrapper,
    "External Merge Sort":  external_merge_sort_wrapper,
}

PRESETS = {
    "Aleatorio (10)":    lambda: random.sample(range(1, 100), 10),
    "Aleatorio (20)":    lambda: random.sample(range(1, 100), 20),
    "Casi ordenado":     lambda: sorted(random.sample(range(1, 50), 12))[:-1] + [random.randint(1, 50)],
    "Orden inverso":     lambda: list(range(20, 0, -1)),
    "Con duplicados":    lambda: [random.choice([3, 7, 12, 18, 25, 31]) for _ in range(12)],
    "Ejemplo del libro": lambda: [15, 3, 9, 1, 18, 7, 12, 5],
}

# ---------------------------------------------------------------------------
# Paleta de colores para los estados
# ---------------------------------------------------------------------------
COLOR = {
    "default":  "#5B8FD6",
    "compare":  "#F5A623",
    "swap":     "#E74C3C",
    "pivot":    "#9B59B6",
    "merge":    "#2ECC71",
    "insert":   "#1ABC9C",
    "done":     "#27AE60",
}

LEGEND = [
    ("Normal",    "default"),
    ("Comparar",  "compare"),
    ("Swap",      "swap"),
    ("Pivote",    "pivot"),
    ("Fusión",    "merge"),
    ("Listo",     "done"),
]


# ---------------------------------------------------------------------------
# Aplicación principal
# ---------------------------------------------------------------------------

class SortingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Algoritmos de Ordenación")
        self.configure(bg="#1E1E2E")
        self.resizable(True, True)
        self.minsize(900, 600)

        self._data: list[int] = PRESETS["Ejemplo del libro"]()
        self._array_size = tk.IntVar(value=10)
        self._running = False

        self._build_ui()
        self._draw_bars(self._data, -1, -1, "default")

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        # ---- Panel izquierdo (controles) ----
        left = tk.Frame(self, bg="#2A2A3E", width=260)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        left.pack_propagate(False)

        tk.Label(left, text="⚙ Configuración", bg="#2A2A3E", fg="#CDD6F4",
                 font=("Segoe UI", 13, "bold")).pack(pady=(18, 6))

        # Algoritmo
        self._build_section(left, "Algoritmo")
        self._algo_var = tk.StringVar(value="Bubble Sort")
        algo_menu = ttk.Combobox(left, textvariable=self._algo_var,
                                 values=list(ALGORITHMS.keys()),
                                 state="readonly", width=24)
        algo_menu.pack(padx=14, pady=4)

        # Preset
        self._build_section(left, "Preset de datos")
        self._preset_var = tk.StringVar(value="Ejemplo del libro")
        preset_menu = ttk.Combobox(left, textvariable=self._preset_var,
                                   values=list(PRESETS.keys()),
                                   state="readonly", width=24)
        preset_menu.pack(padx=14, pady=4)
        tk.Button(left, text="Cargar preset", command=self._load_preset,
                  bg="#6C6F93", fg="white", relief=tk.FLAT,
                  font=("Segoe UI", 9), cursor="hand2").pack(padx=14, pady=2, fill=tk.X)

        # Tamaño del arreglo
        self._build_section(left, "Tamaño del arreglo")
        size_frame = tk.Frame(left, bg="#2A2A3E")
        size_frame.pack(padx=14, pady=4, fill=tk.X)
        tk.Label(size_frame, text="Elementos:", bg="#2A2A3E", fg="#BAC2DE",
                 font=("Segoe UI", 8)).pack(side=tk.LEFT)
        vcmd = (self.register(self._validate_array_size), "%P")
        tk.Spinbox(size_frame, from_=5, to=100, textvariable=self._array_size,
                   validate="key", validatecommand=vcmd,
                   width=6, bg="#313244", fg="#CDD6F4", insertbackground="white",
                   relief=tk.FLAT, font=("Consolas", 10), justify=tk.CENTER).pack(side=tk.LEFT, padx=(8, 6))
        tk.Button(size_frame, text="Generar aleatorio", command=self._generate_random,
                  bg="#6C6F93", fg="white", relief=tk.FLAT,
                  font=("Segoe UI", 9), cursor="hand2").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Input manual
        self._build_section(left, "Arreglo personalizado")
        tk.Label(left, text="Números separados por comas:",
                 bg="#2A2A3E", fg="#BAC2DE", font=("Segoe UI", 8)).pack(padx=14, anchor=tk.W)
        self._custom_entry = tk.Entry(left, width=26, bg="#313244", fg="#CDD6F4",
                                      insertbackground="white", relief=tk.FLAT,
                                      font=("Consolas", 10))
        self._custom_entry.pack(padx=14, pady=4)
        self._custom_entry.insert(0, ", ".join(map(str, self._data)))
        tk.Button(left, text="Usar este arreglo", command=self._load_custom,
                  bg="#6C6F93", fg="white", relief=tk.FLAT,
                  font=("Segoe UI", 9), cursor="hand2").pack(padx=14, pady=2, fill=tk.X)

        # Controles
        self._build_section(left, "Controles")
        btn_frame = tk.Frame(left, bg="#2A2A3E")
        btn_frame.pack(padx=14, fill=tk.X)

        self._btn_start = tk.Button(btn_frame, text="▶ Ordenar", command=self._start,
                                    bg="#89B4FA", fg="#1E1E2E", relief=tk.FLAT,
                                    font=("Segoe UI", 10, "bold"), cursor="hand2")
        self._btn_start.pack(fill=tk.X, pady=3)

        self._btn_reset = tk.Button(btn_frame, text="↺ Reiniciar", command=self._reset,
                                    bg="#F38BA8", fg="#1E1E2E", relief=tk.FLAT,
                                    font=("Segoe UI", 10, "bold"), cursor="hand2")
        self._btn_reset.pack(fill=tk.X, pady=3)

        # Estado
        self._build_section(left, "Estado")
        self._lbl_status = tk.Label(left, text="Estado: listo", bg="#2A2A3E",
                                    fg="#CBA6F7", font=("Consolas", 9),
                                    wraplength=220, justify=tk.LEFT)
        self._lbl_status.pack(anchor=tk.W, padx=16, pady=(2, 10))

        # ---- Panel derecho (canvas + log) ----
        right = tk.Frame(self, bg="#1E1E2E")
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas
        self._canvas = tk.Canvas(right, bg="#181825", highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 4))

        # Log
        log_frame = tk.Frame(right, bg="#1E1E2E")
        log_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(log_frame, text="Arreglo actual:", bg="#1E1E2E",
                 fg="#6C7086", font=("Segoe UI", 8)).pack(anchor=tk.W)
        self._lbl_array = tk.Label(log_frame, text="", bg="#1E1E2E",
                                   fg="#CDD6F4", font=("Consolas", 9),
                                   wraplength=700, justify=tk.LEFT)
        self._lbl_array.pack(anchor=tk.W)

    def _build_section(self, parent, title: str):
        tk.Label(parent, text=title.upper(), bg="#2A2A3E", fg="#6C7086",
                 font=("Segoe UI", 7, "bold")).pack(anchor=tk.W, padx=14, pady=(10, 1))

    # ------------------------------------------------------------------
    # Lógica de datos
    # ------------------------------------------------------------------

    def _load_preset(self):
        self._reset()
        self._data = PRESETS[self._preset_var.get()]()
        self._custom_entry.delete(0, tk.END)
        self._custom_entry.insert(0, ", ".join(map(str, self._data)))
        self._draw_bars(self._data, -1, -1, "default")

    def _validate_array_size(self, value: str) -> bool:
        if value == "":
            return True
        try:
            size = int(value)
        except ValueError:
            return False
        return 5 <= size <= 100

    def _generate_random(self):
        self._reset()
        size = self._array_size.get()
        if size < 5 or size > 100:
            messagebox.showerror("Error", "El tamaño debe estar entre 5 y 100 elementos.")
            return
        self._data = random.sample(list(range(1, size * 5 + 1)), size)
        self._custom_entry.delete(0, tk.END)
        self._custom_entry.insert(0, ", ".join(map(str, self._data)))
        self._draw_bars(self._data, -1, -1, "default")

    def _load_custom(self):
        raw = self._custom_entry.get()
        try:
            nums = [int(x.strip()) for x in raw.split(",") if x.strip()]
            if not nums:
                raise ValueError
            if len(nums) > 100:
                messagebox.showerror("Error",
                                     "No se permite más de 100 elementos en el arreglo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingresa números enteros separados por comas.")
            return
        self._reset()
        self._data = nums
        self._draw_bars(self._data, -1, -1, "default")



    def _draw_bars(self, arr: list[int], idx_a: int, idx_b: int, action: str):
        self._canvas.update_idletasks()
        W = self._canvas.winfo_width() or 700
        H = self._canvas.winfo_height() or 400
        self._canvas.delete("all")

        if not arr:
            return

        n = len(arr)
        max_val = max(arr) or 1
        pad_x, pad_top, pad_bot = 20, 20, 30
        avail_w = W - 2 * pad_x
        avail_h = H - pad_top - pad_bot
        bar_w = max(2, avail_w / n - 2)
        gap = avail_w / n

        for i, val in enumerate(arr):
            x0 = pad_x + i * gap
            bar_h = (val / max_val) * avail_h
            y0 = pad_top + avail_h - bar_h
            x1 = x0 + bar_w
            y1 = pad_top + avail_h

            if action == "done" or (i != idx_a and i != idx_b):
                if action == "done":
                    color = COLOR["done"]
                else:
                    color = COLOR["default"]
            elif i == idx_a or i == idx_b:
                color = COLOR.get(action, COLOR["compare"])
            else:
                color = COLOR["default"]

            self._canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # Etiqueta numérica (solo si hay espacio)
            if bar_w >= 14:
                self._canvas.create_text(
                    (x0 + x1) / 2, y1 + 12,
                    text=str(val), fill="#CDD6F4", font=("Consolas", 8)
                )

        # Índices destacados
        if idx_a >= 0 and bar_w >= 10:
            xa = pad_x + idx_a * gap + bar_w / 2
            self._canvas.create_text(xa, pad_top - 8, text="▼",
                                     fill=COLOR.get(action, "#F5A623"), font=("Segoe UI", 10))
        if idx_b >= 0 and idx_b != idx_a and bar_w >= 10:
            xb = pad_x + idx_b * gap + bar_w / 2
            self._canvas.create_text(xb, pad_top - 8, text="▼",
                                     fill=COLOR.get(action, "#F5A623"), font=("Segoe UI", 10))

        self._lbl_array.config(text="[ " + ", ".join(map(str, arr)) + " ]")

    # ------------------------------------------------------------------
    # Control de animación
    # ------------------------------------------------------------------

    def _start(self):
        if self._running:
            return
        algo_fn = ALGORITHMS[self._algo_var.get()]
        self._lbl_status.config(text=f"Ordenando con {self._algo_var.get()}...")
        self._running = True
        self._btn_start.config(state=tk.DISABLED)
        # Ejecutar el algoritmo directamente
        sorted_data = algo_fn(self._data[:])
        self._data = sorted_data
        self._draw_bars(self._data, -1, -1, "done")
        self._lbl_status.config(text=f"✓ Ordenado con {self._algo_var.get()}")
        self._running = False
        self._btn_start.config(state=tk.DISABLED)

    def _pause(self):
        # No hay pausa en ejecución directa
        pass

    def _reset(self):
        self._running = False
        self._btn_start.config(state=tk.NORMAL, text="▶ Ordenar")
        self._lbl_status.config(text="Estado: listo")
        self._draw_bars(self._data, -1, -1, "default")




# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = SortingApp()
    app.mainloop()