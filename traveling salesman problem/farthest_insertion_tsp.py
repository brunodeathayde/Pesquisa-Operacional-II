import numpy as np
from route_distance import route_distance

def farthest_insertion_tsp(n, D):
    # Passo 1: encontra os dois nós mais distantes
    max_dist = -1
    i0, j0 = 0, 1
    for i in range(n):
        for j in range(i + 1, n):
            if D[i][j] > max_dist:
                max_dist = D[i][j]
                i0, j0 = i, j

    route = [i0, j0]  # rota inicial com dois nós
    unvisited = [k for k in range(n) if k not in route]

    # Passo 2: inserir nós restantes
    while unvisited:
        # encontra o nó mais distante da rota atual
        farthest_node = max(unvisited, key=lambda u: min(D[u][v] for v in route))

        # encontra a posição de inserção que minimiza o aumento do custo
        best_pos, best_increase = None, float("inf")
        for i in range(len(route)):
            j = (i + 1) % len(route)
            increase = (D[route[i]][farthest_node] +
                        D[farthest_node][route[j]] -
                        D[route[i]][route[j]])
            if increase < best_increase:
                best_increase = increase
                best_pos = j

        # insere o nó na melhor posição
        route.insert(best_pos, farthest_node)
        unvisited.remove(farthest_node)

    # calcula a distância total
    total_dist = route_distance(route, D)

    return route, total_dist
