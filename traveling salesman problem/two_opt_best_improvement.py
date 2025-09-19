def route_distance(route, D):
    """Distância total (ciclo fechado)."""
    n = len(route)
    dist = 0.0
    for k in range(n):
        i = route[k]
        j = route[(k + 1) % n]
        dist += D[i][j]
    return dist


def two_opt_best_improvement(route, best_dist, D, tol=1e-12):
    """
    2-opt clássico (best-improvement).
    route: lista de cidades (índices)
    best_dist: distância total da rota
    D: matriz de distâncias
    retorna: (rota_melhorada, distancia_melhorada)
    """
    n = len(route)
    if n <= 3:
        return route.copy(), best_dist

    route = route.copy()

    for i in range(n - 1):
        for j in range(i + 2, n):  # garante não pegar arestas adjacentes
            if i == 0 and j == n - 1:
                continue  # não mexe na aresta de fechamento

            # custo antes
            a, b = route[i], route[i + 1]
            c, d = route[j], route[(j + 1) % n]

            old_cost = D[a][b] + D[c][d]
            new_cost = D[a][c] + D[b][d]

            new_dist = best_dist - old_cost + new_cost

            if new_dist < best_dist - tol:
                # aplica a reversão do subcaminho
                route[i + 1 : j + 1] = reversed(route[i + 1 : j + 1])
                best_dist = new_dist

    return route, best_dist
