import math
import random
import numpy as np
import matplotlib.pyplot as plt

# =====================================================================
# 1. CRIAR INSTÂNCIA DE TESTE 30x30 (30 CIDADES EM ESPAÇO 2D)
# =====================================================================
np.random.seed(42)
n = 50
P = np.random.uniform(-200, 200, size=(n, 2))
np.savetxt("TSP-50.txt", P, fmt="%.2f")


# =====================================================================
# 2. FUNÇÕES BASE
# =====================================================================
def distance_matrix(n, P):
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = P[i][0] - P[j][0]
            dy = P[i][1] - P[j][1]
            D[i][j] = math.sqrt(dx * dx + dy * dy)
    return D


def objective_function_tsp(n, route, D):
    dist = 0.0
    for i in range(n - 1):
        dist += D[route[i]][route[i + 1]]
    dist += D[route[-1]][route[0]]
    return dist


def plotting_route(n, s, P, title="Rota Final Otimizada - TSP"):
    plt.figure(figsize=(8, 6))
    for i in range(n):
        plt.scatter(P[i][0], P[i][1], color="red", s=50, zorder=3)
        plt.annotate(str(i), (P[i][0] + 3, P[i][1] + 3),
                     fontsize=9, color="black", zorder=4)
    for i in range(n - 1):
        x = [P[s[i]][0], P[s[i + 1]][0]]
        y = [P[s[i]][1], P[s[i + 1]][1]]
        plt.plot(x, y, color="blue", linewidth=1.5, zorder=2)
    x_close = [P[s[-1]][0], P[s[0]][0]]
    y_close = [P[s[-1]][1], P[s[0]][1]]
    plt.plot(x_close, y_close, color="blue", linewidth=1.5, zorder=2)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.show()


# =====================================================================
# 3. ANT COLONY SYSTEM (ACS) PURO - DORIGO & GAMBARDELLA
# =====================================================================
D = distance_matrix(n, P)

eta = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            eta[i][j] = 1.0 / D[i][j]

# Parâmetros ACS
num_ants = 10
beta = 2.0
q0 = 0.9
alpha = 0.1
rho = 0.1
max_iter = 100

# tau_0: estimativa simples (ACS puro, sem vizinho mais próximo)
lado_medio = 400.0 / math.sqrt(n)
tau_0 = 1.0 / (n * n * lado_medio)
tau = np.full((n, n), tau_0)

best_solution_found = np.zeros(max_iter)
s_best_global = None
f_best_global = float("inf")

# Rastreamento da solução inicial (iteração 1)
s_initial_best = None
f_initial_best = float("inf")

for iter_idx in range(max_iter):
    start_nodes = np.random.choice(n, size=num_ants, replace=True)
    ant_routes = [[start_nodes[k]] for k in range(num_ants)]

    for step in range(n - 1):
        for k in range(num_ants):
            r = ant_routes[k][-1]
            unvisited = [u for u in range(n) if u not in ant_routes[k]]

            q = random.random()
            if q <= q0:
                s = max(unvisited, key=lambda u: tau[r][u] * (eta[r][u] ** beta))
            else:
                probs = [tau[r][u] * (eta[r][u] ** beta) for u in unvisited]
                sum_probs = sum(probs)
                probs = [p / sum_probs for p in probs]
                s = np.random.choice(unvisited, p=probs)

            ant_routes[k].append(s)

            tau[r][s] = (1.0 - rho) * tau[r][s] + rho * tau_0
            tau[s][r] = tau[r][s]

    for k in range(num_ants):
        route = ant_routes[k]
        cost = objective_function_tsp(n, route, D)
        if cost < f_best_global:
            f_best_global = cost
            s_best_global = list(route)

    # Guarda a melhor solução da primeira iteração (população inicial)
    if iter_idx == 0:
        s_initial_best = list(s_best_global)
        f_initial_best = f_best_global
        print(f"Melhor Solução da População Inicial (Iteração 1): {f_initial_best:.2f}")

    # Atualização global do feromônio (apenas melhor rota)
    for i in range(n - 1):
        r, s = s_best_global[i], s_best_global[i + 1]
        tau[r][s] = (1.0 - alpha) * tau[r][s] + alpha * (1.0 / f_best_global)
        tau[s][r] = tau[r][s]
    r, s = s_best_global[-1], s_best_global[0]
    tau[r][s] = (1.0 - alpha) * tau[r][s] + alpha * (1.0 / f_best_global)
    tau[s][r] = tau[r][s]

    best_solution_found[iter_idx] = f_best_global

print(f"Custo final após ACS puro: {f_best_global:.2f}")

# =====================================================================
# 4. EXIBIÇÃO DOS RESULTADOS
# =====================================================================
# 1. Convergência
plt.figure(figsize=(8, 4))
plt.plot(best_solution_found, color="green", label="Melhor valor encontrado")
plt.xlabel("Iterações")
plt.ylabel("Distância Total (Custo)")
plt.title("Convergência do Ant Colony System (ACS) - TSP 50x50")
plt.legend()
plt.grid(True)
plt.show()

# 2. Rota inicial (iteração 1)
plotting_route(n, s_initial_best, P,
               title=f"Melhor Rota Inicial (Iteração 1) - Custo: {f_initial_best:.2f}")

# 3. Rota final (ACS puro)
plotting_route(n, s_best_global, P,
               title=f"Rota Final - Custo: {f_best_global:.2f}")