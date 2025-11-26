import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from reading_cpp import reading_cpp
from ga_operators import (
    genpop,
    fitness_population,
    selection,
    order_crossover,
    mutation_swap,
    fitness_offspring,
    replacement,
    plot_solution
)

# Ler instância
arquivo = "CPP-1.txt"  # substitua pelo nome do seu arquivo
graph = reading_cpp(arquivo)
n_nodes = len(graph)

# Parâmetros
pop_size = 20
prob_mut = 5
num_gen = 1000

# Inicialização
pop = genpop(pop_size, n_nodes)
fitness = fitness_population(pop, graph)
print("Melhor fitness:", min(fitness))

best_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = order_crossover(pop[parent1], pop[parent2])
    offspring = mutation_swap(prob_mut, offspring)
    fitness_off = fitness_offspring(offspring, graph)
    pop, fitness = replacement(pop, fitness, offspring, fitness_off)    
    best_fitness.append(np.min(fitness))
    
# Plotar o gráfico com a evolução do fitness
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()

# índice da melhor solução
best_idx = np.argmin(fitness)
    
# extrair a melhor permutação
best_solution = pop[best_idx].tolist()
print("Melhor rota: ",best_solution)
print("Melhor fitness: ",min(best_fitness))
plot_solution(graph, best_solution)

