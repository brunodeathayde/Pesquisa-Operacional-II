import numpy as np
import matplotlib.pyplot as plt
from ga_bp2D_operators import(
    binpacking2d_reading,
    genpop_binpacking2d,
    fitness_population_2d,
    selection,
    combined_crossover,
    mutation,
    fitness_offspring_2d,
    replacement,
    plot_best_solution
)

# Ler instância
itens, largura_bin, altura_bin = binpacking2d_reading("bin2d-1.txt")
n_items = len(itens)

# Parâmetros
pop_size = 20
prob_mut = 5
num_gen = 500

# Inicialização
pop = genpop_binpacking2d(pop_size, n_items)
fitness = fitness_population_2d(pop, itens, largura_bin, altura_bin)
print("Melhor solução inicial", min(fitness))

best_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = combined_crossover(pop[parent1], pop[parent2])
    offspring = mutation(prob_mut, offspring)
    fitness_offspring = fitness_offspring_2d(offspring, itens, largura_bin, altura_bin)
    pop, fitness = replacement(pop, fitness, offspring, fitness_offspring) 
    best_fitness.append(np.min(fitness))

print("Melhor solução: ",min(best_fitness))

# Plotar o gráfico com a evolução do fitness
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()




# índice do melhor indivíduo (menor fitness)
best_idx = np.argmin(fitness)
# extrai ordem e orientação
ordem_best, orientation_best = pop[best_idx]
# monta a tupla do melhor indivíduo
best_individuo = (ordem_best, orientation_best)
# plota a solução
plot_best_solution(best_individuo, itens, largura_bin, altura_bin)


