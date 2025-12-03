import numpy as np
import matplotlib.pyplot as plt

from GA_operators_lot_sizing import(
    generate_lot_sizing_instances,
    read_lot_sizing_instance,
    genpop_lotsizing,
    fitness_population,
    selection,
    uniform_crossover_lotsizing,
    mutation_lotsizing,
    fitness_offspring_lotsizing,
    replacement,
    restart_operator_lotsizing,
    plot_lotsizing_solution
)

#generate_lot_sizing_instances(N=5, T=12, m=1, max_demand=20, seed_value=None, prefix="LS")

# Ler instância
N, T, d, p, h, f_cost = read_lot_sizing_instance("LS-1.txt")

# Parâmetros:
pop_size = 100
prob_mut = 2
num_gen = 20000

# Inicialização
pop = genpop_lotsizing(pop_size, N, T, d)
fitness = fitness_population(pop, N, T, d, p, h, f_cost, penalty=1000)
print("Solução inicial: {:.2f}".format(min(fitness)))

best_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = uniform_crossover_lotsizing(pop, parent1, parent2, N, T)
    offspring = mutation_lotsizing(prob_mut, offspring, N, T, d)
    fitness_offspring = fitness_offspring_lotsizing(offspring, N, T, d, p, h, f_cost, penalty=1000)
    pop,fitness = replacement(pop, fitness, offspring, fitness_offspring)
        # Restart (opcional)
    if min(fitness) == max(fitness):
        print("Restart in generation", generation+1)
        pop = restart_operator_lotsizing(pop, pop_size, fitness, N, T, d)
        fitness = fitness_population(pop, N, T, d, p, h, f_cost, penalty=1000)
    melhor_da_geracao = np.min(fitness)
    best_fitness.append(melhor_da_geracao)

print("Melhor solução: {:.2f}".format(min(fitness)))

# Plotar o gráfico com a evolução do fitness
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()


# Vizualização da solução

# Índice do melhor indivíduo
idx_best = fitness.index(min(fitness))

# Melhor cromossomo
best_individual = pop[idx_best]  

plot_lotsizing_solution(best_individual, N, T)