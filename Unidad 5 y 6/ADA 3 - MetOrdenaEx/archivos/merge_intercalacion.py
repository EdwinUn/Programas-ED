"""
merge_gui.py
============
Interfaz gráfica para Ordenamiento por Intercalación (Merge Sort).
Acepta CUALQUIER tipo de archivo de texto: .txt, .json, .csv, .tsv,
.dat, .log, o cualquier archivo plano con datos separados por líneas,
comas, punto y coma, o tabuladores.

El formato se detecta AUTOMÁTICAMENTE — el usuario solo elige archivos.

Requisitos: Python 3.8+  (tkinter incluido en la instalación estándar)
Ejecucion  : python merge_gui.py
"""

import csv
import io
import json
import os
import threading
import time  # <-- AÑADIDO: Necesario para la animación visual
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any


# ══════════════════════════════════════════════════════════
#  PALETA Y ESTILOS
# ══════════════════════════════════════════════════════════
DARK_BG   = "#0f1117"
PANEL_BG  = "#1a1d27"
CARD_BG   = "#21253a"
ACCENT    = "#6c63ff"
ACCENT2   = "#00d4aa"
TEXT_PRI  = "#e8eaf6"
TEXT_SEC  = "#8b90b0"
ERROR_CLR = "#ff5f6d"
OK_CLR    = "#00d4aa"
BORDER    = "#2e3352"

FONT_TITLE = ("Courier New", 22, "bold")
FONT_LABEL = ("Courier New", 10, "bold")
FONT_MONO  = ("Courier New", 9)
FONT_BTN   = ("Courier New", 10, "bold")
FONT_SMALL = ("Courier New", 8)


# ══════════════════════════════════════════════════════════
#  DETECCION Y CARGA UNIVERSAL DE ARCHIVOS
# ══════════════════════════════════════════════════════════

def _convertir(valor: str) -> Any:
    """Convierte cadena a int, float o string normalizado."""
    v = valor.strip()
    if not v:
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v.lower()


def _aplanar(obj: Any) -> list:
    """
    Aplana recursivamente dicts y listas anidadas en una lista plana.
    Util para JSONs con estructura compleja o anidada.
    """
    if isinstance(obj, list):
        resultado = []
        for item in obj:
            resultado.extend(_aplanar(item))
        return resultado
    if isinstance(obj, dict):
        resultado = []
        for v in obj.values():
            resultado.extend(_aplanar(v))
        return resultado
    convertido = _convertir(str(obj))
    return [convertido] if convertido is not None else []


def _detectar_delimitador(texto: str) -> str:
    """
    Detecta el delimitador predominante en texto tipo CSV/TSV.
    Prueba: tabulador, punto y coma, coma, pipe.
    """
    candidatos = ["\t", ";", ",", "|"]
    conteos = {d: texto.count(d) for d in candidatos}
    mejor = max(conteos, key=conteos.get)
    return mejor if conteos[mejor] > 0 else "\n"


def cargar_archivo(ruta: str, log=None) -> list:
    """
    Carga CUALQUIER archivo de texto y extrae una lista de valores.

    Estrategia automatica por extension:
      .json        -> parsea JSON, aplana toda estructura anidada
      .csv / .tsv  -> lee como tabla, extrae todas las celdas
      .txt / .dat /
      .log / otros -> detecta si hay delimitador horizontal;
                      si no, lee una entrada por linea (caso tipico)

    Siempre descarta valores vacios del resultado final.
    """
    ext    = os.path.splitext(ruta)[1].lower()
    nombre = os.path.basename(ruta)

    if log:
        log(f"   Formato detectado: {ext.upper() if ext else 'TEXTO PLANO'}", "dim")

    with open(ruta, "r", encoding="utf-8", errors="replace") as f:
        contenido = f.read()

    # ── JSON ────────────────────────────────────────────────
    if ext == ".json":
        try:
            datos = json.loads(contenido)
            valores = _aplanar(datos)
            if log:
                log("   JSON parseado correctamente.", "ok")
            return [v for v in valores if v is not None]
        except json.JSONDecodeError as e:
            raise ValueError(f"'{nombre}' no es JSON valido: {e}")

    # ── CSV / TSV ────────────────────────────────────────────
    if ext in (".csv", ".tsv"):
        delim = "\t" if ext == ".tsv" else _detectar_delimitador(contenido)
        if log:
            log(f"   Delimitador: {'TAB' if delim == chr(9) else repr(delim)}", "dim")
        lector = csv.reader(io.StringIO(contenido), delimiter=delim)
        valores = []
        for fila in lector:
            for celda in fila:
                v = _convertir(celda)
                if v is not None:
                    valores.append(v)
        return valores

    # ── TXT / DAT / LOG / cualquier texto plano ─────────────
    lineas = [l.strip() for l in contenido.splitlines() if l.strip()]

    # Si hay mas delimitadores que lineas => datos horizontales
    delim = _detectar_delimitador(contenido)
    if delim != "\n" and contenido.count(delim) > len(lineas):
        if log:
            log(f"   Datos separados por {repr(delim)}, expandiendo...", "dim")
        lector = csv.reader(io.StringIO(contenido), delimiter=delim)
        valores = []
        for fila in lector:
            for celda in fila:
                v = _convertir(celda)
                if v is not None:
                    valores.append(v)
        return valores

    # Fallback: una entrada por linea
    valores = []
    for linea in lineas:
        v = _convertir(linea)
        if v is not None:
            valores.append(v)
    return valores


