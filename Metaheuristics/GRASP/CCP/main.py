"""
GRASP para o problema de agrupamento capacitado (CCP)
@author: brunoprata
"""

import numpy as np
import matplotlib.pyplot as plt
from grasp_ccp_operators import (
    ccp_reading,
    distance_matrix_ccp,
    construction_phase_ccp,
    cost_solution_ccp,
    reallocation_ccp,
    swap_ccp,
    plot_clusters_assignment
)

# Dados de entrada
# p           : número de clusters
# n           : número de clientes
# clientes    : coordenadas e demanda dos clientes
# clusters    : coordenadas e capacidade dos clusters
# demandas    : vetor com as demandas dos clientes
# capacidades : vetor com as capacidades dos clusters
# dist_matrix : matriz de distâncias cliente–cluster
instancia = "ccp-1.txt"
p, n, clientes, clusters = ccp_reading(instancia)

# Converte imediatamente para numpy arrays
clientes = np.array(clientes)
clusters = np.array(clusters)

demandas = clientes[:, 2]
capacidades = clusters[:, 2]
dist_matrix = distance_matrix_ccp(clientes, clusters)

# Parâmetros GRASP
alpha = 0.25   # controla aleatoriedade na fase de construção
max_iter = 5000  # número máximo de iterações

# Inicialização
best_solution_found = float("inf")
best_assignment_found = None
best = []

for iteration in range(1, max_iter + 1):
    # Construção
    assignment = construction_phase_ccp(alpha, dist_matrix, demandas, capacidades)
    solution = cost_solution_ccp(assignment, dist_matrix)

    # Reallocation
    new_assignment = reallocation_ccp(assignment, demandas, capacidades, dist_matrix)
    new_solution = cost_solution_ccp(new_assignment, dist_matrix)
    if new_solution < solution:
        solution, assignment = new_solution, new_assignment

    # Swap
    new_assignment = swap_ccp(assignment, demandas, capacidades, dist_matrix)
    new_solution = cost_solution_ccp(new_assignment, dist_matrix)
    if new_solution < solution:
        solution, assignment = new_solution, new_assignment

    # Atualiza melhor solução global
    if solution < best_solution_found:
        best_solution_found = solution
        best_assignment_found = assignment

    best.append(best_solution_found)

# Resultado final
print(f"The best solution found: {best_solution_found:.4f}")
print("Melhor atribuição (cluster de cada cliente):")
print(best_assignment_found)

# Curva de convergência
plt.figure(figsize=(8,5))
plt.plot(best, color='blue', linewidth=1.5)
plt.title("Convergência do GRASP CCP")
plt.xlabel("Iteração")
plt.ylabel("Custo (soma das distâncias)")
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Plot da atribuição final
plot_clusters_assignment(best_assignment_found, clientes, clusters)
