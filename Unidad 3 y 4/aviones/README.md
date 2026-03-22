# ✈️ Sistema de Gestión de Vuelos en Aeropuerto

Un sistema completo de gestión de operaciones aeroportuarias utilizando **Colas Circulares** como estructura de datos principal para optimizar la asignación de pistas de despegue y aterrizaje.

## 📋 Descripción del Proyecto

Este proyecto implementa una simulación de aeropuerto que maneja:

- **Colas Circulares** para gestionar vuelos en pistas de despegue y aterrizaje
- **Lista de Espera (Bicolas)** para vuelos en espera de asignación
- **Interfaz Gráfica** con Tkinter para visualizar operaciones en tiempo real
- **Simulación automática** de llegadas y salidas de vuelos

## 🏗️ Estructura del Proyecto

```
Aviones-Proyecto/
├── V1/                          # Versión inicial
│   ├── backend.py              # Lógica de negocio V1
│   └── EJER1 - Colas, Bicolas.py
│
├── V2/                          # Versión mejorada
│   ├── backend.py              # Lógica de negocio V2
│   └── EJER1 - Colas, Bicolas.py
│
└── README.md                    # Este archivo
```

## 🎯 Características Principales

### Backend (`backend.py`)

- **ColaCircular**: Implementación de cola circular para gestión de pistas
  - Métodos: `encolar()`, `desencolar()`, `esta_llena()`, `esta_vacia()`
  - Capacidad configurable
  - Gestión automática del índice circular

- **AeropuertoManager**: Orquestador de operaciones
  - Manejo de múltiples pistas de despegue y aterrizaje
  - Control de lista de espera
  - Generación de vuelos simulados

### Frontend (`EJER1 - Colas, Bicolas.py`)

- **VentanaAeropuerto**: Interfaz gráfica con Tkinter
  - Visualización en tiempo real de pistas
  - Panel de control para operaciones
  - Simulación automática de vuelos
  - Paleta de colores moderna (tema oscuro)

## 🚀 Cómo Usar

### Requisitos

- Python 3.9+
- tkinter (incluido en Python)

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Aviones-Proyecto.git
cd Aviones-Proyecto

# Ejecutar la aplicación (V2 - versión mejorada)
cd V2
python "EJER1 - Colas, Bicolas.py"
```

## 📊 Estructura de Datos

### Cola Circular

```python
class ColaCircular:
    capacidad: int           # Capacidad máxima
    nombre: str             # Identificador de la pista
    datos: list             # Array de vuelos
    frente: int             # Índice del primer elemento
    final: int              # Índice del próximo elemento a insertar
    tamaño: int             # Cantidad de elementos actuales
```

### Operaciones

- **Encolar (Enqueue)**: O(1) - Agregar vuelo a la pista
- **Desencolar (Dequeue)**: O(1) - Permitir despegue/aterrizaje
- **Consultar siguiente**: O(1) - Ver próximo vuelo a procesar
- **Operaciones**: está_llena, está_vacía

## 🎨 Interfaz Visual

La aplicación utiliza:
- Tema oscuro inspirado en GitHub
- Código de colores para estados:
  - 🔴 Rojo: Pista ocupada
  - 🟢 Verde: Pista disponible
  - 🟡 Amarillo: En espera
  - 🔵 Azul: Acción/Selección

## 📈 Versiones

- **V1**: Versión inicial con implementación básica
- **V2**: Versión mejorada con optimizaciones y mejor interfaz

## 🔄 Diferencias entre V1 y V2

| Aspecto | V1 | V2 |
|--------|----|----|
| Funcionalidad Base | ✅ | ✅ Optimizada |
| Interfaz | Básica | Mejorada |
| Simulación | Manual | Automática |
| Manejo de Errores | Básico | Completo |

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+**
- **Tkinter** - Interfaz gráfica
- **Threading** - Simulación concurrente
- **Estructuras de Datos** - Colas circulares y bicolas

## 📝 Conceptos de Programación

Este proyecto implementa y demuestra:

- ✅ Estructuras de datos lineales
- ✅ Colas circulares (Circular Queues)
- ✅ Bicolas (Double-ended Queues)
- ✅ Programación orientada a objetos (POO)
- ✅ Interfaz gráfica (GUI)
- ✅ Programación concurrente con threads
- ✅ Simulación de sistemas reales

## � Autores

- Edwin Geovanni Un Uicab
- Adrian Enrique Yama Uitz
- José Armando Jimenez Vicente
- Jarol Gael Lizama Chan

## 📄 Licencia

Este proyecto es de uso educativo.

## 💡 Posibles Mejoras

- [ ] Persistencia de datos en base de datos
- [ ] API REST para integración con otros sistemas
- [ ] Estadísticas y reportes de operaciones
- [ ] Configuración de parámetros desde archivo
- [ ] Pruebas unitarias automatizadas
- [ ] Documentación de API

---

**¡Úsalo como referencia para aprender sobre estructuras de datos y programación en Python!** 🚀
