class Tienda:
    def __init__(self):
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        self.ventas = [[0 for _ in self.departamentos] for _ in self.meses]

    def normalizar(self, texto):
        return texto.strip().capitalize()

    def mostrar_tabla(self):
        print("\nVENTAS ANUALES")
        print("Mes".ljust(12), end="")
        for d in self.departamentos:
            print(d.ljust(15), end="")
        print("\n" + "-"*50)

        for i, mes in enumerate(self.meses):
            print(mes.ljust(12), end="")
            for venta in self.ventas[i]:
                print(str(venta).ljust(15), end="")
            print()
        print()

    def insertar_venta(self, mes, departamento, monto):
        mes = self.normalizar(mes)
        departamento = self.normalizar(departamento)

        if mes in self.meses and departamento in self.departamentos:
            f = self.meses.index(mes)
            c = self.departamentos.index(departamento)
            self.ventas[f][c] = monto
            print("Venta registrada correctamente.")
            self.mostrar_tabla()  # ← AHORA SE VE EL CAMBIO
        else:
            print("Mes o departamento no válido.")

    def buscar_venta(self, mes, departamento):
        mes = self.normalizar(mes)
        departamento = self.normalizar(departamento)

        if mes in self.meses and departamento in self.departamentos:
            f = self.meses.index(mes)
            c = self.departamentos.index(departamento)
            print(f"Venta encontrada: ${self.ventas[f][c]}")
        else:
            print("Dato inválido.")

    def eliminar_venta(self, mes, departamento):
        mes = self.normalizar(mes)
        departamento = self.normalizar(departamento)

        if mes in self.meses and departamento in self.departamentos:
            f = self.meses.index(mes)
            c = self.departamentos.index(departamento)
            self.ventas[f][c] = 0
            print("Venta eliminada.")
            self.mostrar_tabla()
        else:
            print("Dato inválido.")

# -------- MINI SISTEMA --------

tienda = Tienda()

while True:
    print("\n===== SISTEMA DE VENTAS =====")
    print("1. Insertar venta")
    print("2. Buscar venta")
    print("3. Eliminar venta")
    print("4. Mostrar tabla")
    print("5. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        mes = input("Mes: ")
        dep = input("Departamento (Ropa, Deportes, Juguetería): ")
        monto = float(input("Monto de venta: "))
        tienda.insertar_venta(mes, dep, monto)

    elif opcion == "2":
        mes = input("Mes: ")
        dep = input("Departamento: ")
        tienda.buscar_venta(mes, dep)

    elif opcion == "3":
        mes = input("Mes: ")
        dep = input("Departamento: ")
        tienda.eliminar_venta(mes, dep)

    elif opcion == "4":
        tienda.mostrar_tabla()

    elif opcion == "5":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción inválida.")


