# ADA2 - Métodos de Ordenamiento 2

## Descripción

**Visualizador interactivo de algoritmos de ordenamiento con interfaz gráfica (tkinter).**

Programa que visualiza 4 métodos de ordenamiento diferentes con **barras animadas** que se reorganizan en tiempo real:

1. **Shell Sort**: Generalización del ordenamiento por inserción con brecha decreciente
2. **Quicksort**: Algoritmo divide y conquista usando pivotes
3. **Heapsort**: Utiliza la estructura de datos heap (montículo)
4. **Radix Sort**: Ordena números dígito por dígito

## Características

✅ **Interfaz Gráfica (GUI)** con tkinter
✅ **Barras Animadas** que se mueven y reorganizan visualmente
✅ **Controles Interactivos**:
   - Seleccionar algoritmo (radio buttons)
   - Cargar números manualmente o generar aleatorios
   - Controlar velocidad de animación
   - Botones: Comenzar, Pausar, Reiniciar

✅ **Visualización Clara**:
   - Barras en azul (sin ordenar)
   - Barras en rojo (siendo comparadas)
   - Barras en verde (ya ordenadas)
   - Valores mostrados en cada barra

✅ **Ejecución en tiempo real** con threading

## Requisitos

```bash
# Solo Python estándar (tkinter viene incluido)
# En caso de necesitar instalarlo:
# Linux: sudo apt-get install python3-tk
# macOS: brew install python-tk
# Windows: Incluido en la instalación de Python
```

## Cómo usar

### Ejecución

```bash
python main.py
```

### Flujo del programa

1. **Cargar Números**: 
   - Click en "Cargar Números"
   - Opción A: Ingresar cantidad y números manualmente
   - Opción B: Generar números aleatorios (especificar rango)

2. **Seleccionar Algoritmo**: 
   - Elegir entre Shell Sort, Quicksort, Heapsort o Radix Sort

3. **Controlar Animación**:
   - "Comenzar": Inicia la animación
   - "Pausa": Pausa la ejecución
   - "Reiniciar": Vuelve al array sin ordenar
   - Deslizador de velocidad: Controla qué tan rápido se anima

4. **Visualización**:
   - Observa las barras moviéndose y reorganizándose
   - El panel de información muestra el paso actual
   - Cuando termina, las barras se ponen verdes

## Colores en la Visualización

| Color | Significado |
|-------|------------|
| 🔵 Azul | Elementos sin ordenar |
| � Amarillo | Elementos siendo comparados (con borde brillante) |
| 🟢 Verde | Elementos ya ordenados |

## Características de Animación

- **Animación suave**: Las barras cambian de forma gradual
- **Indicador de comparación**: Los elementos que se comparan parpadean en amarillo
- **Velocidad controlable**: Ajusta la velocidad en tiempo real con el deslizador
- **Pausa interactiva**: Puedes pausar en cualquier momento para observar

## Algoritmos Implementados

### Shell Sort
- **Complejidad**: O(n log n) promedio, O(n²) peor caso
- **Características**: Generalización de inserción con brecha decreciente
- **Ventaja**: Simple y eficiente para listas medianas

### Quicksort
- **Complejidad**: O(n log n) promedio, O(n²) peor caso
- **Características**: Divide y conquista usando pivote
- **Ventaja**: Muy rápido en la práctica

### Heapsort
- **Complejidad**: O(n log n) garantizado
- **Características**: Utiliza estructura de heap
- **Ventaja**: Garantía de tiempo O(n log n)

### Radix Sort
- **Complejidad**: O(d × n) donde d es el número de dígitos
- **Características**: Ordena por dígitos/posiciones
- **Ventaja**: Muy eficiente para números con dígitos limitados

## Estructura del Proyecto

```
ADA2 - MetOrdenamiento2/
├── main.py                   # Interfaz GUI e interacción
├── sorting_algorithms.py     # Implementación de 4 algoritmos con generadores
└── README.md                 # Este archivo
```

## Características Técnicas

- **Generadores** para animación paso a paso sin bloqueo
- **Threading** para mantener la interfaz responsiva
- **Tema Oscuro** para mejor visualización de las barras
- **Escalable** - el tamaño de las barras se ajusta automáticamente

## Ejemplo de Uso

```
1. Ejecutar: python main.py
2. Click en "Cargar Números"
3. Generar 15 números aleatorios entre 10 y 100
4. Seleccionar "Quicksort"
5. Ajustar velocidad a un nivel cómodo
6. Click en "Comenzar"
7. ¡Observar cómo las barras se organizan!
```

## Notas

- **Radix Sort**: Convierte automáticamente números negativos a positivos
- **Velocidad**: Ajustable en tiempo real mientras se ejecuta
- **Pausar**: Puedes pausar la animación en cualquier momento
- **Reiniciar**: Reinicia el array al estado desordenado original

## Autor

Programa educativo para visualizar y entender métodos de ordenamiento avanzados.

