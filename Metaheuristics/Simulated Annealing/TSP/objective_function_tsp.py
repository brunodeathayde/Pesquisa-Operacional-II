def objective_function_tsp(n, route, D):
    dist = 0
    for i in range(n-1):
        dist += D[route[i]][route[i+1]]
    dist += D[route[-1]][route[0]]  # fecha o ciclo
    return dist
