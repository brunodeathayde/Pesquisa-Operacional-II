import numpy as np
import matplotlib.pyplot as plt
from ga_operators import (
    genpop,
    fitness_population,
    selection,
    order_crossover,
    mutation_swap,
    fitness_offspring,
    replacement
)

def full_genetic_algorithm(graph, pop_size, prob_mut, num_gen):
    n_nodes = len(graph)

    # Inicialização
    pop = genpop(pop_size, n_nodes)
    fitness = fitness_population(pop, graph)


    # Loop evolucionário
    for generation in range(1, num_gen + 1):
        parent1, parent2 = selection(pop_size, fitness)
        offspring = order_crossover(pop[parent1], pop[parent2])
        offspring = mutation_swap(prob_mut, offspring)
        fitness_off = fitness_offspring(offspring, graph)
        pop, fitness = replacement(pop, fitness, offspring, fitness_off)

    # Melhor solução
    best_idx = np.argmin(fitness)
    best_solution = pop[best_idx].tolist()
    best_fitness = np.min(fitness)

    return best_fitness