# ══════════════════════════════════════════════════════════
#  ALGORITMO DE INTERCALACION MANUAL
# ══════════════════════════════════════════════════════════

def _comparar(a: Any, b: Any) -> int:
    """Comparacion segura entre tipos mixtos (numeros antes que strings)."""
    es_num_a = isinstance(a, (int, float))
    es_num_b = isinstance(b, (int, float))
    if es_num_a and not es_num_b:
        return -1
    if not es_num_a and es_num_b:
        return 1
    return -1 if a < b else (1 if a > b else 0)


def _intercalar(a: list, b: list) -> list:
    """
    Mezcla dos listas YA ORDENADAS en una sola lista ordenada.
    Estrategia de dos punteros — O(n+m), sin .sort().
    """
    resultado, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if _comparar(a[i], b[j]) <= 0:
            resultado.append(a[i]); i += 1
        else:
            resultado.append(b[j]); j += 1
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado


def _merge_sort(lst: list) -> list:
    """Merge Sort recursivo para pre-ordenar listas desordenadas."""
    if len(lst) <= 1:
        return lst
    m = len(lst) // 2
    return _intercalar(_merge_sort(lst[:m]), _merge_sort(lst[m:]))


def esta_ordenada(lst: list) -> bool:
    return all(_comparar(lst[i], lst[i + 1]) <= 0 for i in range(len(lst) - 1))


# ══════════════════════════════════════════════════════════
#  ORQUESTADOR PRINCIPAL (MODIFICADO PARA ANIMACIÓN)
# ══════════════════════════════════════════════════════════

