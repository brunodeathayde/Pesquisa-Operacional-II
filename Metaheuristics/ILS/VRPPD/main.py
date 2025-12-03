import matplotlib.pyplot as plt
import random

from ILS_operators_VRPPD import(
    vrppd_reading,
    route_cost,
    flatten_routes,
    perturbation,
    two_opt_pdvrp,
    plotting_route_pick_up_and_delivery
)

# Lendo a instância
file_name = "VRPPD-1.txt"
P = vrppd_reading(file_name)
n = len(P)
# Capacidade do veículo (frota homogênea)
capacity = 20

# parâmetros
size = 0.4
max_iter = 1000

# Inicialização com rota aleatória
route = random.sample(range(0, n), n)
route, dist_total, viavel = route_cost(route, P, capacity)
best_route = route
best_cost = dist_total
print(f"Initial solution {best_cost:.2f}")

best = []

for iteration in range(1, max_iter + 1): 
    # Perturbação
    new_route = perturbation(route, size)

    # Flatten obrigatório
    new_route = flatten_routes(new_route)

    # Avalia
    new_route, new_cost, viavel = route_cost(new_route, P, capacity)

    # Local search
    new_route, new_cost = two_opt_pdvrp(new_route, P, capacity)

    # Aceitação
    if new_cost < best_cost:
        best_route, best_cost = new_route, new_cost

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
plotting_route_pick_up_and_delivery(P, best_route, capacity)