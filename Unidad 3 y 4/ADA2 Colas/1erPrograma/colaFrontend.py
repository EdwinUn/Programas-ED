"""
Utilizando la clase Cola, escriba una función llamada que reciba 2 Colas con números  
enteros y devuelva una nueva Cola con sus elementos sumados uno a uno.  
"""

# ── frontend/cola_frontend.py ────────────────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Importar el backend
sys.path.insert(0, os.path.dirname(__file__))
from colaBackend import Cola, sumar_colas


# ── Paleta de colores ────────────────────────────────────────────
BG        = "#1e1e2e"
PANEL     = "#2a2a3e"
ACCENT    = "#7c6af7"
ACCENT2   = "#f7766a"
SUCCESS   = "#50fa7b"
TEXT      = "#cdd6f4"
SUBTEXT   = "#6c7086"
WHITE     = "#ffffff"
ENTRY_BG  = "#313244"
FONT_TITLE = ("Consolas", 18, "bold")
FONT_LABEL = ("Consolas", 10, "bold")
FONT_MONO  = ("Consolas", 11)
FONT_SMALL = ("Consolas", 9)


class AppCola(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Suma de Colas")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.cola_a = Cola()
        self.cola_b = Cola()

        self._build_ui()

    # ── Construcción de la UI ────────────────────────────────────
    def _build_ui(self):
        # Título
        tk.Label(self, text="⬡  SUMA DE COLAS  ⬡", font=FONT_TITLE,
                 bg=BG, fg=ACCENT).pack(pady=(18, 4))
        tk.Label(self, text="Ingresa valores enteros en cada cola y súmalas",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(pady=(0, 14))

        # Contenedor principal (3 columnas)
        frame_main = tk.Frame(self, bg=BG)
        frame_main.pack(padx=20, pady=4)

        self._panel_cola(frame_main, "Cola A", ACCENT,  col=0,
                         get_cola=lambda: self.cola_a,
                         set_cola=lambda c: setattr(self, "cola_a", c),
                         lv_attr="lv_a")

        # Botón central
        frame_center = tk.Frame(frame_main, bg=BG)
        frame_center.grid(row=0, column=1, padx=14, pady=4)
        tk.Label(frame_center, text="", bg=BG).pack(expand=True)
        tk.Button(frame_center, text="SUMAR\n  ▶▶  ",
                  font=("Consolas", 10, "bold"),
                  bg=SUCCESS, fg="#1e1e2e", relief="flat",
                  padx=10, pady=8, cursor="hand2",
                  command=self._sumar).pack(pady=6)
        tk.Button(frame_center, text="LIMPIAR\n  ✕  ",
                  font=("Consolas", 9, "bold"),
                  bg=ACCENT2, fg=WHITE, relief="flat",
                  padx=10, pady=6, cursor="hand2",
                  command=self._limpiar).pack(pady=4)

        self._panel_cola(frame_main, "Cola B", "#f79d6a", col=2,
                         get_cola=lambda: self.cola_b,
                         set_cola=lambda c: setattr(self, "cola_b", c),
                         lv_attr="lv_b")

        # Panel resultado
        self._panel_resultado()

        # Status bar
        self.status_var = tk.StringVar(value="Listo.")
        tk.Label(self, textvariable=self.status_var, font=FONT_SMALL,
                 bg=BG, fg=SUBTEXT, anchor="w").pack(
                     fill="x", padx=20, pady=(6, 10))

    def _panel_cola(self, parent, titulo, color, col,
                    get_cola, set_cola, lv_attr):
        frame = tk.Frame(parent, bg=PANEL, bd=0, relief="flat")
        frame.grid(row=0, column=col, padx=6, pady=4, sticky="n")

        # Encabezado
        tk.Label(frame, text=titulo, font=FONT_LABEL,
                 bg=color, fg="#1e1e2e", padx=12, pady=6,
                 width=18).pack(fill="x")

        # Entry + botón encolar
        row_entry = tk.Frame(frame, bg=PANEL)
        row_entry.pack(padx=10, pady=(10, 4))

        entry = tk.Entry(row_entry, font=FONT_MONO, bg=ENTRY_BG,
                         fg=WHITE, insertbackground=WHITE,
                         relief="flat", width=10, justify="center")
        entry.pack(side="left", ipady=4, padx=(0, 6))

        def encolar(e=None):
            val = entry.get().strip()
            try:
                get_cola().encolar(int(val))
                entry.delete(0, "end")
                self._refresh_listbox(get_cola(), lv_attr)
                self._set_status(f"Encolado {val} en {titulo}.")
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número entero válido.")

        entry.bind("<Return>", encolar)
        tk.Button(row_entry, text="+ Encolar", font=FONT_SMALL,
                  bg=color, fg="#1e1e2e", relief="flat",
                  padx=6, pady=4, cursor="hand2",
                  command=encolar).pack(side="left")

        # Botón desencolar
        def desencolar():
            try:
                val = get_cola().desencolar()
                self._refresh_listbox(get_cola(), lv_attr)
                self._set_status(f"Desencolado {val} de {titulo}.")
            except IndexError as ex:
                messagebox.showwarning("Cola vacía", str(ex))

        tk.Button(frame, text="⬅ Desencolar", font=FONT_SMALL,
                  bg=ENTRY_BG, fg=TEXT, relief="flat",
                  padx=6, pady=3, cursor="hand2",
                  command=desencolar).pack(pady=(0, 6))

        # Listbox con scrollbar
        frame_lv = tk.Frame(frame, bg=PANEL)
        frame_lv.pack(padx=10, pady=(0, 10))

        sb = tk.Scrollbar(frame_lv, orient="vertical")
        lv = tk.Listbox(frame_lv, font=FONT_MONO, bg=ENTRY_BG, fg=color,
                        selectbackground=color, selectforeground="#1e1e2e",
                        relief="flat", width=16, height=8,
                        yscrollcommand=sb.set, bd=0)
        sb.config(command=lv.yview)
        lv.pack(side="left")
        sb.pack(side="left", fill="y")

        setattr(self, lv_attr, lv)

    def _panel_resultado(self):
        frame = tk.Frame(self, bg=PANEL)
        frame.pack(fill="x", padx=20, pady=(4, 0))

        tk.Label(frame, text="  Cola Resultado", font=FONT_LABEL,
                 bg=SUCCESS, fg="#1e1e2e", padx=10, pady=5,
                 anchor="w").pack(fill="x")

        self.lv_res = tk.Listbox(frame, font=FONT_MONO, bg=ENTRY_BG,
                                  fg=SUCCESS, relief="flat",
                                  height=3, bd=0)
        self.lv_res.pack(fill="x", padx=10, pady=8)

    # ── Lógica de la UI ─────────────────────────────────────────
    def _refresh_listbox(self, cola, attr):
        lv = getattr(self, attr)
        lv.delete(0, "end")
        for i, v in enumerate(cola.como_lista()):
            prefix = "▶ " if i == 0 else "  "
            lv.insert("end", f"{prefix}{v}")

    def _sumar(self):
        try:
            resultado = sumar_colas(self.cola_a, self.cola_b)
            self.lv_res.delete(0, "end")
            for i, v in enumerate(resultado.como_lista()):
                prefix = "▶ " if i == 0 else "  "
                self.lv_res.insert("end", f"{prefix}{v}")
            self._set_status(
                f"✓ Suma completada — {resultado.tamanio()} elementos.")
        except ValueError as ex:
            messagebox.showerror("Error de tamaño", str(ex))

    def _limpiar(self):
        self.cola_a = Cola()
        self.cola_b = Cola()
        for attr in ("lv_a", "lv_b", "lv_res"):
            getattr(self, attr).delete(0, "end")
        self._set_status("Colas limpiadas.")

    def _set_status(self, msg):
        self.status_var.set(msg)


if __name__ == "__main__":
    app = AppCola()
    app.mainloop()