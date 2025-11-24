from scheptk.scheptk import ParallelMachines
import numpy as np
import matplotlib.pyplot as plt
from pso_operators import (
    gen_velocities,
    gen_population,
    to_permutations,
    position_to_permutation,
    fitness_population,
    update_best,
    update_velocities,
    update_positions,
    apply_elitism
)

# Leitura da instância
instance = ParallelMachines('instance.txt')
n = instance.jobs

popsize = 10
num_gen = 100

# Inicialização
velocities = gen_velocities(n, popsize, vmin=-0.1, vmax=0.1)
pop = gen_population(n, popsize, xmin=-5, xmax=5)
permutations = to_permutations(pop)
fitness = fitness_population(permutations, instance)
p_best_positions, p_best_fitness, g_best_position, g_best_fitness = update_best(
    pop, fitness, p_best_positions=None, p_best_fitness=None)

melhores_fitness = []
media_fitness = []

# Evolução
for generation in range(1, num_gen + 1):    
    velocities = update_velocities(velocities, pop, p_best_positions, g_best_position, c1=1.5, c2=1.5)
    pop = update_positions(pop, velocities, xmin=-5, xmax=5)
    permutations = to_permutations(pop)
    fitness = fitness_population(permutations, instance)
    p_best_positions, p_best_fitness, g_best_position, g_best_fitness = update_best(
        pop, fitness, p_best_positions, p_best_fitness)
    pop, fitness = apply_elitism(pop, fitness, g_best_position, g_best_fitness)
    melhores_fitness.append(g_best_fitness)
    avg_fitness = np.mean(fitness)
    media_fitness.append((avg_fitness))

# Resultado final


best_idx = np.argmin(fitness)
best_bits = pop[best_idx]
print(f"Melhor makespan encontrado: {g_best_fitness}")

plt.plot(melhores_fitness, label='Melhor Fitness', color='blue')
plt.plot(media_fitness, label='Fitness Médio', color='orange')

plt.xlabel('Geração')
plt.ylabel('Fitness')
plt.title('Evolução do Fitness')
plt.legend()
plt.grid(True)
plt.show()

sequence = position_to_permutation(g_best_position)
print(sequence)
instance.print_schedule(sequence, 'Makespan.png')
