def floyd_warshall(matriz):
    n = len(matriz)
    dist = list(map(lambda i: list(map(lambda j: j, i)), matriz))
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

# INF representa que no hay conexión directa
INF = 999
grafo_matriz = [
    [0, 5, INF, 10],
    [INF, 0, 3, INF],
    [INF, INF, 0, 1],
    [INF, INF, INF, 0]
]
print(floyd_warshall(grafo_matriz))