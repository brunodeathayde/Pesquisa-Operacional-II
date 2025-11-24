
import matplotlib.pyplot as plt
import random
import math
import numpy as np

from random_initial_solution_tsp import random_initial_solution_tsp
from tsp_reading import tsp_reading
from distance_matrix import distance_matrix
from objective_function_tsp import objective_function_tsp
from swap_permutation import swap_permutation
from plotting_route import plotting_route
from two_opt_best_improvement import two_opt_best_improvement

# Input
file_name = "TSP-1.txt"
P = tsp_reading(file_name)
n = len(P)
D = distance_matrix(n, P)

# Parameters
T_0 = 1000          # temperatura inicial
T_f = 0.01          # temperatura mínima
alpha = 0.95        # fator de resfriamento
max_iter = 10000    # número máximo de iterações

# Initial setting
best_solution_found = np.zeros(max_iter)
T = T_0
s_0 = random_initial_solution_tsp(n)
f_0 = objective_function_tsp(n, s_0, D)
num_iter = 0
s_best = s_0
f_best = f_0

print("Initial solution: {:.2f}".format(f_best))

while num_iter < max_iter:
    # gera vizinho
    s_1 = swap_permutation(s_0, n)
    # avalia vizinho
    f_1 = objective_function_tsp(n, s_1, D)

    # critério de aceitação
    if (f_1 < f_0) or (random.random() < math.exp((f_0 - f_1) / T)):
        s_0, f_0 = s_1, f_1

    # atualiza melhor global
    if f_0 < f_best:
        f_best = f_0
        s_best = s_0
        

    # resfriamento clássico
    T = alpha * T
    if T < T_f:
        T = T_f

    best_solution_found[num_iter] = f_best
    num_iter += 1

# refinamento final com two-opt
s_best, f_best = two_opt_best_improvement(n, s_best, f_best, D)

print("Best solution: {:.2f}".format(abs(f_best)))

# Plotar o gráfico com a evolução do fitness
plt.figure(figsize=(8,5))
plt.plot(best_solution_found, label="Best solution")
plt.xlabel('Iterations')
plt.ylabel('Objective function value')
plt.title('Simulated Annealing - TSP')
plt.legend()
plt.grid(True)
plt.savefig("best_solutions.jpg")
plt.show()

# Plotar rota final
plotting_route(n, s_best, P)
