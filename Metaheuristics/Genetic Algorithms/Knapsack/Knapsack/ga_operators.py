import numpy as np
from random import randint

# Operadores que penalizam soluções viáveis

# Avalia a população
def fitness_population(pop, p, w, W):
    pop_size = len(pop)
    fitness = np.zeros(pop_size)

    for j in range(pop_size):
        individual = np.array(pop[j])
        total_profit = np.sum(np.array(p) * individual)
        total_weight = np.sum(np.array(w) * individual)

        if total_weight <= W:
            fitness[j] = total_profit
        else:
            penalty = (total_weight - W) * 10
            fitness[j] = total_profit - penalty

    return fitness

# Avalia o filho gerado
def fitness_offspring(p, w, W, offspring):
    offspring = np.array(offspring)
    p = np.array(p)
    w = np.array(w)

    total_profit = np.sum(p * offspring)
    total_weight = np.sum(w * offspring)

    if total_weight <= W:
        return total_profit
    else:
        penalty = (total_weight - W) * 100  # penalidade proporcional ao excesso
        return total_profit - penalty


# Gera população inicial aleatoriamente
def genpop(n, pop_size):
    return np.array([[randint(0, 1) for _ in range(n)] for _ in range(pop_size)])

# Mutação simples
def mutation(prob_mut, offspring):
    rand = randint(1, 100)
    if rand <= prob_mut * 100:  # prob_mut é probabilidade entre 0 e 1
        idx = randint(0, len(offspring) - 1)
        offspring[idx] = 1 - offspring[idx]
    return offspring

# Substitui o pior indivíduo problema de maximização)
def replacement(pop, fitness, offspring, fitness_off):
    worst_idx = np.argmin(fitness)

    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off > fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off

    return pop, fitness

# Seleção por torneio (problema de maximização)
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] > fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] > fitness[candidates[3]] else candidates[3]
    return parent1, parent2


# Crossover uniforme
def uniform_crossover(n, pop, parent1, parent2):
    return np.array([
        pop[parent1][j] if randint(0, 1) == 0 else pop[parent2][j]
        for j in range(n)
    ])

# Novos operadores - geração de soluções viáveis

# Geração da população apenas com soluções viáveis
def genpop_feasible(n, pop_size, w, W):
    pop = []

    for _ in range(pop_size):
        individuo = [0] * n
        peso_total = 0

        for i in range(n):
            if peso_total + w[i] <= W:
                gene = randint(0, 1)
                if gene == 1:
                    peso_total += w[i]
                    individuo[i] = 1
            # Se não couber, mantém 0
        pop.append(individuo)

    return np.array(pop)

# Operador de cruzamneto que gera apenas filhos viáveis
def uniform_crossover_feasible(n, pop, parent1, parent2, w, W):
    offspring = [0] * n
    peso_total = 0

    for j in range(n):
        gene = pop[parent1][j] if randint(0, 1) == 0 else pop[parent2][j]
        if gene == 1 and peso_total + w[j] <= W:
            offspring[j] = 1
            peso_total += w[j]
        # Caso contrário, mantém 0

    return np.array(offspring)

# Operador de mutação que não infringe a viabilidade
def mutation_feasible(prob_mut, offspring, w, W):
    rand = randint(1, 100)
    if rand <= prob_mut * 100:
        idx = randint(0, len(offspring) - 1)
        mutated = offspring.copy()
        mutated[idx] = 1 - mutated[idx]  # tenta inverter o gene

        # calcula o novo peso total
        total_weight = np.sum(np.array(w) * mutated)

        # só aplica a mutação se não ultrapassar a capacidade
        if total_weight <= W:
            offspring[idx] = mutated[idx]
    return offspring
