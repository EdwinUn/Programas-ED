def kruskal(n, aristas):
    aristas.sort(key=lambda x: x[2]) # Ordenar por peso
    padre = list(range(n))
    
    def encontrar(i):
        if padre[i] == i: return i
        return encontrar(padre[i])

    mst = []
    for u, v, peso in aristas:
        raiz_u = encontrar(u)
        raiz_v = encontrar(v)
        if raiz_u != raiz_v:
            mst.append((u, v, peso))
            padre[raiz_u] = raiz_v
    return mst

# (nodo1, nodo2, peso)
conexiones = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
print(kruskal(4, conexiones))