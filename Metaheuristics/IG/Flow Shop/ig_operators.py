import random
import numpy as np
import copy
import math

# -----------------------------
# Earliest Due Date (EDD)
# -----------------------------
def EDD(d):
    # retorna os índices que ordenam o vetor d em ordem crescente
    pi = sorted(range(len(d)), key=lambda i: d[i])
    return pi

# -----------------------------
# Construction operator
# -----------------------------
def construction(pi_D, pi_P, M, N, P, d, objective_fn):
    best_Pi = []
    best_tardiness = float("inf")
    best_position = 0
    best_value = 0

    # loop sobre cada job em pi_D
    for k in range(len(pi_D)):
        best_tardiness = float("inf")

        # testar todas as posições possíveis na sequência parcial
        for l in range(len(pi_P) + 1):
            pi_P.insert(l, pi_D[k])  # insere temporariamente
            current_tardiness = objective_fn(pi_P, P, d, M, len(pi_P))

            if current_tardiness < best_tardiness:
                best_tardiness = current_tardiness
                best_Pi = pi_P.copy()
                best_position = l
                best_value = pi_D[k]

            # remover inserção temporária
            pi_P.pop(l)

        # insere na melhor posição encontrada
        pi_P.insert(best_position, best_value)

    # calcula o valor final da função objetivo
    best_tardiness = objective_fn(pi_P, P, d, M, N)
    return pi_P, best_tardiness


# -----------------------------
# Destruction operator
# -----------------------------
def destruction(pi_0, k_destruction):
    pi_D = random.sample(pi_0, k_destruction)
    pi_P = [x for x in pi_0 if x not in pi_D]
    return pi_D, pi_P


# -----------------------------
# Temperature calculation
# -----------------------------
def calculate_temperature(P, tal):
    m = len(P)          # número de linhas
    n = len(P[0])       # número de colunas
    total = sum(sum(row) for row in P)
    T = tal * (total / (10 * m * n))
    return T


# -----------------------------
# Tardiness function
# -----------------------------
def tardiness(Pi, P, d, M, N):
    F = np.zeros((M, N), dtype=int)
    C = np.zeros(N, dtype=int)
    T = np.zeros(N, dtype=int)

    for i in range(M):
        for k in range(N):
            job = Pi[k]
            if i == 0:
                if k == 0:
                    F[i, k] = P[i, job]
                else:
                    F[i, k] = F[i, k-1] + P[i, job]
            else:
                if k == 0:
                    F[i, k] = F[i-1, k] + P[i, job]
                else:
                    F[i, k] = max(F[i-1, k], F[i, k-1]) + P[i, job]

    for j in range(N):
        C[j] = F[M-1, j]
        T[j] = abs(C[j] - d[Pi[j]])

    return np.sum(T)


# -----------------------------
# NEH heuristic
# -----------------------------
def NEH(alpha, P, d, M, N, objective_fn):
    Pi = [alpha[0]]
    best_Pi = []
    best_tardiness = float("inf")
    best_position = 0
    best_value = 0

    for k in range(1, len(alpha)):
        best_tardiness = float("inf")

        for l in range(len(Pi) + 1):
            Pi.insert(l, alpha[k])
            current_tardiness = objective_fn(Pi, P, d, M, len(Pi))

            if current_tardiness < best_tardiness:
                best_tardiness = current_tardiness
                best_Pi = copy.deepcopy(Pi)
                best_position = l
                best_value = alpha[k]

            Pi.pop(l)

        Pi.insert(best_position, best_value)

    ET = objective_fn(Pi, P, d, M, N)
    return Pi, ET

# -----------------------------
# Busca local 2-opt
# -----------------------------
def two_opt_best_improvement(Pi, best_tardiness, P, M, N, d):
    for i in range(0, N-1):       
        for j in range(1, N):     
            # troca
            Pi[i], Pi[j] = Pi[j], Pi[i]

            TT = tardiness(Pi, P, d, M, N)

            if TT < best_tardiness:
                best_tardiness = TT
                
            else:
                # desfaz troca
                Pi[j], Pi[i] = Pi[i], Pi[j]

    return Pi, best_tardiness

