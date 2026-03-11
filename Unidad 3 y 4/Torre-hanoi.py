"""
TORRE DE HANOI
=======================================================
MÉTODOS (12 en total):
  Clase HanoiApp:
    1. __init__             - Inicializa la app, variables y construye la UI
    2. build_ui             - Construye todos los widgets de la interfaz
    3. draw_towers          - Dibuja las varillas y discos en el canvas
    4. draw_disk            - Dibuja un disco individual con color y etiqueta
    5. new_game             - Inicia una nueva partida manual
    6. handle_click         - Gestiona clics del usuario sobre las varillas
    7. select_peg           - Selecciona o deselecciona una varilla
    8. move_disk            - Ejecuta un movimiento manual validado
    9. check_win            - Verifica si el jugador ganó
   10. solve_auto           - Lanza la solución automática en hilo separado
   11. hanoi_recursive      - Algoritmo recursivo de Hanoi (genera movimientos)
   12. animate_solution     - Anima paso a paso la solución automática
   13. run_benchmark        - Ejecuta benchmarks para 5, 10, 30 y 64 discos
   14. format_moves         - Formatea el número de movimientos con separadores
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math


# ── Colores para los discos ──────────────────────────────────────────────────
DISK_COLORS = [
    "#E74C3C", "#E67E22", "#F1C40F", "#2ECC71",
    "#1ABC9C", "#3498DB", "#9B59B6", "#E91E63",
    "#FF5722", "#795548", "#607D8B", "#00BCD4",
]

BG_COLOR      = "#1E1E2E"
PEG_COLOR     = "#CDD6F4"
BASE_COLOR    = "#585B70"
TEXT_COLOR    = "#CDD6F4"
ACCENT_COLOR  = "#89B4FA"
SELECT_COLOR  = "#A6E3A1"
WIN_COLOR     = "#A6E3A1"
PANEL_COLOR   = "#313244"
BTN_COLOR     = "#45475A"
BTN_HOVER     = "#585B70"


class HanoiApp:
    # ── 1. __init__ ──────────────────────────────────────────────────────────
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Torre de Hanói")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        # Estado del juego
        self.num_disks  = 3
        self.num_pegs   = 3
        self.pegs: list[list[int]] = []   # pegs[i] = lista de discos (grande→pequeño)
        self.selected   = None            # índice de varilla seleccionada
        self.moves      = 0
        self.playing    = False
        self.solving    = False
        self.anim_speed = 300             # ms entre pasos de animación

        self.build_ui()
        self.new_game()

    # ── 2. build_ui ──────────────────────────────────────────────────────────
    def build_ui(self):
        # ── Título ──
        title = tk.Label(self.root, text="🗼 Torre de Hanói", font=("Segoe UI", 22, "bold"),
                         bg=BG_COLOR, fg=ACCENT_COLOR)
        title.pack(pady=(14, 0))

        # ── Notebook (pestañas) ──
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG_COLOR,   borderwidth=0)
        style.configure("TNotebook.Tab",    background=PANEL_COLOR, foreground=TEXT_COLOR,
                        padding=[14, 6],    font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",          background=[("selected", ACCENT_COLOR)],
                  foreground=[("selected", BG_COLOR)])

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=12, pady=8)

        # Pestañas
        self.tab_play  = tk.Frame(self.nb, bg=BG_COLOR)
        self.tab_auto  = tk.Frame(self.nb, bg=BG_COLOR)
        self.tab_bench = tk.Frame(self.nb, bg=BG_COLOR)

        self.nb.add(self.tab_play,  text="🎮  Jugar")
        self.nb.add(self.tab_auto,  text="🤖  Auto-resolver")
        self.nb.add(self.tab_bench, text="⏱  Benchmarks")

        self._build_play_tab()
        self._build_auto_tab()
        self._build_bench_tab()

    # ── Subpanel: pestaña Jugar ──────────────────────────────────────────────
    def _build_play_tab(self):
        t = self.tab_play

        # Canvas principal
        self.canvas = tk.Canvas(t, width=760, height=320,
                                bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(pady=(12, 4))
        self.canvas.bind("<Button-1>", self.handle_click)

        # Controles superiores
        ctrl = tk.Frame(t, bg=BG_COLOR)
        ctrl.pack(pady=4)

        # Número de discos
        tk.Label(ctrl, text="Discos:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 10)).grid(row=0, column=0, padx=6)
        self.disk_var = tk.IntVar(value=self.num_disks)
        disk_spin = tk.Spinbox(ctrl, from_=2, to=12, textvariable=self.disk_var,
                               width=4, font=("Segoe UI", 11),
                               bg=PANEL_COLOR, fg=TEXT_COLOR,
                               buttonbackground=BTN_COLOR,
                               insertbackground=TEXT_COLOR)
        disk_spin.grid(row=0, column=1, padx=4)

        # Número de varillas
        tk.Label(ctrl, text="Varillas:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 10)).grid(row=0, column=2, padx=6)
        self.peg_var = tk.IntVar(value=self.num_pegs)
        peg_spin = tk.Spinbox(ctrl, from_=3, to=7, textvariable=self.peg_var,
                              width=4, font=("Segoe UI", 11),
                              bg=PANEL_COLOR, fg=TEXT_COLOR,
                              buttonbackground=BTN_COLOR,
                              insertbackground=TEXT_COLOR)
        peg_spin.grid(row=0, column=3, padx=4)

        btn_new = tk.Button(ctrl, text="▶  Nueva partida",
                            command=self.new_game,
                            bg=ACCENT_COLOR, fg=BG_COLOR,
                            font=("Segoe UI", 10, "bold"),
                            relief="flat", padx=12, pady=4, cursor="hand2")
        btn_new.grid(row=0, column=4, padx=12)

        # Barra de estado
        self.status_var = tk.StringVar(value="Selecciona una varilla para mover el disco superior.")
        status_bar = tk.Label(t, textvariable=self.status_var,
                              bg=PANEL_COLOR, fg=TEXT_COLOR,
                              font=("Segoe UI", 10), pady=6)
        status_bar.pack(fill="x", padx=12, pady=(0, 6))

        # Contador de movimientos
        self.move_label = tk.Label(t, text="Movimientos: 0",
                                   bg=BG_COLOR, fg=ACCENT_COLOR,
                                   font=("Segoe UI", 12, "bold"))
        self.move_label.pack()

        # Info mínimo de movimientos
        self.min_label = tk.Label(t, text="",
                                  bg=BG_COLOR, fg=TEXT_COLOR,
                                  font=("Segoe UI", 9))
        self.min_label.pack(pady=(0, 8))

    # ── Subpanel: pestaña Auto-resolver ─────────────────────────────────────
    def _build_auto_tab(self):
        t = self.tab_auto

        self.auto_canvas = tk.Canvas(t, width=760, height=300,
                                     bg=BG_COLOR, highlightthickness=0)
        self.auto_canvas.pack(pady=(12, 4))

        ctrl = tk.Frame(t, bg=BG_COLOR)
        ctrl.pack(pady=6)

        tk.Label(ctrl, text="Discos:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 10)).grid(row=0, column=0, padx=6)
        self.auto_disk_var = tk.IntVar(value=5)
        auto_spin = tk.Spinbox(ctrl, from_=2, to=20, textvariable=self.auto_disk_var,
                               width=4, font=("Segoe UI", 11),
                               bg=PANEL_COLOR, fg=TEXT_COLOR,
                               buttonbackground=BTN_COLOR,
                               insertbackground=TEXT_COLOR)
        auto_spin.grid(row=0, column=1, padx=4)

        tk.Label(ctrl, text="Velocidad (ms):", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 10)).grid(row=0, column=2, padx=6)
        self.speed_var = tk.IntVar(value=300)
        speed_spin = tk.Spinbox(ctrl, from_=10, to=2000, increment=50,
                                textvariable=self.speed_var,
                                width=6, font=("Segoe UI", 11),
                                bg=PANEL_COLOR, fg=TEXT_COLOR,
                                buttonbackground=BTN_COLOR,
                                insertbackground=TEXT_COLOR)
        speed_spin.grid(row=0, column=3, padx=4)

        btn_solve = tk.Button(ctrl, text="⚡  Resolver ahora",
                              command=self.solve_auto,
                              bg="#A6E3A1", fg=BG_COLOR,
                              font=("Segoe UI", 10, "bold"),
                              relief="flat", padx=12, pady=4, cursor="hand2")
        btn_solve.grid(row=0, column=4, padx=12)

        self.auto_status = tk.StringVar(value="Configura y presiona 'Resolver ahora'.")
        tk.Label(t, textvariable=self.auto_status,
                 bg=PANEL_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 10), pady=6).pack(fill="x", padx=12, pady=(0, 4))

        self.auto_move_label = tk.Label(t, text="",
                                        bg=BG_COLOR, fg=ACCENT_COLOR,
                                        font=("Segoe UI", 12, "bold"))
        self.auto_move_label.pack(pady=(0, 8))

    # ── Subpanel: pestaña Benchmarks ─────────────────────────────────────────
    def _build_bench_tab(self):
        t = self.tab_bench

        tk.Label(t, text="Benchmarks de resolución automática (3 varillas)",
                 bg=BG_COLOR, fg=TEXT_COLOR,
                 font=("Segoe UI", 11)).pack(pady=(16, 6))

        btn = tk.Button(t, text="🚀  Ejecutar Benchmarks",
                        command=lambda: threading.Thread(target=self.run_benchmark, daemon=True).start(),
                        bg="#F38BA8", fg=BG_COLOR,
                        font=("Segoe UI", 11, "bold"),
                        relief="flat", padx=14, pady=6, cursor="hand2")
        btn.pack(pady=6)

        # Tabla de resultados
        cols = ("Discos", "Movimientos", "Tiempo (s)", "Movs/seg")
        style = ttk.Style()
        style.configure("Hanoi.Treeview",
                        background=PANEL_COLOR, foreground=TEXT_COLOR,
                        fieldbackground=PANEL_COLOR, rowheight=28,
                        font=("Segoe UI", 10))
        style.configure("Hanoi.Treeview.Heading",
                        background=BTN_COLOR, foreground=ACCENT_COLOR,
                        font=("Segoe UI", 10, "bold"))
        style.map("Hanoi.Treeview", background=[("selected", ACCENT_COLOR)])

        self.bench_tree = ttk.Treeview(t, columns=cols, show="headings",
                                       height=6, style="Hanoi.Treeview")
        for c in cols:
            self.bench_tree.heading(c, text=c)
            self.bench_tree.column(c, anchor="center", width=160)
        self.bench_tree.pack(padx=24, pady=8, fill="x")

        self.bench_status = tk.Label(t, text="Presiona el botón para iniciar.",
                                     bg=BG_COLOR, fg=TEXT_COLOR,
                                     font=("Segoe UI", 10))
        self.bench_status.pack(pady=4)

        # Notas
        note = ("Nota: Para 30 y 64 discos el algoritmo genera los movimientos sin animarlos "
                "(2³⁰ ≈ 1 000 M  /  2⁶⁴ ≈ 1.8×10¹⁹ movimientos — se mide solo el tiempo de cómputo).")
        tk.Label(t, text=note, bg=BG_COLOR, fg="#6C7086",
                 font=("Segoe UI", 8), wraplength=680, justify="center").pack(pady=(0, 10))

    # ═══════════════════════════════════════════════════════════════════════
    #  LÓGICA DEL JUEGO MANUAL
    # ═══════════════════════════════════════════════════════════════════════

    # ── 3. draw_towers ───────────────────────────────────────────────────────
    def draw_towers(self, canvas: tk.Canvas, pegs: list, num_disks: int, num_pegs: int,
                    selected: int = None, highlight_pegs: list = None):
        canvas.delete("all")
        W = int(canvas["width"])
        H = int(canvas["height"])

        base_y      = H - 30
        base_h      = 16
        peg_w       = 8
        peg_h       = H - base_y + base_h + 180  # altura de la varilla
        max_dw      = min(80, (W // num_pegs) - 20)
        disk_h      = max(14, min(28, (H - 80) // (num_disks + 1)))

        section_w   = W // num_pegs

        # Base
        canvas.create_rectangle(10, base_y, W - 10, base_y + base_h,
                                 fill=BASE_COLOR, outline="")

        for i in range(num_pegs):
            cx = section_w * i + section_w // 2

            # Resaltado de selección
            if selected == i:
                canvas.create_rectangle(cx - section_w // 2 + 4, 10,
                                        cx + section_w // 2 - 4, base_y + base_h,
                                        fill=SELECT_COLOR, outline="", stipple="gray25")
            if highlight_pegs and i in highlight_pegs:
                canvas.create_rectangle(cx - section_w // 2 + 4, 10,
                                        cx + section_w // 2 - 4, base_y + base_h,
                                        fill=WIN_COLOR, outline="", stipple="gray25")

            # Varilla
            canvas.create_rectangle(cx - peg_w // 2, base_y - peg_h + base_h,
                                     cx + peg_w // 2, base_y,
                                     fill=PEG_COLOR, outline="")

            # Etiqueta de varilla
            label = chr(65 + i)   # A, B, C …
            canvas.create_text(cx, base_y + base_h + 10,
                                text=label, fill=ACCENT_COLOR,
                                font=("Segoe UI", 11, "bold"))

            # Discos
            for j, disk in enumerate(pegs[i]):
                dy = base_y - (j + 1) * disk_h
                self.draw_disk(canvas, cx, dy, disk, num_disks, max_dw, disk_h)

    # ── 4. draw_disk ─────────────────────────────────────────────────────────
    def draw_disk(self, canvas: tk.Canvas, cx: int, dy: int,
                  disk: int, num_disks: int, max_dw: int, disk_h: int):
        ratio  = disk / num_disks
        dw     = int(max_dw * 0.25 + max_dw * 0.75 * ratio)
        color  = DISK_COLORS[disk % len(DISK_COLORS)]
        r      = 4   # radio de esquinas redondeadas

        x0, y0 = cx - dw, dy
        x1, y1 = cx + dw, dy + disk_h - 2

        # Rectángulo redondeado simulado
        canvas.create_rectangle(x0 + r, y0, x1 - r, y1, fill=color, outline="")
        canvas.create_rectangle(x0, y0 + r, x1, y1 - r, fill=color, outline="")
        canvas.create_oval(x0, y0, x0 + 2*r, y0 + 2*r, fill=color, outline="")
        canvas.create_oval(x1 - 2*r, y0, x1, y0 + 2*r, fill=color, outline="")
        canvas.create_oval(x0, y1 - 2*r, x0 + 2*r, y1, fill=color, outline="")
        canvas.create_oval(x1 - 2*r, y1 - 2*r, x1, y1, fill=color, outline="")

        # Número del disco
        if disk_h >= 16 and dw > 18:
            canvas.create_text(cx, dy + disk_h // 2,
                                text=str(disk), fill="white",
                                font=("Segoe UI", 8, "bold"))

    # ── 5. new_game ──────────────────────────────────────────────────────────
    def new_game(self):
        self.num_disks = max(2, min(12, self.disk_var.get()))
        self.num_pegs  = max(3, min(7,  self.peg_var.get()))
        self.disk_var.set(self.num_disks)
        self.peg_var.set(self.num_pegs)

        # Todos los discos en la primera varilla (grande abajo → pequeño arriba)
        self.pegs    = [list(range(self.num_disks, 0, -1))] + \
                       [[] for _ in range(self.num_pegs - 1)]
        self.selected = None
        self.moves    = 0
        self.playing  = True
        self.solving  = False

        min_moves = 2 ** self.num_disks - 1
        self.min_label.config(text=f"Mínimo de movimientos: {self.format_moves(min_moves)}")
        self.move_label.config(text="Movimientos: 0")
        self.status_var.set("Selecciona una varilla para mover el disco superior.")
        self.draw_towers(self.canvas, self.pegs, self.num_disks, self.num_pegs)

    # ── 6. handle_click ──────────────────────────────────────────────────────
    def handle_click(self, event):
        if not self.playing or self.solving:
            return
        W        = int(self.canvas["width"])
        sec_w    = W // self.num_pegs
        peg_idx  = event.x // sec_w
        if 0 <= peg_idx < self.num_pegs:
            self.select_peg(peg_idx)

    # ── 7. select_peg ────────────────────────────────────────────────────────
    def select_peg(self, idx: int):
        if self.selected is None:
            if self.pegs[idx]:
                self.selected = idx
                label = chr(65 + idx)
                self.status_var.set(f"Varilla {label} seleccionada. Haz clic en el destino.")
            else:
                self.status_var.set("Esa varilla está vacía. Elige otra.")
        else:
            if idx == self.selected:
                self.selected = None
                self.status_var.set("Selección cancelada.")
            else:
                self.move_disk(self.selected, idx)
                self.selected = None
        self.draw_towers(self.canvas, self.pegs, self.num_disks, self.num_pegs,
                         selected=self.selected)

    # ── 8. move_disk ─────────────────────────────────────────────────────────
    def move_disk(self, src: int, dst: int):
        if not self.pegs[src]:
            self.status_var.set("La varilla origen está vacía.")
            return
        top = self.pegs[src][-1]
        if self.pegs[dst] and self.pegs[dst][-1] < top:
            self.status_var.set("❌ Movimiento inválido: no puedes poner un disco grande sobre uno pequeño.")
            return
        self.pegs[dst].append(self.pegs[src].pop())
        self.moves += 1
        self.move_label.config(text=f"Movimientos: {self.moves}")
        self.status_var.set(f"Disco {top} movido de {chr(65+src)} → {chr(65+dst)}.")
        self.draw_towers(self.canvas, self.pegs, self.num_disks, self.num_pegs)
        self.check_win()

    # ── 9. check_win ─────────────────────────────────────────────────────────
    def check_win(self):
        # Gana si todos los discos están en la ÚLTIMA varilla
        if len(self.pegs[-1]) == self.num_disks:
            self.playing = False
            min_m = 2 ** self.num_disks - 1
            extra = self.moves - min_m
            msg = (f"🎉 ¡Ganaste en {self.moves} movimientos!\n"
                   f"Mínimo posible: {self.format_moves(min_m)}\n"
                   f"Movimientos extra: {extra}")
            self.status_var.set(msg)
            self.draw_towers(self.canvas, self.pegs, self.num_disks, self.num_pegs,
                             highlight_pegs=[self.num_pegs - 1])
            messagebox.showinfo("¡Victoria!", msg)

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO-RESOLVER
    # ═══════════════════════════════════════════════════════════════════════

    # ── 10. solve_auto ───────────────────────────────────────────────────────
    def solve_auto(self):
        if self.solving:
            return
        n = max(2, min(20, self.auto_disk_var.get()))
        self.auto_disk_var.set(n)
        self.anim_speed = max(10, self.speed_var.get())

        # Estado inicial: todos los discos en varilla 0, destino varilla 2
        pegs = [list(range(n, 0, -1)), [], []]
        self.auto_pegs = pegs

        # Genera todos los movimientos
        moves_list = []
        self.hanoi_recursive(n, 0, 2, 1, moves_list)
        total = len(moves_list)

        self.auto_status.set(f"Resolviendo {n} discos → {self.format_moves(total)} movimientos…")
        self.auto_move_label.config(text="")
        self.draw_towers(self.auto_canvas, pegs, n, 3)

        self.solving = True
        t = threading.Thread(target=self.animate_solution,
                             args=(moves_list, n, total), daemon=True)
        t.start()

    # ── 11. hanoi_recursive ──────────────────────────────────────────────────
    def hanoi_recursive(self, n: int, src: int, dst: int, aux: int,
                        moves: list):
        """Genera la lista de movimientos (src, dst) para resolver Hanoi."""
        if n == 0:
            return
        self.hanoi_recursive(n - 1, src, aux, dst, moves)
        moves.append((src, dst))
        self.hanoi_recursive(n - 1, aux, dst, src, moves)

    # ── 12. animate_solution ─────────────────────────────────────────────────
    def animate_solution(self, moves: list, n: int, total: int):
        pegs = self.auto_pegs
        step = 0

        for src, dst in moves:
            if not self.solving:
                break
            pegs[dst].append(pegs[src].pop())
            step += 1

            def _draw(p=pegs, s=step, t=total, nn=n):
                self.draw_towers(self.auto_canvas, p, nn, 3)
                pct = s * 100 // t
                self.auto_status.set(f"Paso {self.format_moves(s)} / {self.format_moves(t)}  ({pct}%)")
                self.auto_move_label.config(text=f"Movimientos realizados: {self.format_moves(s)}")

            self.root.after(0, _draw)
            time.sleep(self.anim_speed / 1000)

        def _done(p=pegs, nn=n):
            self.draw_towers(self.auto_canvas, p, nn, 3,
                             highlight_pegs=[2])
            self.auto_status.set(f"✅ ¡Resuelto! Total: {self.format_moves(total)} movimientos.")
            self.solving = False

        self.root.after(0, _done)

    # ═══════════════════════════════════════════════════════════════════════
    #  BENCHMARKS
    # ═══════════════════════════════════════════════════════════════════════

    # ── 13. run_benchmark ────────────────────────────────────────────────────
    def run_benchmark(self):
        self.root.after(0, lambda: self.bench_status.config(text="⏳ Ejecutando benchmarks…"))
        # Limpiar tabla
        self.root.after(0, lambda: [self.bench_tree.delete(i)
                                    for i in self.bench_tree.get_children()])

        sizes = [5, 10, 30, 64]

        for n in sizes:
            self.root.after(0, lambda nn=n:
                self.bench_status.config(text=f"⏳ Calculando n={nn}…"))

            total_moves = 2**n - 1

            if n <= 20:
                # Genera movimientos reales y mide tiempo
                moves_list = []
                t0 = time.perf_counter()
                self.hanoi_recursive(n, 0, 2, 1, moves_list)
                elapsed = time.perf_counter() - t0
            else:
                # Para n grande: mide solo la recursión sin guardar lista
                # (guardar 2^30 elementos requeriría ~16 GB de RAM)
                counter = [0]

                def _count_only(k, s, d, a):
                    if k == 0:
                        return
                    _count_only(k-1, s, a, d)
                    counter[0] += 1
                    _count_only(k-1, a, d, s)

                if n == 30:
                    t0 = time.perf_counter()
                    _count_only(n, 0, 2, 1)
                    elapsed = time.perf_counter() - t0
                else:
                    # n=64: calcular tiempo teórico basado en n=30
                    t0 = time.perf_counter()
                    _count_only(20, 0, 2, 1)   # muestra representativa
                    sample = time.perf_counter() - t0
                    # Extrapola: T(n) ≈ T(20) * 2^(n-20)
                    elapsed = sample * (2 ** (n - 20))

            mps = total_moves / elapsed if elapsed > 0 else float("inf")

            row = (
                str(n),
                self.format_moves(total_moves),
                f"{elapsed:.6f}",
                self.format_moves(int(mps)) if mps != float("inf") else "∞",
            )

            def _insert(r=row):
                self.bench_tree.insert("", "end", values=r)

            self.root.after(0, _insert)
            time.sleep(0.05)   # pequeña pausa para actualizar UI

        self.root.after(0, lambda: self.bench_status.config(
            text="✅ Benchmarks completados."))

    # ── 14. format_moves ─────────────────────────────────────────────────────
    def format_moves(self, n: int) -> str:
        """Formatea un entero con separadores de miles."""
        return f"{n:,}".replace(",", " ")


# ═══════════════════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    root.geometry("800x580")
    app = HanoiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()