import numpy as np
import matplotlib.pyplot as plt
from ovrp_reading import ovrp_reading

from grasp_operators import (
    distance_matrix,
    construction_phase,
    cost_solution,
    plot_routes,
    reallocation,
    swap,
    two_opt_route
)

# Dados de entrada
# capacidade   : capacidade dos veículos (frota homogênea)
# depot        : coordenadas do depósito (origem dos veículos)
# delivery     : coordenadas do ponto de entrega final
# clients      : coordenadas e demanda dos clientes
# demands      : vetor com as demandas dos clientes
# dist_matrix  : matriz de distâncias euclidianas entre depósito, entrega e clientes
capacidade = 20
depot, delivery, clients = ovrp_reading("OVRP-1.txt")
demands = clients[:, 2]
dist_matrix = distance_matrix(depot, delivery, clients)

# Parâmetros
alpha = 0.25
max_iter = 10000
# alpha     : parâmetro da fase de construção GRASP
# max_iter  : número máximo de iterações

# Inicialização
best_solution_found = float("inf")
best_routes_found = None
best = []

for iteration in range(1, max_iter + 1): 
    routes = construction_phase(alpha, capacidade, dist_matrix, demands)
    solution = cost_solution(routes, dist_matrix)

    # Reallocation
    new_routes = reallocation(routes, capacidade, demands, dist_matrix)
    new_solution = cost_solution(new_routes, dist_matrix)
    if new_solution < solution:
        solution, routes = new_solution, new_routes

    # Swap
    new_routes = swap(routes, capacidade, demands, dist_matrix)
    new_solution = cost_solution(new_routes, dist_matrix)
    if new_solution < solution:
        solution, routes = new_solution, new_routes

    # 2-opt
    # Aplica 2-opt em todas as rotas
    new_routes = [two_opt_route(r, dist_matrix) for r in routes]
    new_solution = cost_solution(new_routes, dist_matrix)
    if new_solution < solution:
        solution, routes = new_solution, new_routes

    # Atualiza melhor solução global
    if solution < best_solution_found:
        best_solution_found = solution
        best_routes_found = routes

    best.append(best_solution_found)


# Resultado final
print(f"The best solution found: {best_solution_found:.2f}")
print("Melhores rotas:", best_routes_found)
plt.plot(best, color='blue')
plt.xlabel('Iteração')
plt.ylabel('Distância total')
plt.legend()
plt.grid(True)
plt.show()

# Imprimindo rotas
plot_routes(routes, depot, delivery, clients)

