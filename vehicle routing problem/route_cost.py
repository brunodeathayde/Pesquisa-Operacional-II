import numpy as np

import numpy as np

def route_cost(route, P, capacity):
    dist = 0.0
    carga = 0
    atual = 0  # começa na origem (0,0)

    for ponto in route:
        demanda = P[ponto - 1][2]  # demanda está na terceira coluna
        if carga + demanda > capacity:
            # retorna ao depósito
            if atual != 0:
                xa, ya = P[atual - 1][0], P[atual - 1][1]
                dist += np.hypot(xa, ya)
            # vai do depósito ao novo ponto
            xb, yb = P[ponto - 1][0], P[ponto - 1][1]
            dist += np.hypot(xb, yb)
            carga = demanda
        else:
            if atual == 0:
                xa, ya = 0, 0
            else:
                xa, ya = P[atual - 1][0], P[atual - 1][1]
            xb, yb = P[ponto - 1][0], P[ponto - 1][1]
            dist += np.hypot(xa - xb, ya - yb)
            carga += demanda
        atual = ponto

    # retorno final ao depósito
    xa, ya = P[atual - 1][0], P[atual - 1][1]
    dist += np.hypot(xa, ya)
    return dist
