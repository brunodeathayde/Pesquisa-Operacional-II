import numpy as np
import matplotlib.pyplot as plt
from ga_operators import (
    genpop,
    fitness_population,
    fitness_offspring,
    mutation,
    replacement,
    selection,
    uniform_crossover,
    bits_to_float
)

# Parâmetros
pop_size = 50
num_gen = 100
prob_mut = 0.01
precision = 10

# Inicialização
pop = genpop(precision, pop_size)
fitness = fitness_population(pop, pop_size)

melhores_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = uniform_crossover(precision, pop, parent1, parent2)
    offspring = mutation(prob_mut, offspring)
    fitness_off = fitness_offspring(offspring)
    pop, fitness = replacement(pop, fitness, offspring, fitness_off)

    melhor_da_geracao = np.min(fitness)
    melhores_fitness.append(melhor_da_geracao)



# Resultado final
best_idx = np.argmin(fitness)
best_bits = pop[best_idx]
best_x = bits_to_float(best_bits)
print(f"Melhor x encontrado: {best_x:.6f}")
print(f"Valor mínimo de x^2: {fitness[best_idx]:.6f}")


# Plotar o gráfico com a evolução do fitness
plt.plot(melhores_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness (x²)')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()

