import numpy as np
import matplotlib.pyplot as plt

from pmedian_reading import pmedian_reading
from distance_matrix import distance_matrix
from ga_operators import (
    genpop,
    fitness_population,
    selection,
    uniform_crossover_pmedian,
    mutation_pmedian,
    fitness_offspring_pmedian,
    replacement,
    restart_operator,
    plot_best_solution
)

# Dados de entrada
file_name = "pmedian-1.txt"
p, coords = pmedian_reading(file_name)
n = len(coords)
dist_matrix = distance_matrix(n,coords)

# Parâmetros:
pop_size = 100
prob_mut = 2
num_gen = 50000

# Inicialziando população
pop = genpop(pop_size, n, p)
fitness = fitness_population(pop, dist_matrix)
print("Solução inicial: {:.2f}".format(min(fitness)))

best_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = uniform_crossover_pmedian(n, pop, parent1, parent2, p)
    offspring = mutation_pmedian(prob_mut, offspring, p)
    fitness_offspring = fitness_offspring_pmedian(offspring, dist_matrix)
    pop,fitness = replacement(pop, fitness, offspring, fitness_offspring)
    # Restart (opcional)
    if min(fitness) == max(fitness):
        print("Restart in generation", generation+1)
        pop = restart_operator(pop, pop_size, fitness, n, p)
        fitness = fitness_population(pop, dist_matrix)
    melhor_da_geracao = np.min(fitness)
    best_fitness.append(melhor_da_geracao)

best_index = np.argmin(fitness)
best_value = best_fitness[best_index]
best_solution = pop[best_index] 
print("Solução obtida: {:.2f}".format(min(fitness)))


# Plotar o gráfico com a evolução do fitness
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()

# Plotar a solução obtida
plot_best_solution(coords, best_solution)



