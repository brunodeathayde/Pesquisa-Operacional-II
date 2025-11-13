import numpy as np
import matplotlib.pyplot as plt
from ga_operators import (
    genpop,
    genpop_feasible,
    fitness_population,
    fitness_offspring,
    mutation,
    mutation_feasible,
    replacement,
    selection,
    uniform_crossover,
    uniform_crossover_feasible
)

# Instância
# Valores dos itens (benefícios)
p = [2, 1, 5, 12, 3, 10, 4, 6, 15, 11, 9, 7]

# Pesos dos itens (custos)
w = [3, 2, 4, 8, 3, 7, 2, 5, 9, 6, 4, 3]

# Capacidade da mochila
W = 25

n_itens = len(p)

# Parâmetros do Algoritmo Genético
pop_size = 20
num_gen = 1000
prob_mut = 0.01


# Inicialização
pop = genpop_feasible(n_itens, pop_size, w, W)
fitness = fitness_population(pop, p, w, W)

melhores_fitness = []

# Evolução
for generation in range(1, num_gen + 1):
    parent1, parent2 = selection(pop_size, fitness)
    offspring = uniform_crossover_feasible(n_itens, pop, parent1, parent2, w, W)
    offspring = mutation_feasible(prob_mut, offspring, w, W)
    fitness_off = fitness_offspring(p, w, W, offspring)
    pop, fitness = replacement(pop, fitness, offspring, fitness_off)
    melhor_da_geracao = np.min(fitness)
    melhores_fitness.append(melhor_da_geracao)


# Resultado final para o problema da mochila
best_idx = np.argmax(fitness)  # queremos o maior lucro, não o menor
best_bits = pop[best_idx]      # vetor binário com os itens selecionados

# Calcula lucro e peso total
total_profit = np.sum(np.array(p) * best_bits)
total_weight = np.sum(np.array(w) * best_bits)

print("Melhor solução encontrada:")
print("Itens selecionados:", best_bits)
print(f"Lucro total: {total_profit}")
print(f"Peso total: {total_weight} (Capacidade: {W})")

# Plotar o gráfico com a evolução do fitness
plt.plot(melhores_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness (lucro)')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()

