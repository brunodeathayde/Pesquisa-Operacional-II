# =====================================================================
# SIMULATED ANNEALING PARA O CCP - VERSÃO COLAB (instância maior)
# =====================================================================

import matplotlib.pyplot as plt
import random
import math
import numpy as np

# =====================================================================
# 1. GERAÇÃO DA INSTÂNCIA
# =====================================================================
def ccp_generation(n=200, p=10, seed=42, tightness=0.85):
    rng = np.random.default_rng(seed)
    coords = rng.uniform(1, 100, size=(n, 2))
    demands = rng.uniform(1, 20, size=n)
    Q = demands.sum() / (p * tightness)
    return coords, demands, p, Q


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


def objective_function_ccp(n, solution, centers, D):
    cost = 0.0
    for k in range(n):
        cost += D[k][centers[solution[k]]]
    return cost


def cluster_loads(n, solution, demands, p):
    load = [0.0] * p
    for k in range(n):
        load[solution[k]] += demands[k]
    return load


# =====================================================================
# 3. HEURÍSTICA CONSTRUTIVA (FIND → ASSIGN → RE-COMPUTE)
# =====================================================================
def constructive_heuristic_ccp(n, p, Q, demands, D):
    max_d, a, b = -1.0, 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            if D[i][j] > max_d:
                max_d, a, b = D[i][j], i, j
    centers = [a, b]

    while len(centers) < p:
        best_k, best_prod = -1, -1.0
        for k in range(n):
            if k in centers:
                continue
            prod = 1.0
            for c in centers:
                prod *= D[k][c]
            if prod > best_prod:
                best_prod, best_k = prod, k
        centers.append(best_k)

    capacity_left = [Q] * p
    solution = [-1] * n

    order = sorted(
        [k for k in range(n) if k not in centers],
        key=lambda k: min(D[k][c] for c in centers)
    )

    for k in order:
        sorted_centers = sorted(range(p), key=lambda c: D[k][centers[c]])
        assigned = False
        for c in sorted_centers:
            if capacity_left[c] >= demands[k]:
                solution[k] = c
                capacity_left[c] -= demands[k]
                assigned = True
                break
        if not assigned:
            solution[k] = sorted_centers[0]
            capacity_left[sorted_centers[0]] -= demands[k]

    for c in range(p):
        solution[centers[c]] = c

    for c in range(p):
        members = [k for k in range(n) if solution[k] == c]
        if not members:
            continue
        best_center, best_sum = members[0], float("inf")
        for m in members:
            s = sum(D[m][k] for k in members)
            if s < best_sum:
                best_sum, best_center = s, m
        centers[c] = best_center

    return solution, centers


# =====================================================================
# 4. VIZINHANÇA λ-INTERCHANGE COM REPARO
# =====================================================================
def recompute_centers(n, solution, centers, affected, D):
    new_centers = list(centers)
    for c in affected:
        members = [k for k in range(n) if solution[k] == c]
        if not members:
            continue
        best_center, best_sum = members[0], float("inf")
        for m in members:
            s = sum(D[m][k] for k in members)
            if s < best_sum:
                best_sum, best_center = s, m
        new_centers[c] = best_center
    return new_centers


def repair_capacity(n, solution, demands, Q, p, preferred_target):
    """
    Se algum cluster excede Q, move clientes excedentes para o cluster
    com maior folga (que não seja o próprio). Retorna solução reparada
    ou None se não for possível.
    """
    sol = list(solution)
    for _ in range(3 * n):
        load = cluster_loads(n, sol, demands, p)
        overloaded = [c for c in range(p) if load[c] > Q + 1e-9]
        if not overloaded:
            return sol

        c = overloaded[0]
        under = [d for d in range(p) if d != c and load[d] < Q]
        if not under:
            return None
        # move o cliente de c com menor "arrependimento" para o cluster com maior folga
        target = max(under, key=lambda d: Q - load[d])
        members = [k for k in range(n) if sol[k] == c]
        # escolhe o cliente de c cuja transferência custa menos (distância ao novo centro)
        k_move = min(members, key=lambda k: abs(demands[k] - (load[c] - Q)))
        sol[k_move] = target
    return None


