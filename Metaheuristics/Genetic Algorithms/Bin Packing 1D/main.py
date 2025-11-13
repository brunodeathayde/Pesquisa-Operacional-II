import numpy as np
import math
import matplotlib.pyplot as plt
from ga_operators import (
    genpop,
    fitness_population,
    fitness_offspring,
    mutation,
    replacement,
    selection,
    uniform_crossover
)

# Instância
# Tamanhos dos itens 
l = [2.7, 5.9, 1.8, 3.6, 4.2, 0.9, 2.1, 5.4, 3.3, 1.2,
     4.8, 2.5, 5.1, 3.0, 1.7, 2.9, 4.4, 0.6, 3.8, 5.6,
     1.5, 2.3, 4.0, 3.1, 5.7, 0.7, 2.6, 4.9, 1.0, 3.5,
     5.3, 2.0, 4.6, 0.8, 3.9, 1.3, 5.0, 2.8, 4.1, 3.2,
     1.9, 5.2, 0.5, 4.3, 2.2, 3.7, 1.1, 5.5, 0.6, 4.7,
     2.4, 3.4, 1.6, 5.8, 0.7, 4.5, 2.1, 3.6, 1.4, 5.9,
     0.9, 4.2, 2.7, 3.3, 1.8, 5.1, 0.5, 4.0, 2.6, 3.0,
     1.2, 5.4, 0.8, 4.6, 2.3, 3.9, 1.0, 5.7, 0.6, 4.8,
     2.5, 3.1, 1.5, 5.0, 0.7, 4.4, 2.9, 3.8, 1.1, 5.2,
     0.9, 4.1, 2.0, 3.7, 1.3, 5.6, 0.5, 4.3, 2.8, 3.2]

# Capacidade do bin
L = 12

# Número de itens
n_itens = len(l)

# Estimativa (limite superior) para o número de bins
n_bins = math.ceil(sum(l) / L)


# Parâmetros do Algoritmo Genético
pop_size = 20
num_gen = 1000
prob_mut = 0.01

# Inicialização
pop = genpop(pop_size, n_itens, n_bins, l, L)
fitness = fitness_population(pop, l, L)

best_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = uniform_crossover(n_itens, pop, parent1, parent2, l, L, n_bins)
    offspring = mutation(prob_mut, offspring, l, L, n_bins)
    fitness_off = fitness_offspring(offspring, l, L)
    pop, fitness = replacement(pop, fitness, offspring, fitness_off)
    melhor_da_geracao = np.min(fitness)
    best_fitness.append(melhor_da_geracao)

best_index = np.argmin(best_fitness)
best_value = best_fitness[best_index]
print("Perda quadrática média: {:.2f}".format(best_value))

# Plotar o gráfico com a evolução do fitness
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()

