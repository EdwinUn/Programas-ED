import tkinter as tk
from tkinter import messagebox

class Cola:
    def __init__(self):
        self.items = []
        self.contador = 1

    def encolar(self):
        turno = self.contador
        self.items.append(turno)
        self.contador += 1
        return turno

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def esta_vacia(self):
        return len(self.items) == 0

class AppSeguros:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Turnos - Seguros")
        self.root.geometry("400x500")
        
        # Diccionario de colas (Servicio 1, 2 y 3 por defecto)
        self.servicios = {
            1: Cola(),
            2: Cola(),
            3: Cola()
        }

        self.setup_ui()

    def setup_ui(self):
        # --- SECCIÓN CLIENTE (Generar Turno) ---
        tk.Label(self.root, text="ÁREA DE CLIENTES", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
        
        frame_cliente = tk.LabelFrame(self.root, text="Solicitar Turno", padx=10, pady=10)
        frame_cliente.pack(padx=20, fill="x")

        tk.Label(frame_cliente, text="Seleccione Servicio:").pack()
        self.btn_s1 = tk.Button(frame_cliente, text="Servicio 1", width=15, command=lambda: self.nuevo_cliente(1))
        self.btn_s1.pack(pady=2)
        self.btn_s2 = tk.Button(frame_cliente, text="Servicio 2", width=15, command=lambda: self.nuevo_cliente(2))
        self.btn_s2.pack(pady=2)

        # --- SECCIÓN PERSONAL (Atender) ---
        tk.Label(self.root, text="ÁREA DE ATENCIÓN", font=("Arial", 12, "bold"), fg="green").pack(pady=20)
        
        frame_personal = tk.LabelFrame(self.root, text="Llamar Cliente", padx=10, pady=10)
        frame_personal.pack(padx=20, fill="x")

        tk.Button(frame_personal, text="Atender Servicio 1", bg="#e1f5fe", command=lambda: self.atender_cliente(1)).pack(pady=5, fill="x")
        tk.Button(frame_personal, text="Atender Servicio 2", bg="#e1f5fe", command=lambda: self.atender_cliente(2)).pack(pady=5, fill="x")

        # --- PANTALLA DE LLAMADO ---
        self.lbl_llamado = tk.Label(self.root, text="Esperando...", font=("Arial", 16, "bold"), fg="red", pady=20)
        self.lbl_llamado.pack()

    def nuevo_cliente(self, num):
        turno = self.servicios[num].encolar()
        messagebox.showinfo("Ticket Generado", f"Servicio {num}\nSu turno es el: {turno}")

    def atender_cliente(self, num):
        turno = self.servicios[num].desencolar()
        if turno:
            self.lbl_llamado.config(text=f"TURNO {turno}\nPASE A SERVICIO {num}")
        else:
            messagebox.showwarning("Atención", f"No hay clientes en la cola del Servicio {num}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSeguros(root)
    root.mainloop()