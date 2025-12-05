from scheptk.scheptk import OpenShop
import numpy as np
import matplotlib.pyplot as plt
import random

from vns_operators import (
    job_exchange,
    job_insertion,
    job_series_exchange,
    job_series_move_one,
    job_series_move_two
)

# Leitura da instância
instance = OpenShop('instance.txt')
n = instance.jobs
m = instance.machines

# lista de vizinhanças em Python
neighborhoods = [
    job_exchange,
    job_insertion,
    job_series_move_one,
    job_series_move_two,
    job_series_exchange
]

# Parâmetros
max_iter = 1000

# Solução inicial (pode ser aleatória)
pi = list(range(n * m))
random.shuffle(pi)

cmax = instance.Cmax(pi)
Cmax_best = cmax
pi_best = pi[:]

print("Initial solution makespan:", cmax)

best_solution_found = []
iter_ = 0

# --- início do VNS ---
while iter_ < max_iter:
    iter_ += 1

    # gerar permutação aleatória das vizinhanças
    order = random.sample(range(len(neighborhoods)), len(neighborhoods))

    # executar as vizinhanças na ordem sorteada
    for nh in order:
        move = neighborhoods[nh]
        pi_star = move(pi[:])          # importante copiar
        Cmax_star = instance.Cmax(pi_star)

        # --- aceita melhoria ---
        if Cmax_star < cmax:
            pi = pi_star[:]
            cmax = Cmax_star

        # update global best
        if cmax < Cmax_best:
            pi_best = pi[:]
            Cmax_best = cmax
        break  # first improvement
    best_solution_found.append(Cmax_best)

# Resultado final
print("Best solution found:", Cmax_best)
plt.plot(best_solution_found, color='blue')
plt.xlabel('Iteração')
plt.ylabel('Makespan')
plt.grid(True)
plt.show()

instance.print_schedule(pi_best, 'Makespan.png')
