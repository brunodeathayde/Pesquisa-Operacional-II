def two_opt_best_improvement(n, route, best_dist, D):
    route = list(route)  # garante que é lista
    for i in range(n - 1):
        for j in range(i + 2, n): 
            if i == 0 and j == n - 1:
                continue  
            # custo antes
            a, b = route[i], route[i + 1]
            c, d = route[j], route[(j + 1) % n]
            old_cost = D[a][b] + D[c][d]
            new_cost = D[a][c] + D[b][d]
            new_dist = best_dist - old_cost + new_cost
            if new_dist < best_dist:                
                route[i + 1 : j + 1] = list(reversed(route[i + 1 : j + 1]))
                best_dist = new_dist

    return route, best_dist
