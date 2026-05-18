"""
visualizador_binaria.py
────────────────────────────────────────────────────────────────
Visualizador paso a paso de los 5 métodos de busqueda_binaria.py

  Pestaña 1 → buscar_iterativo   : punteros IZQ / MED / DER
  Pestaña 2 → buscar_recursivo   : pila de llamadas recursivas
  Pestaña 3 → buscar_todos       : expansión desde ocurrencia central
  Pestaña 4 → buscar_mas_cercano : comparación de vecinos finales
  Pestaña 5 → buscar_en_rango    : dos fases de acotación

Requiere: busqueda_binaria.py en la misma carpeta.
"""

import tkinter as tk
from tkinter import messagebox
from busqueda_binaria import BusquedaBinaria

# ── Paleta ─────────────────────────────────────────────────────
BG        = "#0d1117"
BG_PANEL  = "#161b22"
BG_CARD   = "#21262d"
BG_ENTRY  = "#2d333b"
C_TEXT    = "#cdd9e5"
C_MUTED   = "#768390"
C_ACCENT  = "#539bf5"
C_GREEN   = "#57ab5a"
C_YELLOW  = "#daaa3f"
C_RED     = "#e5534b"
C_PURPLE  = "#b083f0"
C_ORANGE  = "#e5873a"
C_TEAL    = "#39c5cf"
C_WHITE   = "#ffffff"

# Estados de celda → color de relleno
ST_IDLE    = "#21262d"
ST_ACTIVE  = "#6e5101"   # mid comparándose
ST_ELIM    = "#161b22"   # mitad descartada
ST_FOUND   = "#1b4721"   # encontrado
ST_EXPAND  = "#0e3a6e"   # expansión buscar_todos
ST_RANGE   = "#0e3a6e"   # dentro del rango
ST_CLOSEST = "#4b1d20"   # vecino más cercano
ST_PHASE1  = "#1c3a2e"   # fase 1 en rango
ST_PHASE2  = "#1a2d4a"   # fase 2 en rango

# Bordes de estado
BD_IDLE    = "#444c56"
BD_ACTIVE  = C_YELLOW
BD_ELIM    = "#2d333b"
BD_FOUND   = C_GREEN
BD_EXPAND  = C_ACCENT
BD_RANGE   = C_ACCENT
BD_CLOSEST = C_RED
BD_PHASE1  = C_TEAL
BD_PHASE2  = C_PURPLE

F_TITLE = ("Segoe UI", 16, "bold")
F_TAB   = ("Segoe UI",  9, "bold")
F_LABEL = ("Segoe UI", 10)
F_SMALL = ("Segoe UI",  9)
F_MONO  = ("Courier New", 10)
F_CELL  = ("Courier New", 13, "bold")
F_INFO  = ("Courier New", 9)

TABS = [
    ("1  Iterativo",   "#539bf5"),
    ("2  Recursivo",   "#b083f0"),
    ("3  Buscar Todos","#57ab5a"),
    ("4  Más Cercano", "#e5873a"),
    ("5  En Rango",    "#39c5cf"),
]

