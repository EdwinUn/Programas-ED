def warshall(matriz):
    n = len(matriz)
    clausura = [fila[:] for fila in matriz]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                clausura[i][j] = clausura[i][j] or (clausura[i][k] and clausura[k][j])
    return clausura

# 1 si hay conexión, 0 si no
grafo_binario = [
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 0, 1, 0]
]
print(warshall(grafo_binario))