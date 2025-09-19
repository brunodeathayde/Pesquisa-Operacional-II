import numpy as np
from route_distance import route_distance

def nearest_neighbor_tsp(n, D):
    unvisited = list(range(n))
    
    # ponto inicial aleatório
    start = np.random.choice(unvisited)
    route = [start]
    unvisited.remove(start)
    
    current = start
    while unvisited:
        # encontra o vizinho mais próximo
        next_node = min(unvisited, key=lambda city: D[current][city])
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
    
    # calcula a distância total
    total_dist = route_distance(route, D)
    
    return route, total_dist
