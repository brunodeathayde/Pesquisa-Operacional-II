import numpy as np
from random import randint

# Converte bits para float no intervalo [-10, 10]
def bits_to_float(bits, min_val=-10, max_val=10):
    binary = ''.join(str(bit) for bit in bits)
    decimal = int(binary, 2)
    max_decimal = 2**len(bits) - 1
    x = min_val + (decimal / max_decimal) * (max_val - min_val)
    return x

# Avalia a população
def fitness_population(pop, pop_size):
    fitness = np.zeros(pop_size)
    for j in range(pop_size):
        x = bits_to_float(pop[j])
        fitness[j] = x**2  # Minimizar x^2
    return fitness

# Avalia o filho gerado
def fitness_offspring(offspring):
    x = bits_to_float(offspring)
    return x**2

# Gera população inicial aleatoriamente
def genpop(n, popsize):
    return np.array([[randint(0, 1) for _ in range(n)] for _ in range(popsize)])

# Mutação simples
def mutation(pmut, offspring):
    rand = randint(1, 100)
    if rand <= pmut * 100:  # pmut é probabilidade entre 0 e 1
        idx = randint(0, len(offspring) - 1)
        offspring[idx] = 1 - offspring[idx]
    return offspring

# Substitui o pior indivíduo
def replacement(pop, fitness, offspring, fitness_off):    
    worst_idx = np.argmax(fitness)  # pior = maior valor

    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off

    return pop, fitness


# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Crossover uniforme
def uniform_crossover(n, pop, parent1, parent2):
    return np.array([
        pop[parent1][j] if randint(0, 1) == 0 else pop[parent2][j]
        for j in range(n)
    ])