def lambda_interchange_ccp(n, p, Q, demands, solution, centers, D):
    """
    λ=1 com reparo: sorteia operador (0,1), (1,0) ou (1,1) entre dois clusters.
    Se violar capacidade, tenta reparo; se o reparo for inviável, retorna None.
    """
    if p < 2:
        return None, None

    i, j = random.sample(range(p), 2)
    members_i = [k for k in range(n) if solution[k] == i]
    members_j = [k for k in range(n) if solution[k] == j]

    op = random.choice(["01", "10", "11"])
    new_solution = list(solution)
    affected = (i, j)

    if op == "01" and members_i:
        k = random.choice(members_i)
        new_solution[k] = j
    elif op == "10" and members_j:
        k = random.choice(members_j)
        new_solution[k] = i
    elif op == "11" and members_i and members_j:
        ki = random.choice(members_i)
        kj = random.choice(members_j)
        new_solution[ki] = j
        new_solution[kj] = i
    else:
        return None, None

    # reparo se necessário
    repaired = repair_capacity(n, new_solution, demands, Q, p, preferred_target=j)
    if repaired is None:
        return None, None

    new_centers = recompute_centers(n, repaired, centers, affected, D)
    return repaired, new_centers


# =====================================================================
# 5. PLOTAGEM
# =====================================================================
def plotting_ccp(n, solution, centers, P, title="CCP - Solução"):
    colors = plt.cm.tab20.colors
    plt.figure(figsize=(9, 7))
    for k in range(n):
        c = solution[k]
        plt.scatter(P[k][0], P[k][1], color=colors[c % 20], s=30, zorder=3)
        plt.plot(
            [P[k][0], P[centers[c]][0]],
            [P[k][1], P[centers[c]][1]],
            color=colors[c % 20], linewidth=0.4, alpha=0.4, zorder=1
        )
    for c, center in enumerate(centers):
        plt.scatter(P[center][0], P[center][1], color=colors[c % 20],
                    s=300, marker="*", edgecolor="black", zorder=4)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")
    plt.show()


# =====================================================================
# 6. EXECUÇÃO PRINCIPAL
# =====================================================================
n, p = 200, 10
P, demands, p, Q = ccp_generation(n=n, p=p, seed=42, tightness=0.85)
D = distance_matrix(n, P)

# Parâmetros SA
T_0 = 5000.0
T_f = 0.01
alpha = 0.995          # resfriamento mais lento (mais exploração)
max_iter = 100000

# Solução inicial
s_0, centers_0 = constructive_heuristic_ccp(n, p, Q, demands, D)
f_0 = objective_function_ccp(n, s_0, centers_0, D)

s_best, centers_best, f_best = list(s_0), list(centers_0), f_0
T = T_0
best_solution_found = np.zeros(max_iter)
num_iter = 0
num_viable = 0
num_accepted = 0

print(f"Instância: n={n}, p={p}, Q={Q:.2f}")
print(f"Initial solution: {f_best:.2f}")

while num_iter < max_iter:
    s_1, centers_1 = lambda_interchange_ccp(
        n, p, Q, demands, s_0, centers_0, D
    )

    if s_1 is None:
        best_solution_found[num_iter] = f_best
        num_iter += 1
        continue

    num_viable += 1
    f_1 = objective_function_ccp(n, s_1, centers_1, D)

    if (f_1 < f_0) or (random.random() < math.exp((f_0 - f_1) / T)):
        s_0, centers_0, f_0 = s_1, centers_1, f_1
        num_accepted += 1

    if f_0 < f_best - 1e-9:
        f_best = f_0
        s_best = list(s_0)
        centers_best = list(centers_0)

    T = alpha * T
    if T < T_f:
        T = T_f

    best_solution_found[num_iter] = f_best
    num_iter += 1

print(f"Movimentos viáveis: {num_viable} ({100*num_viable/max_iter:.1f}%)")
print(f"Movimentos aceitos: {num_accepted} ({100*num_accepted/max_iter:.1f}%)")
print(f"Best solution: {f_best:.2f}")

# Convergência
plt.figure(figsize=(8, 5))
plt.plot(best_solution_found, label="Best solution")
plt.xlabel("Iterations")
plt.ylabel("Objective function value")
plt.title("Simulated Annealing - CCP (n=200, p=10)")
plt.legend()
plt.grid(True)
plt.savefig("best_solutions_ccp.jpg")
plt.show()

plotting_ccp(n, s_best, centers_best, P,
             title=f"CCP - Melhor solução (custo {f_best:.2f})")