# ══════════════════════════════════════════════════════════════════
class Visualizador:

    def __init__(self, root):
        self.root      = root
        self.root.title("Visualizador — Búsqueda Binaria")
        self.root.configure(bg=BG)
        self.root.minsize(940, 620)

        self.tab_actual  = 0
        self.pasos       = []
        self.paso_idx    = 0
        self.after_id    = None
        self.animando    = False

        self._build_ui()

    # ── Construcción de UI ──────────────────────────────────────

    def _build_ui(self):
        # Encabezado
        hdr = tk.Frame(self.root, bg=BG_PANEL, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⟨/⟩  Búsqueda Binaria — Visualizador",
                 font=F_TITLE, bg=BG_PANEL, fg=C_ACCENT).pack(side="left", padx=20)
        tk.Label(hdr, text="Visualización paso a paso · powered by busqueda_binaria.py",
                 font=F_SMALL, bg=BG_PANEL, fg=C_MUTED).pack(side="left", padx=6)

        # Pestañas
        self.frm_tabs = tk.Frame(self.root, bg=BG, pady=6)
        self.frm_tabs.pack(fill="x", padx=16)
        self.btns_tab = []
        for i, (nombre, color) in enumerate(TABS):
            b = tk.Button(self.frm_tabs, text=nombre, font=F_TAB,
                          relief="flat", cursor="hand2", padx=14, pady=6,
                          command=lambda n=i: self._cambiar_tab(n))
            b.pack(side="left", padx=3)
            self.btns_tab.append((b, color))
        self._resaltar_tab(0)

        # Panel de entrada (cambia por tab)
        self.frm_entrada = tk.Frame(self.root, bg=BG_PANEL, padx=16, pady=10)
        self.frm_entrada.pack(fill="x", padx=0)

        # Canvas principal
        self.canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0, height=260)
        self.canvas.pack(fill="x", padx=16, pady=(10, 0))
        self.canvas.bind("<Configure>", lambda e: self._redibujar())

        # Barra de llamada a librería
        self.frm_lib = tk.Frame(self.root, bg=BG_CARD, padx=14, pady=6)
        self.frm_lib.pack(fill="x", padx=16, pady=(6, 0))
        tk.Label(self.frm_lib, text="Llamada a librería:",
                 font=F_SMALL, bg=BG_CARD, fg=C_MUTED).pack(side="left")
        self.lbl_lib = tk.Label(self.frm_lib, text="—",
                                font=F_INFO, bg=BG_CARD, fg=C_ACCENT)
        self.lbl_lib.pack(side="left", padx=8)

        # Barra de estado
        self.frm_status = tk.Frame(self.root, bg=BG_PANEL, padx=14, pady=8)
        self.frm_status.pack(fill="x", padx=0, pady=(4, 0))
        self.lbl_status = tk.Label(self.frm_status, text="Configura los parámetros y presiona ▶ Iniciar.",
                                   font=F_LABEL, bg=BG_PANEL, fg=C_TEXT, anchor="w")
        self.lbl_status.pack(fill="x")

        # Pila recursiva (solo tab 2)
        self.frm_pila = tk.Frame(self.root, bg=BG, padx=16, pady=0)
        self.frm_pila.pack(fill="x")
        self.lbl_pila = tk.Label(self.frm_pila, text="",
                                 font=F_INFO, bg=BG, fg=C_PURPLE, anchor="w")
        self.lbl_pila.pack(fill="x")

        # Controles
        ctrls = tk.Frame(self.root, bg=BG, pady=10)
        ctrls.pack()
        self.btn_play = self._btn(ctrls, "▶  Iniciar",    self._iniciar,      C_ACCENT)
        self.btn_step = self._btn(ctrls, "⏭  Paso",       self._paso_manual,  "#2f6b2f")
        self.btn_rst  = self._btn(ctrls, "↺  Reiniciar",  self._reiniciar,    "#5a3a1a")
        for b in (self.btn_play, self.btn_step, self.btn_rst):
            b.pack(side="left", padx=5)

        tk.Label(ctrls, text="Velocidad:", font=F_SMALL, bg=BG, fg=C_MUTED).pack(side="left", padx=(20,4))
        self.vel = tk.IntVar(value=900)
        tk.Scale(ctrls, from_=200, to=2000, orient="horizontal",
                 variable=self.vel, bg=BG, fg=C_TEXT,
                 highlightthickness=0, troughcolor=BG_CARD,
                 length=130, showvalue=False).pack(side="left")

        # Leyenda (cambia por tab)
        self.frm_leyenda = tk.Frame(self.root, bg=BG, pady=6)
        self.frm_leyenda.pack()

        # Cargar primer tab
        self._cambiar_tab(0)

    def _btn(self, p, txt, cmd, color):
        return tk.Button(p, text=txt, command=cmd, font=("Segoe UI", 10, "bold"),
                         bg=color, fg=C_WHITE, relief="flat", padx=14, pady=6,
                         cursor="hand2", activebackground=C_ACCENT,
                         activeforeground=BG)

    # ── Gestión de tabs ─────────────────────────────────────────

    def _resaltar_tab(self, idx):
        for i, (b, color) in enumerate(self.btns_tab):
            if i == idx:
                b.config(bg=color, fg=BG)
            else:
                b.config(bg=BG_CARD, fg=C_MUTED)

    def _cambiar_tab(self, idx):
        self._reiniciar()
        self.tab_actual = idx
        self._resaltar_tab(idx)
        self._build_entrada(idx)
        self._build_leyenda(idx)
        self.lbl_pila.config(text="")

    def _build_entrada(self, idx):
        for w in self.frm_entrada.winfo_children():
            w.destroy()

        configuraciones = [
            # (label_lista, default_lista, extras)
            ("Lista ordenada:", "2,5,8,12,16,23,38,45,51,60,72,88",
             [("Buscar:", "38")]),
            ("Lista ordenada:", "3,7,14,21,28,35,42,49,56,63",
             [("Buscar (ID):", "42")]),
            ("Lista (puede tener duplicados):", "4,8,8,8,15,16,23,23,42",
             [("Buscar:", "8")]),
            ("Lista ordenada:", "10,20,30,40,50,60,70,80,90,100",
             [("Mi presupuesto:", "55")]),
            ("Lista ordenada:", "5,12,18,24,31,37,43,50,58,65,71",
             [("Mín:", "20"), ("Máx:", "55")]),
        ]

        label_l, default_l, extras = configuraciones[idx]

        tk.Label(self.frm_entrada, text=label_l,
                 font=F_SMALL, bg=BG_PANEL, fg=C_MUTED).grid(row=0, column=0, sticky="w", padx=(0,8))
        self.entry_lista = self._entry_widget(self.frm_entrada, default_l, 42)
        self.entry_lista.grid(row=0, column=1, padx=(0, 20))

        self.entries_extra = []
        for col, (lbl, default) in enumerate(extras):
            tk.Label(self.frm_entrada, text=lbl,
                     font=F_SMALL, bg=BG_PANEL, fg=C_MUTED).grid(row=0, column=2+col*2, sticky="w", padx=(0,6))
            e = self._entry_widget(self.frm_entrada, default, 8)
            e.grid(row=0, column=3+col*2, padx=(0, 12))
            self.entries_extra.append(e)

    def _entry_widget(self, parent, default, width):
        e = tk.Entry(parent, font=F_MONO, width=width, bg=BG_ENTRY,
                     fg=C_TEXT, insertbackground=C_TEXT, relief="flat", bd=5)
        e.insert(0, default)
        return e

    def _build_leyenda(self, idx):
        for w in self.frm_leyenda.winfo_children():
            w.destroy()

        leyendas = [
            [(C_YELLOW,"Comparando (MED)"),(C_MUTED,"Descartado"),(C_GREEN,"Encontrado")],
            [(C_YELLOW,"Comparando (MED)"),(C_MUTED,"Descartado"),(C_GREEN,"Encontrado"),(C_PURPLE,"Pila recursiva")],
            [(C_YELLOW,"Ocurrencia central"),(C_ACCENT,"Expansión"),(C_GREEN,"Todas las ocurrencias")],
            [(C_YELLOW,"MED actual"),(C_RED,"Vecino más cercano"),(C_GREEN,"Resultado")],
            [(C_TEAL,"Fase 1: límite izq."),(C_PURPLE,"Fase 2: límite der."),(C_ACCENT,"En rango")],
        ]
        for color, txt in leyendas[idx]:
            tk.Canvas(self.frm_leyenda, width=12, height=12, bg=color,
                      highlightthickness=0).pack(side="left", padx=(14,3))
            tk.Label(self.frm_leyenda, text=txt, font=F_SMALL,
                     bg=BG, fg=C_TEXT).pack(side="left", padx=(0,6))

    # ── Parseo ──────────────────────────────────────────────────

    def _parsear(self):
        try:
            lista = [int(x.strip()) for x in self.entry_lista.get().split(",")]
        except ValueError:
            messagebox.showerror("Error", "La lista debe contener enteros separados por coma.")
            return None
        if lista != sorted(lista):
            messagebox.showwarning("Atención", "La lista no está ordenada. Se ordenará automáticamente.")
            lista = sorted(lista)
        return lista

    def _parsear_extra(self, idx):
        try:
            return [int(e.get().strip()) for e in self.entries_extra]
        except ValueError:
            messagebox.showerror("Error", "Los parámetros adicionales deben ser enteros.")
            return None

    # ══════════════════════════════════════════════════════════════
    # GENERADORES DE PASOS (uno por método de la librería)
    # ══════════════════════════════════════════════════════════════

    # ── 1. buscar_iterativo ─────────────────────────────────────
    def _gen_iterativo(self, lista, objetivo):
        n = len(lista)
        estados = [ST_IDLE] * n
        pasos = []

        # Resultado real de la librería
        resultado = BusquedaBinaria.buscar_iterativo(lista, objetivo)

        pasos.append(self._paso(estados, [],
            f"Búsqueda de {objetivo} en lista de {n} elementos ordenada",
            f"BusquedaBinaria.buscar_iterativo({lista}, {objetivo})"))

        izq, der = 0, n - 1
        while izq <= der:
            mid = (izq + der) // 2
            e2 = estados[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq, C_ACCENT), ("MED", mid, C_YELLOW), ("DER", der, C_ORANGE)],
                f"MED = ({izq}+{der})//2 = {mid}  →  lista[{mid}] = {lista[mid]}",
                f"buscar_en_rango(lista[{izq}:{mid+1}], {objetivo}, {objetivo})  # verificar mitad izquierda"))

            # Usa la librería para saber si el objetivo está en la mitad izquierda
            en_izq = BusquedaBinaria.buscar_en_rango(lista[izq:mid+1], objetivo, objetivo)

            if lista[mid] == objetivo:
                e3 = e2[:]
                e3[mid] = ST_FOUND
                pasos.append(self._paso(e3,
                    [("✔ FOUND", mid, C_GREEN)],
                    f"✅  lista[{mid}] = {lista[mid]} == {objetivo}  →  ¡ENCONTRADO en índice {mid}!",
                    f"→ Retorna: {resultado}"))
                return pasos
            elif lista[mid] < objetivo:
                for i in range(izq, mid + 1): estados[i] = ST_ELIM
                pasos.append(self._paso(estados[:],
                    [("IZQ→", mid+1, C_ACCENT), ("DER", der, C_ORANGE)],
                    f"lista[{mid}]={lista[mid]} < {objetivo}  →  Descartamos índices {izq}–{mid}, IZQ = {mid+1}",
                    f"buscar_en_rango(lista[{mid+1}:{der+1}], {objetivo}, {objetivo})"))
                izq = mid + 1
            else:
                for i in range(mid, der + 1): estados[i] = ST_ELIM
                pasos.append(self._paso(estados[:],
                    [("IZQ", izq, C_ACCENT), ("←DER", mid-1, C_ORANGE)],
                    f"lista[{mid}]={lista[mid]} > {objetivo}  →  Descartamos índices {mid}–{der}, DER = {mid-1}",
                    f"buscar_en_rango(lista[{izq}:{mid}], {objetivo}, {objetivo})"))
                der = mid - 1

        pasos.append(self._paso([ST_ELIM]*n, [],
            f"❌  IZQ({izq}) > DER({der})  →  {objetivo} no existe en la lista.",
            f"→ Retorna: None"))
        return pasos

    # ── 2. buscar_recursivo ─────────────────────────────────────
    def _gen_recursivo(self, lista, objetivo):
        n = len(lista)
        estados = [ST_IDLE] * n
        pasos = []
        pila_log = []

        resultado = BusquedaBinaria.buscar_recursivo(lista, objetivo)

        def recurse(izq, der, prof):
            if izq > der:
                pasos.append(self._paso([ST_ELIM]*n, [],
                    f"❌  Caso base: izq({izq}) > der({der})  →  No encontrado.",
                    f"→ Retorna: None",
                    pila="  |  ".join(pila_log)))
                return

            mid = (izq + der) // 2
            pila_log.append(f"f({izq},{der})")
            e2 = estados[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq, C_ACCENT), ("MED", mid, C_YELLOW), ("DER", der, C_ORANGE)],
                f"Llamada #{len(pila_log)}: buscar_recursivo(lista, {objetivo}, izq={izq}, der={der})  →  mid={mid}, lista[{mid}]={lista[mid]}",
                f"BusquedaBinaria.buscar_recursivo(lista, {objetivo}, {izq}, {der})",
                pila="  →  ".join(pila_log)))

            # Usa librería para verificar si objetivo está en subarray
            sub = lista[izq:der+1]
            en_sub = BusquedaBinaria.buscar_en_rango(sub, objetivo, objetivo)

            if lista[mid] == objetivo:
                e3 = e2[:]
                e3[mid] = ST_FOUND
                pasos.append(self._paso(e3,
                    [("✔ FOUND", mid, C_GREEN)],
                    f"✅  lista[{mid}] = {lista[mid]} == {objetivo}  →  ¡ENCONTRADO en índice {mid}!",
                    f"→ Retorna: {resultado}",
                    pila="  →  ".join(pila_log) + "  ✔"))
            elif lista[mid] < objetivo:
                for i in range(izq, mid + 1): estados[i] = ST_ELIM
                pasos.append(self._paso(estados[:],
                    [("IZQ→", mid+1, C_ACCENT), ("DER", der, C_ORANGE)],
                    f"lista[{mid}] < {objetivo}  →  Llamada recursiva a derecha [{mid+1}, {der}]",
                    f"buscar_recursivo(lista, {objetivo}, {mid+1}, {der})",
                    pila="  →  ".join(pila_log)))
                recurse(mid + 1, der, prof + 1)
            else:
                for i in range(mid, der + 1): estados[i] = ST_ELIM
                pasos.append(self._paso(estados[:],
                    [("IZQ", izq, C_ACCENT), ("←DER", mid-1, C_ORANGE)],
                    f"lista[{mid}] > {objetivo}  →  Llamada recursiva a izquierda [{izq}, {mid-1}]",
                    f"buscar_recursivo(lista, {objetivo}, {izq}, {mid-1})",
                    pila="  →  ".join(pila_log)))
                recurse(izq, mid - 1, prof + 1)

        pasos.append(self._paso(estados, [],
            f"Búsqueda recursiva de {objetivo} — cada paso es una llamada a la función",
            f"BusquedaBinaria.buscar_recursivo({lista}, {objetivo})"))
        recurse(0, n - 1, 0)
        return pasos

    # ── 3. buscar_todos ─────────────────────────────────────────
    def _gen_buscar_todos(self, lista, objetivo):
        n = len(lista)
        estados = [ST_IDLE] * n
        pasos = []

        # Resultado real de la librería
        todos = BusquedaBinaria.buscar_todos(lista, objetivo)

        pasos.append(self._paso(estados, [],
            f"Buscar TODAS las ocurrencias de {objetivo}",
            f"BusquedaBinaria.buscar_todos({lista}, {objetivo})"))

        # Fase 1: encontrar primera ocurrencia con búsqueda binaria
        izq, der = 0, n - 1
        mid_central = None
        while izq <= der:
            mid = (izq + der) // 2
            e2 = estados[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq, C_ACCENT), ("MED", mid, C_YELLOW), ("DER", der, C_ORANGE)],
                f"Fase 1 — Encontrar una ocurrencia: lista[{mid}]={lista[mid]}",
                f"buscar_iterativo(lista, {objetivo})  # primera ocurrencia"))

            sub_izq = lista[izq:mid+1]
            en_izq = BusquedaBinaria.buscar_en_rango(sub_izq, objetivo, objetivo)

            if lista[mid] == objetivo:
                mid_central = mid
                e2[mid] = ST_FOUND
                pasos.append(self._paso(e2,
                    [("★ 1ª", mid, C_GREEN)],
                    f"✅  Primera ocurrencia en índice {mid}  →  Fase 2: expandir",
                    f"→ Ocurrencia inicial: índice {mid}"))
                break
            elif lista[mid] < objetivo:
                for i in range(izq, mid + 1): estados[i] = ST_ELIM
                izq = mid + 1
            else:
                for i in range(mid, der + 1): estados[i] = ST_ELIM
                der = mid - 1
        else:
            pasos.append(self._paso([ST_ELIM]*n, [],
                f"❌  {objetivo} no existe en la lista.",
                f"→ buscar_todos retorna: []"))
            return pasos

        if not todos:
            return pasos

        # Fase 2: expandir izquierda
        i = mid_central - 1
        encontrados = [mid_central]
        while i >= 0 and lista[i] == objetivo:
            estados[i] = ST_EXPAND
            e2 = estados[:]
            pasos.append(self._paso(e2,
                [("← exp", i, C_ACCENT)],
                f"Expandiendo izquierda: lista[{i}]={lista[i]} == {objetivo}  →  nueva ocurrencia",
                f"buscar_en_rango(lista, {objetivo}, {objetivo})  # verificar izquierda"))
            encontrados.append(i)
            i -= 1

        # Fase 3: expandir derecha
        i = mid_central + 1
        while i < n and lista[i] == objetivo:
            estados[i] = ST_EXPAND
            e2 = estados[:]
            pasos.append(self._paso(e2,
                [("exp →", i, C_ACCENT)],
                f"Expandiendo derecha: lista[{i}]={lista[i]} == {objetivo}  →  nueva ocurrencia",
                f"buscar_en_rango(lista, {objetivo}, {objetivo})  # verificar derecha"))
            encontrados.append(i)
            i += 1

        # Estado final
        e_final = [ST_ELIM]*n
        for idx in todos: e_final[idx] = ST_FOUND
        pasos.append(self._paso(e_final,
            [(f"[{idx}]", idx, C_GREEN) for idx in todos],
            f"✅  {objetivo} aparece {len(todos)} vez/veces  →  índices: {todos}",
            f"→ buscar_todos retorna: {todos}"))
        return pasos

    # ── 4. buscar_mas_cercano ───────────────────────────────────
    def _gen_mas_cercano(self, lista, objetivo):
        n = len(lista)
        estados = [ST_IDLE] * n
        pasos = []

        # Resultado real de la librería
        cercano = BusquedaBinaria.buscar_mas_cercano(lista, objetivo)

        pasos.append(self._paso(estados, [],
            f"Buscar el elemento más cercano a {objetivo} (puede no existir exactamente)",
            f"BusquedaBinaria.buscar_mas_cercano({lista}, {objetivo})"))

        izq, der = 0, n - 1
        last_izq, last_der = izq, der
        encontrado_exacto = False

        while izq <= der:
            mid = (izq + der) // 2
            e2 = estados[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq, C_ACCENT), ("MED", mid, C_YELLOW), ("DER", der, C_ORANGE)],
                f"MED={mid}, lista[{mid}]={lista[mid]}",
                f"buscar_en_rango(lista[{izq}:{mid+1}], {objetivo}, {objetivo})"))

            sub = lista[izq:mid+1]
            BusquedaBinaria.buscar_en_rango(sub, objetivo, objetivo)

            if lista[mid] == objetivo:
                e2[mid] = ST_FOUND
                pasos.append(self._paso(e2,
                    [("✔ EXACTO", mid, C_GREEN)],
                    f"✅  Coincidencia exacta: lista[{mid}] = {lista[mid]} == {objetivo}",
                    f"→ buscar_mas_cercano retorna: {cercano}"))
                encontrado_exacto = True
                break
            elif lista[mid] < objetivo:
                for i in range(izq, mid + 1): estados[i] = ST_ELIM
                last_izq = mid + 1
                izq = mid + 1
            else:
                for i in range(mid, der + 1): estados[i] = ST_ELIM
                last_der = mid - 1
                der = mid - 1

        if not encontrado_exacto:
            # Mostrar los dos vecinos y comparar distancias
            # Asegurar que los índices son válidos
            vi = min(last_izq, n - 1)
            vd = max(last_der, 0)
            e_vecinos = [ST_ELIM] * n
            e_vecinos[vi] = ST_CLOSEST
            e_vecinos[vd] = ST_CLOSEST
            pasos.append(self._paso(e_vecinos,
                [("IZQ→", vi, C_RED), ("←DER", vd, C_RED)],
                f"Rango agotado. Vecinos: lista[{vd}]={lista[vd]} y lista[{vi}]={lista[vi]}",
                f"buscar_mas_cercano: comparando |{lista[vd]}-{objetivo}| vs |{lista[vi]}-{objetivo}|"))

            idx_cercano = lista.index(cercano)
            e_final = [ST_ELIM] * n
            e_final[idx_cercano] = ST_FOUND
            dist = abs(cercano - objetivo)
            pasos.append(self._paso(e_final,
                [("≈ CERCANO", idx_cercano, C_GREEN)],
                f"✅  Elemento más cercano a {objetivo}:  {cercano}  (distancia = {dist})",
                f"→ buscar_mas_cercano retorna: {cercano}"))
        return pasos

    # ── 5. buscar_en_rango ──────────────────────────────────────
    def _gen_en_rango(self, lista, minimo, maximo):
        n = len(lista)
        estados = [ST_IDLE] * n
        pasos = []

        # Resultado real de la librería
        resultado = BusquedaBinaria.buscar_en_rango(lista, minimo, maximo)

        pasos.append(self._paso(estados, [],
            f"Buscar todos los elementos en rango [{minimo}, {maximo}]",
            f"BusquedaBinaria.buscar_en_rango({lista}, {minimo}, {maximo})"))

        # Fase 1: encontrar límite izquierdo (primer índice >= minimo)
        izq, der, inicio = 0, n - 1, None
        while izq <= der:
            mid = (izq + der) // 2
            e2 = estados[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq, C_TEAL), ("MED", mid, C_YELLOW), ("DER", der, C_TEAL)],
                f"FASE 1 — Límite izquierdo: lista[{mid}]={lista[mid]} >= {minimo}?",
                f"buscar_en_rango: buscando primer índice >= {minimo}"))

            sub = lista[izq:mid+1]
            BusquedaBinaria.buscar_en_rango(sub, minimo, lista[mid] if lista[mid] >= minimo else minimo)

            if lista[mid] >= minimo:
                inicio = mid
                e2[mid] = ST_PHASE1
                pasos.append(self._paso(e2,
                    [("↓LIM.IZQ", mid, C_TEAL)],
                    f"lista[{mid}]={lista[mid]} >= {minimo}  →  candidato para límite izquierdo, DER={mid-1}",
                    f"inicio = {mid}, seguir buscando hacia la izquierda"))
                der = mid - 1
            else:
                for i in range(izq, mid + 1): estados[i] = ST_ELIM
                pasos.append(self._paso(estados[:],
                    [("IZQ→", mid+1, C_TEAL)],
                    f"lista[{mid}]={lista[mid]} < {minimo}  →  Avanzar IZQ = {mid+1}",
                    f"buscar_en_rango: ajustando izquierda"))
                izq = mid + 1

        if inicio is None:
            pasos.append(self._paso([ST_ELIM]*n, [],
                f"❌  No hay elementos >= {minimo}.",
                f"→ buscar_en_rango retorna: []"))
            return pasos

        # Fase 2: encontrar límite derecho (último índice <= maximo)
        izq2, der2, fin = inicio, n - 1, None
        estados2 = [ST_IDLE] * n
        estados2[inicio] = ST_PHASE1
        while izq2 <= der2:
            mid = (izq2 + der2) // 2
            e2 = estados2[:]
            e2[mid] = ST_ACTIVE
            pasos.append(self._paso(e2,
                [("IZQ", izq2, C_PURPLE), ("MED", mid, C_YELLOW), ("DER", der2, C_PURPLE)],
                f"FASE 2 — Límite derecho: lista[{mid}]={lista[mid]} <= {maximo}?",
                f"buscar_en_rango: buscando último índice <= {maximo}"))

            sub = lista[mid:der2+1]
            BusquedaBinaria.buscar_en_rango(sub, lista[mid], maximo if lista[mid] <= maximo else lista[mid])

            if lista[mid] <= maximo:
                fin = mid
                e2[mid] = ST_PHASE2
                pasos.append(self._paso(e2,
                    [("LIM.DER↓", mid, C_PURPLE)],
                    f"lista[{mid}]={lista[mid]} <= {maximo}  →  candidato límite derecho, IZQ={mid+1}",
                    f"fin = {mid}, seguir buscando hacia la derecha"))
                izq2 = mid + 1
            else:
                for i in range(mid, der2 + 1): estados2[i] = ST_ELIM
                pasos.append(self._paso(estados2[:],
                    [("←DER", mid-1, C_PURPLE)],
                    f"lista[{mid}]={lista[mid]} > {maximo}  →  Reducir DER = {mid-1}",
                    f"buscar_en_rango: ajustando derecha"))
                der2 = mid - 1

        if fin is None:
            pasos.append(self._paso([ST_ELIM]*n, [],
                f"❌  No hay elementos <= {maximo} desde el índice {inicio}.",
                f"→ buscar_en_rango retorna: []"))
            return pasos

        # Resultado final
        e_final = [ST_ELIM] * n
        for i in range(inicio, fin + 1): e_final[i] = ST_RANGE
        pasos.append(self._paso(e_final,
            [("inicio", inicio, C_TEAL), ("fin", fin, C_PURPLE)],
            f"✅  Elementos en [{minimo}, {maximo}]:  {resultado}  ({len(resultado)} elementos, índices {inicio}–{fin})",
            f"→ buscar_en_rango retorna: {resultado}"))
        return pasos

    # ── Helper paso ─────────────────────────────────────────────

    def _paso(self, estados, punteros, msg, lib, pila=""):
        return {"estados": list(estados), "punteros": list(punteros),
                "msg": msg, "lib": lib, "pila": pila}

    # ── Animación ───────────────────────────────────────────────

    def _iniciar(self):
        if self.animando: return
        pasos = self._construir_pasos()
        if pasos is None: return
        self.pasos      = pasos
        self.paso_idx   = 0
        self.animando   = True
        self.btn_step.config(state="disabled")
        self._ejecutar_paso_auto()

    def _paso_manual(self):
        if self.animando: return
        if not self.pasos:
            pasos = self._construir_pasos()
            if pasos is None: return
            self.pasos    = pasos
            self.paso_idx = 0
        self._mostrar_paso(self.paso_idx)
        self.paso_idx += 1

    def _ejecutar_paso_auto(self):
        if not self.animando or self.paso_idx >= len(self.pasos):
            self.animando = False
            self.btn_step.config(state="normal")
            return
        self._mostrar_paso(self.paso_idx)
        self.paso_idx += 1
        self.after_id = self.root.after(self.vel.get(), self._ejecutar_paso_auto)

    def _reiniciar(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.animando  = False
        self.pasos     = []
        self.paso_idx  = 0
        self.canvas.delete("all")
        self.lbl_status.config(text="Configura los parámetros y presiona ▶ Iniciar.", fg=C_TEXT)
        self.lbl_lib.config(text="—")
        self.lbl_pila.config(text="")
        self.btn_step.config(state="normal")

    def _construir_pasos(self):
        lista = self._parsear()
        if lista is None: return None
        t = self.tab_actual
        if t == 0:
            extra = self._parsear_extra(t)
            if extra is None: return None
            return self._gen_iterativo(lista, extra[0])
        elif t == 1:
            extra = self._parsear_extra(t)
            if extra is None: return None
            return self._gen_recursivo(lista, extra[0])
        elif t == 2:
            extra = self._parsear_extra(t)
            if extra is None: return None
            return self._gen_buscar_todos(lista, extra[0])
        elif t == 3:
            extra = self._parsear_extra(t)
            if extra is None: return None
            return self._gen_mas_cercano(lista, extra[0])
        elif t == 4:
            extra = self._parsear_extra(t)
            if extra is None: return None
            return self._gen_en_rango(lista, extra[0], extra[1])

    def _mostrar_paso(self, idx):
        if idx >= len(self.pasos): return
        p = self.pasos[idx]
        self._dibujar(p["estados"], p["punteros"])
        self.lbl_status.config(text=p["msg"],
                               fg=C_GREEN if "✅" in p["msg"] else
                                  C_RED   if "❌" in p["msg"] else C_TEXT)
        self.lbl_lib.config(text=p["lib"])
        self.lbl_pila.config(text=f"Pila: {p['pila']}" if p.get("pila") else "")

    # ── Dibujo ──────────────────────────────────────────────────

    def _redibujar(self):
        if self.pasos and self.paso_idx > 0:
            idx = min(self.paso_idx - 1, len(self.pasos) - 1)
            p = self.pasos[idx]
            self._dibujar(p["estados"], p["punteros"])

    BORDERS = {
        ST_IDLE: BD_IDLE, ST_ACTIVE: BD_ACTIVE, ST_ELIM: BD_ELIM,
        ST_FOUND: BD_FOUND, ST_EXPAND: BD_EXPAND, ST_RANGE: BD_RANGE,
        ST_CLOSEST: BD_CLOSEST, ST_PHASE1: BD_PHASE1, ST_PHASE2: BD_PHASE2,
    }
    TEXT_COLORS = {
        ST_IDLE: C_TEXT, ST_ACTIVE: C_YELLOW, ST_ELIM: C_MUTED,
        ST_FOUND: C_GREEN, ST_EXPAND: C_ACCENT, ST_RANGE: C_ACCENT,
        ST_CLOSEST: C_RED, ST_PHASE1: C_TEAL, ST_PHASE2: C_PURPLE,
    }

    def _dibujar(self, estados, punteros):
        self.canvas.delete("all")
        n = len(estados)
        if n == 0: return

        W    = self.canvas.winfo_width() or 900
        H    = self.canvas.winfo_height() or 260
        cel  = min(68, max(36, (W - 40) // n - 6))
        gap  = min(8, max(3, (W - 40 - n * cel) // max(n - 1, 1)))
        tot  = n * cel + (n - 1) * gap
        x0   = (W - tot) // 2
        y0   = 50

        # Área de punteros superior (IZQ, DER) y etiquetas
        for i, estado in enumerate(estados):
            x = x0 + i * (cel + gap)
            fill   = estado
            border = self.BORDERS.get(estado, BD_IDLE)
            tc     = self.TEXT_COLORS.get(estado, C_TEXT)

            # Sombra
            self.canvas.create_rectangle(x+3, y0+3, x+cel+3, y0+cel+3,
                                         fill="#070a0f", outline="")
            # Celda
            self.canvas.create_rectangle(x, y0, x+cel, y0+cel,
                                         fill=fill, outline=border, width=2)

            # Lista ordenada: marcar con pequeño triángulo
            if estado not in (ST_ELIM,):
                # Pequeño indicador visual de "ordenado" en esquina superior
                pass

            # Valor
            fs = max(9, min(14, cel // 5))
            # Obtener lista actual para el valor
            lista_actual = None
            if self.pasos and self.paso_idx > 0:
                # Buscamos los valores de la lista parseada
                pass
            self.canvas.create_text(x + cel//2, y0 + cel//2,
                                    text="?", font=("Courier New", fs, "bold"),
                                    fill=tc)
            # Índice
            self.canvas.create_text(x + cel//2, y0 + cel + 13,
                                    text=f"[{i}]", font=F_SMALL, fill=C_MUTED)

        # Punteros (flechas encima de celdas)
        ptr_usados = {}
        for label, idx, color in punteros:
            if idx < 0 or idx >= n: continue
            x = x0 + idx * (cel + gap) + cel // 2
            offset = ptr_usados.get(idx, 0)
            yp = y0 - 18 - offset * 14
            ptr_usados[idx] = offset + 1
            self.canvas.create_polygon(x-6, yp, x+6, yp, x, yp+8,
                                       fill=color, outline="")
            self.canvas.create_text(x, yp - 9, text=label,
                                    font=("Segoe UI", 7, "bold"), fill=color)

    def _dibujar(self, estados, punteros):
        """Versión final con valores reales de la lista."""
        self.canvas.delete("all")
        n = len(estados)
        if n == 0: return

        # Obtener lista actual
        lista_str = self.entry_lista.get()
        try:
            lista = sorted([int(x.strip()) for x in lista_str.split(",")])
        except Exception:
            lista = list(range(n))
        if len(lista) != n:
            lista = lista[:n] if len(lista) >= n else lista + [0]*(n - len(lista))

        W   = max(self.canvas.winfo_width(), 900)
        H   = max(self.canvas.winfo_height(), 240)
        cel = min(68, max(38, (W - 60) // n - 6))
        gap = min(10, max(2, (W - 60 - n * cel) // max(n - 1, 1)))
        tot = n * cel + (n - 1) * gap
        x0  = (W - tot) // 2
        y0  = 60

        for i, estado in enumerate(estados):
            x      = x0 + i * (cel + gap)
            fill   = estado
            border = self.BORDERS.get(estado, BD_IDLE)
            tc     = self.TEXT_COLORS.get(estado, C_TEXT)
            val    = lista[i] if i < len(lista) else "?"

            # Sombra
            self.canvas.create_rectangle(x+3, y0+3, x+cel+3, y0+cel+3,
                                         fill="#070a0f", outline="")
            # Celda
            self.canvas.create_rectangle(x, y0, x+cel, y0+cel,
                                         fill=fill, outline=border, width=2)
            # Valor
            fs = max(9, min(14, cel // 5))
            self.canvas.create_text(x + cel//2, y0 + cel//2,
                                    text=str(val),
                                    font=("Courier New", fs, "bold"),
                                    fill=tc)
            # Índice
            self.canvas.create_text(x + cel//2, y0 + cel + 13,
                                    text=f"[{i}]", font=("Segoe UI", 8), fill=C_MUTED)

        # Punteros
        conteo = {}
        for label, idx, color in punteros:
            if not (0 <= idx < n): continue
            cx = x0 + idx * (cel + gap) + cel // 2
            n_ptr = conteo.get(idx, 0)
            yp = y0 - 20 - n_ptr * 16
            conteo[idx] = n_ptr + 1
            self.canvas.create_polygon(cx-7, yp, cx+7, yp, cx, yp+9,
                                       fill=color, outline="")
            self.canvas.create_text(cx, yp - 10, text=label,
                                    font=("Segoe UI", 7, "bold"), fill=color)

        # Paso actual / total
        if self.pasos:
            self.canvas.create_text(W - 12, 8, anchor="ne",
                                    text=f"Paso {min(self.paso_idx, len(self.pasos))} / {len(self.pasos)}",
                                    font=F_SMALL, fill=C_MUTED)


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    Visualizador(root)
    root.mainloop()