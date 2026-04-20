import heapq

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    prioridad = [(0, inicio)]
    
    while prioridad:
        distancia_actual, nodo_actual = heapq.heappop(prioridad)
        
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(prioridad, (distancia, vecino))
    return distancias

# Ejemplo de uso
red = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 5, 'D': 10},
    'C': {'D': 3},
    'D': {}
}
print(dijkstra(red, 'A'))