def procesar(ruta_a: str, ruta_b: str, ruta_out: str, log) -> None:
    log("Iniciando proceso...", "info")

    # Archivo A
    log(f"Archivo A -> {os.path.basename(ruta_a)}", "info")
    lista_a = cargar_archivo(ruta_a, log)
    if not lista_a:
        raise ValueError(f"No se extrajeron datos de '{os.path.basename(ruta_a)}'.")
    log(f"   {len(lista_a)} elemento(s) cargado(s).", "ok")
    # MODIFICACIÓN: Mostrar previsualización completa en la consola
    log(f"   ► PREVISUALIZACIÓN A: {lista_a}", "success") 

    # Archivo B
    log(f"\nArchivo B -> {os.path.basename(ruta_b)}", "info")
    lista_b = cargar_archivo(ruta_b, log)
    if not lista_b:
        raise ValueError(f"No se extrajeron datos de '{os.path.basename(ruta_b)}'.")
    log(f"   {len(lista_b)} elemento(s) cargado(s).", "ok")
    # MODIFICACIÓN: Mostrar previsualización completa en la consola
    log(f"   ► PREVISUALIZACIÓN B: {lista_b}\n", "success")

    log("Analizando datos... (pausa para leer previsualizaciones)", "warn")
    time.sleep(2.0) # Pausa para que el usuario pueda leer los datos cargados

    # Verificacion y pre-ordenamiento
    log("Verificando pre-ordenamiento...", "info")
    if esta_ordenada(lista_a):
        log("   Archivo A ya estaba ordenado.", "ok")
    else:
        log("   Archivo A desordenado -> aplicando Merge Sort interno.", "warn")
        lista_a = _merge_sort(lista_a)

    if esta_ordenada(lista_b):
        log("   Archivo B ya estaba ordenado.", "ok")
    else:
        log("   Archivo B desordenado -> aplicando Merge Sort interno.", "warn")
        lista_b = _merge_sort(lista_b)

    # MODIFICACIÓN: Intercalacion Visual paso a paso
    log("\nEjecutando intercalacion manual VISUAL...", "info")
    
    resultado, i, j = [], 0, 0
    while i < len(lista_a) and j < len(lista_b):
        log(f"Comparando: A[{i}]={lista_a[i]} vs B[{j}]={lista_b[j]}", "dim")
        if _comparar(lista_a[i], lista_b[j]) <= 0:
            log(f"   --> Gana A: {lista_a[i]}", "ok")
            resultado.append(lista_a[i])
            i += 1
        else:
            log(f"   --> Gana B: {lista_b[j]}", "ok")
            resultado.append(lista_b[j])
            j += 1
        time.sleep(0.3) # MODIFICACIÓN: Retraso para animar la consola

    # Agregar sobrantes
    if i < len(lista_a):
        log(f"Agregando restos de A: {lista_a[i:]}", "dim")
        resultado.extend(lista_a[i:])
    if j < len(lista_b):
        log(f"Agregando restos de B: {lista_b[j:]}", "dim")
        resultado.extend(lista_b[j:])
        
    log(f"\n   ► {len(resultado)} elementos intercalados con éxito.", "success")
    log(f"   RESULTADO FINAL: {resultado}", "dim")

    # Guardado
    with open(ruta_out, "w", encoding="utf-8") as f:
        f.write("\n".join(str(e) for e in resultado) + "\n")

    log(f"\nResultado guardado -> {os.path.basename(ruta_out)}", "ok")
    log("Proceso completado exitosamente!", "success")


# ══════════════════════════════════════════════════════════
#  TIPOS DE ARCHIVO ACEPTADOS EN EL EXPLORADOR
# ══════════════════════════════════════════════════════════
TIPOS_ARCHIVO = [
    ("Todos los formatos soportados", "*.txt *.json *.csv *.tsv *.dat *.log"),
    ("Texto plano",                   "*.txt"),
    ("JSON",                          "*.json"),
    ("CSV",                           "*.csv"),
    ("TSV",                           "*.tsv"),
    ("Datos / Log",                   "*.dat *.log"),
    ("Cualquier archivo",             "*.*"),
]


# ══════════════════════════════════════════════════════════
#  COMPONENTES GUI
# ══════════════════════════════════════════════════════════

