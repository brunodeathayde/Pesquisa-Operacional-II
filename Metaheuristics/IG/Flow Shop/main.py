from scheptk.scheptk import FlowShop
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import math
import copy

from ig_operators import (
    EDD,
    tardiness,
    construction,
    destruction,
    calculate_temperature,
    NEH,
    two_opt_best_improvement
)

elapsed = 0
t0 = time.time()

# ----------------------------------------------------------------------
# Leitura da instância
# ----------------------------------------------------------------------
instance = FlowShop('instance.txt')
N = instance.jobs
M = instance.machines
P = np.array(instance.pt)   # garante NumPy
d = instance.dd

# ----------------------------------------------------------------------
# Parâmetros
# ----------------------------------------------------------------------
alpha = 0.99
k_destruction = 4
time_limit = 5  # segundos

# Temperatura inicial
T = calculate_temperature(P, alpha)

# ----------------------------------------------------------------------
# Solução inicial via EDD + NEH
# ----------------------------------------------------------------------
Pi = EDD(d)
best_tardiness = tardiness(Pi, P, d, M, N)
print("Tardiness - EDD:", best_tardiness)

# Refinando via NEH 
current_pi, current_tardiness = NEH(Pi, P, d, M, N, tardiness)

best_tardiness = current_tardiness
best_pi = copy.deepcopy(current_pi)

print("Melhor sequência inicial:", best_pi)
print("Tardiness NEH:", best_tardiness)

best_solution_found = []

# ----------------------------------------------------------------------
# Loop principal (Simulated Annealing)
# ----------------------------------------------------------------------
while elapsed <= time_limit:

    # Fase de destruição
    pi_D, pi_P = destruction(current_pi, k_destruction)

    # Fase de construção
    new_pi, new_tardiness = construction(
        pi_D, pi_P, M, N, P, d, tardiness
    )

    # Busca local 2-opt
    new_pi, new_tardiness = two_opt_best_improvement(
        new_pi, new_tardiness, P, M, N, d
    )

    # Critério de aceitação
    if new_tardiness < current_tardiness:
        current_pi = copy.deepcopy(new_pi)
        current_tardiness = new_tardiness
    else:
        # Probabilidade de Metropolis
        RN = random.random()
        A = math.exp(-(new_tardiness - current_tardiness) / T)
        if RN < A:
            current_pi = new_pi
            current_tardiness = new_tardiness

    # Atualiza melhor solução global
    if current_tardiness < best_tardiness:
        best_tardiness = current_tardiness
        best_pi = copy.deepcopy(current_pi)

    # Atualiza tempo
    elapsed = time.time() - t0
    best_solution_found.append(best_tardiness)

# ----------------------------------------------------------------------
# Resultado final
# ----------------------------------------------------------------------
print("Melhor sequência encontrada:", best_pi)
print("Melhor tardiness encontrado:", best_tardiness)

plt.plot(best_solution_found)
plt.xlabel('Iteração')
plt.ylabel('Tardiness')
plt.grid(True)
plt.show()

instance.print_schedule(best_pi, 'Tardiness.png')
