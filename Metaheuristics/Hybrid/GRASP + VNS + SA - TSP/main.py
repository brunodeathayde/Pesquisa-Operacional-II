import matplotlib.pyplot as plt
import random
import math
import numpy as np

from grasp_vns_sa_operators import(
    tsp_reading,
    distance_matrix,
    construction_phase_tsp,
    node_insertion,
    node_exchange,
    node_series_exchange,
    node_series_move_one,
    node_series_move_two,
    node_shift,
    objective_function_tsp,
    two_opt_best_improvement,
    plotting_route
)

# Lista de vizinhanças
neighborhoods = [
    node_exchange,
    node_insertion,
    node_series_exchange,
    node_series_move_one,
    node_series_move_two,
    node_shift
]

# Leitura da instância
file_name = "TSP-2.txt"
P = tsp_reading(file_name)
n = len(P)
D = distance_matrix(n, P)

# Parâmetros GRASP, SA 
T_0 = 1000
T_f = 0.01
alpha = 0.95
max_iter = 1000
alpha_grasp = 0.3

# Parâmetro de reinicialização 
max_no_improve = int(0.05 * max_iter)  # reiniciar após iterações sem melhoria
no_improve = 0                         # contador

# Inicialização com GRASP 
s_0 = construction_phase_tsp(alpha_grasp, D)
f_0 = objective_function_tsp(n, s_0, D)

s_best = s_0[:]
f_best = f_0
best_solution_found = np.zeros(max_iter+1)
best_solution_found[0] = f_0

print("Initial solution cost (GRASP):", f_0)

T = T_0
num_iter = 0

# GRASP + SA + VNS loop 
while num_iter < max_iter:

    improvement_this_iter = False

    order = random.sample(range(len(neighborhoods)), len(neighborhoods))
    
    for nh in order:
        move = neighborhoods[nh]

        s_1 = move(s_0[:])
        f_1 = objective_function_tsp(n, s_1, D)

        # critério de aceitação SA
        if (f_1 < f_0) or (random.random() < math.exp((f_0 - f_1) / T)):
            s_0, f_0 = s_1, f_1

            # refinamento com 2-opt
            s_0, f_0 = two_opt_best_improvement(n, s_0, f_0, D)

        # atualizar melhor global
        if f_0 < f_best:
            s_best, f_best = s_0[:], f_0
            improvement_this_iter = True

    # Atualiza contador de não melhoria
    if improvement_this_iter:
        no_improve = 0
    else:
        no_improve += 1

    # Restart
    if no_improve >= max_no_improve:
        print("Reinicialização na iteração ", num_iter)

        s_0 = construction_phase_tsp(alpha_grasp, D)
        f_0 = objective_function_tsp(n, s_0, D)
        T = T_0          # reset temperatura
        no_improve = 0   # zera contador

    # registrar evolução
    best_solution_found[num_iter + 1] = f_best
    
    # resfriamento
    T = alpha * T
    if T < T_f:
        T = T_f

    num_iter += 1

# Resultado final
print("\nBest solution found:", f_best)

# Gráfico com a evolução da melhor solução
plt.figure(figsize=(8,5))
plt.plot(best_solution_found, label="Best solution")
plt.xlabel('Iterations')
plt.ylabel('Objective function value')
plt.title('GRASP + VNS + SA (com reinicialização)')
plt.legend()
plt.grid(True)
plt.show()

# Rota final
plotting_route(n, s_best, P)
