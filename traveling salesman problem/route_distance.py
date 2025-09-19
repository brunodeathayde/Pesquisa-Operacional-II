import numpy as np

def route_distance(route, D):
    dist = 0
    for i in range(len(route) - 1):
        dist += D[route[i]][route[i+1]]
    # fechar o ciclo (voltar para o início)
    dist += D[route[-1]][route[0]]
    return dist