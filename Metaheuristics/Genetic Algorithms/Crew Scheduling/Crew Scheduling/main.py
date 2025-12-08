from scp_reading import scp_reading
import time
import numpy as np
import matplotlib.pyplot as plt
from genpop import genpop
from fitness_evaluation import fitness_evaluation
from fitness_offspring import fitness_offspring
from selection import selection
from uniform_crossover import uniform_crossover
from mutation import mutation
from replacement import replacement

# Tempo inicial 
time_start = time.perf_counter()

# Leitura da instância
A,c = scp_reading("SCP-1.txt")
m = len(A)
n = len(A[0])


# Parâmetros:
popsize = 10
penalty = 1000
pmut = 5
time_limit = 20   # limite de tempo em segundos

# Inicialização
pop = genpop(n, popsize)
fitness = fitness_evaluation(A, c, pop, popsize, penalty)

print("Fitness - população inicial:")
print(fitness)

# Evolução com limite de tempo
best_fitness = []
cont = 1
while (time.perf_counter() - time_start) < time_limit:
    parent1, parent2 = selection(popsize, fitness)
    offspring = uniform_crossover(n, pop, parent1, parent2)
    offspring = mutation(pmut, offspring)
    fo = fitness_offspring(A, c, offspring, penalty)
    pop, fitness = replacement(pop, fitness, offspring, fo)

    # Melhor da geração
    melhor_da_geracao = np.min(fitness)
    best_fitness.append(melhor_da_geracao)

    cont += 1

# Resultados finais
best_index = np.argmin(fitness)
best_value = best_fitness[best_index]
best_solution = pop[best_index]

print("Solução obtida: {:.2f}".format(min(fitness)))
print("Número de gerações executadas:", cont)

time_elapsed = time.perf_counter() - time_start
print("Tempo computacional (s):")
print(f"{time_elapsed:.2f}")

# Plotar evolução do melhor fitness 
plt.plot(best_fitness)
plt.xlabel('Geração')
plt.ylabel('Melhor Fitness')
plt.title('Evolução do Melhor Fitness')
plt.grid(True)
plt.show()
