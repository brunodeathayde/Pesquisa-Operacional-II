import numpy as np
import matplotlib.pyplot as plt
from read_layout import read_layout

from ILS_layout_operators import(
    random_initial_solution,
    cost_layout,
    perturbation,
    two_opt_qap_best_improvement,
    plot_layout
)

# Exemplo de uso
dist, flows = read_layout("layout-1.txt")
n = len(dist)

# parâmetros
size = 0.3
max_iter = 500

# Inicialização
layout = random_initial_solution (n)
best_cost = cost_layout(dist, flows, layout)
layout, best_cost = two_opt_qap_best_improvement(layout, dist, flows, best_cost)
print(f"Initial solution {best_cost:.2f}")
best = []

for iteration in range(1, max_iter + 1): 
    # Perturbação
    new_layout = perturbation(layout,size)
    new_cost = cost_layout(dist, flows, new_layout)

    # Busca local
    new_layout, new_cost = two_opt_qap_best_improvement(new_layout, dist, flows, new_cost)

    # Aceitação
    if new_cost < best_cost:
        layout, best_cost = new_layout, new_cost

    best.append(best_cost)


# Resultado final
print(f"The best solution found: {best_cost:.2f}")

# Plotar o gráfico
plt.plot(best, color='blue')
plt.xlabel('Iteração')
plt.ylabel('Função objetivo')
plt.legend()
plt.grid(True)
plt.show()

# Plotar o layout gerado
plot_layout(layout, title="Layout")