class FilePickerRow(tk.Frame):
    """Fila con selector de archivo y badge de formato automatico."""

    COLORES_EXT = {
        ".JSON": ("#ffd166", DARK_BG),
        ".CSV":  (ACCENT2,   DARK_BG),
        ".TSV":  ("#a29bfe", DARK_BG),
        ".TXT":  (TEXT_PRI,  CARD_BG),
        ".DAT":  ("#fd79a8", DARK_BG),
        ".LOG":  ("#74b9ff", DARK_BG),
    }

    def __init__(self, parent, label: str, **kwargs):
        super().__init__(parent, bg=PANEL_BG, **kwargs)
        self._path = tk.StringVar()
        self._path.trace_add("write", self._actualizar_badge)

        # Etiqueta
        tk.Label(
            self, text=label, bg=PANEL_BG, fg=ACCENT,
            font=FONT_LABEL, width=12, anchor="w",
        ).pack(side="left", padx=(0, 8))

        # Entry de ruta
        self.entry = tk.Entry(
            self, textvariable=self._path,
            bg=CARD_BG, fg=TEXT_PRI,
            insertbackground=ACCENT,
            relief="flat", font=FONT_MONO,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        # Badge de formato
        self.badge = tk.Label(
            self, text="  —  ", bg=CARD_BG, fg=TEXT_SEC,
            font=FONT_SMALL, relief="flat", padx=4, pady=3,
        )
        self.badge.pack(side="left", padx=(0, 8))

        # Boton
        tk.Button(
            self, text="EXPLORAR",
            bg=ACCENT, fg="white",
            relief="flat", font=FONT_BTN,
            padx=14, pady=4,
            activebackground="#5a52e0",
            activeforeground="white",
            cursor="hand2",
            command=self._browse,
        ).pack(side="left")

    def _browse(self):
        path = filedialog.askopenfilename(filetypes=TIPOS_ARCHIVO)
        if path:
            self._path.set(path)

    def _actualizar_badge(self, *_):
        ext = os.path.splitext(self._path.get())[1].upper()
        if ext:
            fg, bg = self.COLORES_EXT.get(ext, (TEXT_SEC, CARD_BG))
            self.badge.configure(text=f" {ext} ", fg=fg, bg=bg)
        else:
            self.badge.configure(text="  —  ", fg=TEXT_SEC, bg=CARD_BG)

    @property
    def path(self) -> str:
        return self._path.get().strip()


class ConsoleWidget(tk.Frame):
    """Panel de log estilo terminal con colores por nivel."""

    TAGS = {
        "info":    TEXT_PRI,
        "ok":      OK_CLR,
        "warn":    "#ffd166",
        "error":   ERROR_CLR,
        "success": ACCENT2,
        "dim":     TEXT_SEC,
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=DARK_BG, **kwargs)
        self.text = tk.Text(
            self, bg=DARK_BG, fg=TEXT_PRI,
            font=FONT_MONO, relief="flat",
            state="disabled", wrap="word",
            padx=12, pady=10,
            highlightthickness=0,
            cursor="arrow",
        )
        sb = tk.Scrollbar(
            self, command=self.text.yview,
            bg=PANEL_BG, troughcolor=DARK_BG,
            relief="flat", width=8,
        )
        self.text.configure(yscrollcommand=sb.set)
        self.text.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for tag, color in self.TAGS.items():
            self.text.tag_configure(tag, foreground=color)

    def log(self, message: str, kind: str = "info"):
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n", kind)
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")


# ══════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════

class MergeApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Merge Sort - Intercalacion Universal de Archivos")
        self.configure(bg=DARK_BG)
        self.resizable(True, True)
        self.minsize(740, 580)
        self._center(860, 660)
        self._build_ui()

    def _center(self, w: int, h: int):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def _build_ui(self):

        # Encabezado
        header = tk.Frame(self, bg=PANEL_BG, pady=18)
        header.pack(fill="x")

        tk.Label(
            header, text="MERGE SORT",
            bg=PANEL_BG, fg=ACCENT, font=FONT_TITLE,
        ).pack()

        tk.Label(
            header,
            text="Intercalacion universal  .txt  .json  .csv  .tsv  .dat  .log  ...",
            bg=PANEL_BG, fg=TEXT_SEC, font=FONT_SMALL,
        ).pack(pady=(4, 0))

        # Chips de formatos
        chips_frame = tk.Frame(header, bg=PANEL_BG)
        chips_frame.pack(pady=(10, 0))
        formatos = [
            (".TXT",  TEXT_PRI),
            (".JSON", "#ffd166"),
            (".CSV",  ACCENT2),
            (".TSV",  "#a29bfe"),
            (".DAT",  "#fd79a8"),
            (".LOG",  "#74b9ff"),
            ("+ cualquier texto", TEXT_SEC),
        ]
        for fmt, color in formatos:
            tk.Label(
                chips_frame, text=fmt,
                bg=CARD_BG, fg=color,
                font=FONT_SMALL, padx=7, pady=3,
            ).pack(side="left", padx=3)

        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x")

        # Cuerpo
        body = tk.Frame(self, bg=DARK_BG, padx=28, pady=22)
        body.pack(fill="both", expand=True)

        self._section(body, "ARCHIVOS DE ENTRADA  (cualquier formato)")

        self.picker_a = FilePickerRow(body, "Archivo A")
        self.picker_a.pack(fill="x", pady=(0, 10))

        self.picker_b = FilePickerRow(body, "Archivo B")
        self.picker_b.pack(fill="x", pady=(0, 18))

        self._section(body, "ARCHIVO DE SALIDA")

        out_row = tk.Frame(body, bg=DARK_BG)
        out_row.pack(fill="x", pady=(0, 18))

        self._out_path = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "resultado_ordenado.txt")
        )
        tk.Entry(
            out_row, textvariable=self._out_path,
            bg=CARD_BG, fg=TEXT_PRI,
            insertbackground=ACCENT,
            relief="flat", font=FONT_MONO,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT2,
        ).pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        tk.Button(
            out_row, text="GUARDAR EN...",
            bg=ACCENT2, fg=DARK_BG,
            relief="flat", font=FONT_BTN,
            padx=14, pady=4,
            activebackground="#00b894",
            activeforeground=DARK_BG,
            cursor="hand2",
            command=self._choose_out,
        ).pack(side="left")

        self.btn_run = tk.Button(
            body, text="EJECUTAR INTERCALACION",
            bg=ACCENT, fg="white",
            relief="flat", font=("Courier New", 12, "bold"),
            pady=12,
            activebackground="#5a52e0",
            activeforeground="white",
            cursor="hand2",
            command=self._run,
        )
        self.btn_run.pack(fill="x", pady=(0, 14))

        # Barra de progreso
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Merge.Horizontal.TProgressbar",
            troughcolor=CARD_BG, background=ACCENT,
            thickness=4, borderwidth=0,
        )
        self.progress = ttk.Progressbar(
            body, style="Merge.Horizontal.TProgressbar",
            mode="indeterminate",
        )
        self.progress.pack(fill="x", pady=(0, 12))

        self._section(body, "CONSOLA")
        self.console = ConsoleWidget(body, height=10)
        self.console.pack(fill="both", expand=True)
        self.console.log(
            "Listo. Selecciona dos archivos de cualquier formato y pulsa EJECUTAR.",
            "dim"
        )

    def _section(self, parent, title: str):
        row = tk.Frame(parent, bg=DARK_BG)
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text=title, bg=DARK_BG, fg=TEXT_SEC,
                 font=FONT_SMALL).pack(side="left")
        tk.Frame(row, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0), pady=6
        )

    def _choose_out(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile="resultado_ordenado.txt",
        )
        if path:
            self._out_path.set(path)

    def _run(self):
        ruta_a   = self.picker_a.path
        ruta_b   = self.picker_b.path
        ruta_out = self._out_path.get().strip()

        if not ruta_a:
            messagebox.showerror("Falta archivo", "Selecciona el Archivo A.")
            return
        if not ruta_b:
            messagebox.showerror("Falta archivo", "Selecciona el Archivo B.")
            return
        if not ruta_out:
            messagebox.showerror("Falta ruta", "Indica donde guardar el resultado.")
            return

        self.console.clear()
        self.btn_run.configure(state="disabled", text="Procesando...")
        self.progress.start(12)

        threading.Thread(
            target=self._worker,
            args=(ruta_a, ruta_b, ruta_out),
            daemon=True,
        ).start()

    def _worker(self, ruta_a, ruta_b, ruta_out):
        try:
            procesar(ruta_a, ruta_b, ruta_out, self.console.log)
            self.after(0, self._on_success, ruta_out)
        except FileNotFoundError as e:
            self.after(0, self._on_error, f"Archivo no encontrado:\n{e}")
        except (ValueError, json.JSONDecodeError) as e:
            self.after(0, self._on_error, f"Error al leer datos:\n{e}")
        except Exception as e:
            self.after(0, self._on_error, f"Error inesperado:\n{e}")

    def _on_success(self, ruta_out: str):
        self.progress.stop()
        self.btn_run.configure(state="normal", text="EJECUTAR INTERCALACION")
        if messagebox.askyesno(
            "Listo!",
            f"Archivo guardado:\n{ruta_out}\n\nAbrir la carpeta?",
        ):
            carpeta = os.path.dirname(ruta_out) or "."
            if os.name == "nt":
                os.startfile(carpeta)
            elif hasattr(os, "uname") and os.uname().sysname == "Darwin":
                os.system(f"open '{carpeta}'")
            else:
                os.system(f"xdg-open '{carpeta}'")

    def _on_error(self, mensaje: str):
        self.progress.stop()
        self.btn_run.configure(state="normal", text="EJECUTAR INTERCALACION")
        self.console.log(f"ERROR: {mensaje}", "error")
        messagebox.showerror("Error", mensaje)


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = MergeApp()
    app.mainloop()