package ED;

import java.util.Scanner;

public class EjercicioDepartamentoJAVA {
    private String[] meses = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };
    private String[] departamentos = {"Ropa", "Deportes", "Juguetería"};
    private double[][] ventas = new double[12][3]; // 12 meses, 3 departamentos

    // Método para normalizar: quita espacios y pone la primera en mayúscula
    private String normalizar(String texto) {
        if (texto == null || texto.isEmpty()) return "";
        texto = texto.trim().toLowerCase();
        return texto.substring(0, 1).toUpperCase() + texto.substring(1);
    }

    // Buscar el índice de un elemento en un arreglo de Strings
    private int buscarIndice(String[] arreglo, String valor) {
        for (int i = 0; i < arreglo.length; i++) {
            if (arreglo[i].equals(valor)) return i;
        }
        return -1;
    }

    public void mostrarTabla() {
        System.out.println("\nVENTAS ANUALES");
        System.out.printf("%-12s", "Mes");
        for (String d : departamentos) {
            System.out.printf("%-15s", d);
        }
        System.out.println("\n--------------------------------------------------");

        for (int i = 0; i < meses.length; i++) {
            System.out.printf("%-12s", meses[i]);
            for (int j = 0; j < departamentos.length; j++) {
                System.out.printf("%-15s", ventas[i][j]);
            }
            System.out.println();
        }
        System.out.println();
    }

    public void insertarVenta(String mes, String departamento, double monto) {
        mes = normalizar(mes);
        departamento = normalizar(departamento);

        int f = buscarIndice(meses, mes);
        int c = buscarIndice(departamentos, departamento);

        if (f != -1 && c != -1) {
            ventas[f][c] = monto;
            System.out.println("Venta registrada correctamente.");
            mostrarTabla();
        } else {
            System.out.println("Mes o departamento no válido.");
        }
    }

    public void buscarVenta(String mes, String departamento) {
        mes = normalizar(mes);
        departamento = normalizar(departamento);

        int f = buscarIndice(meses, mes);
        int c = buscarIndice(departamentos, departamento);

        if (f != -1 && c != -1) {
            System.out.println("Venta encontrada: $" + ventas[f][c]);
        } else {
            System.out.println("Dato inválido.");
        }
    }

    public void eliminarVenta(String mes, String departamento) {
        mes = normalizar(mes);
        departamento = normalizar(departamento);

        int f = buscarIndice(meses, mes);
        int c = buscarIndice(departamentos, departamento);

        if (f != -1 && c != -1) {
            ventas[f][c] = 0;
            System.out.println("Venta eliminada.");
            mostrarTabla();
        } else {
            System.out.println("Dato inválido.");
        }
    }

// -------- MÉTODO MAIN (EL MINI SISTEMA) --------
    public static void main(String[] args) {
       
        EjercicioDepartamentoJAVA tienda = new EjercicioDepartamentoJAVA(); 
        
        Scanner sc = new Scanner(System.in);
        String opcion;

        while (true) {
            System.out.println("\n===== SISTEMA DE VENTAS =====");
            System.out.println("1. Insertar venta");
            System.out.println("2. Buscar venta");
            System.out.println("3. Eliminar venta");
            System.out.println("4. Mostrar tabla");
            System.out.println("5. Salir");
            System.out.print("Elige una opción: ");
            opcion = sc.nextLine();

            if (opcion.equals("5")) {
                System.out.println("Saliendo del sistema...");
                break;
            }

            String m, d;
            switch (opcion) {
                case "1":
                    System.out.print("Mes: ");
                    m = sc.nextLine();
                    System.out.print("Departamento (Ropa, Deportes, Juguetería): ");
                    d = sc.nextLine();
                    System.out.print("Monto de venta: ");
                    double monto = Double.parseDouble(sc.nextLine());
                    tienda.insertarVenta(m, d, monto);
                    break;
                case "2":
                    System.out.print("Mes: ");
                    m = sc.nextLine();
                    System.out.print("Departamento: ");
                    d = sc.nextLine();
                    tienda.buscarVenta(m, d);
                    break;
                case "3":
                    System.out.print("Mes: ");
                    m = sc.nextLine();
                    System.out.print("Departamento: ");
                    d = sc.nextLine();
                    tienda.eliminarVenta(m, d);
                    break;
                case "4":
                    tienda.mostrarTabla();
                    break;
                default:
                    System.out.println("Opción inválida.");
            }
        }
        sc.close();
    }
}