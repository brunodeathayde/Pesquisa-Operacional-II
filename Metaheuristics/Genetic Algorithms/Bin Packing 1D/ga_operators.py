import numpy as np
import random
from random import randint

def genpop(pop_size, n_itens, n_bins, l, L):
    pop = []
    for _ in range(pop_size):
        individuo = [-1] * n_itens  # Cada posição representa um item, valor é o bin
        bin_loads = [0] * n_bins    # Carga atual de cada bin

        for i in range(n_itens):
            bins_viaveis = [b for b in range(n_bins) if bin_loads[b] + l[i] <= L]
            if bins_viaveis:
                b = random.choice(bins_viaveis)
                individuo[i] = b
                bin_loads[b] += l[i]
        pop.append(individuo)
    return np.array(pop)


def fitness_population(pop, l, L):
    fitness = []
    for individuo in pop:
        bins_usados = set([b for b in individuo if b != -1])
        if not bins_usados:
            fitness.append(float('inf'))
            continue
        carga_por_bin = {}
        for i, bin_id in enumerate(individuo):
            if bin_id == -1:
                continue
            carga_por_bin.setdefault(bin_id, 0)
            carga_por_bin[bin_id] += l[i]
        perda_quadrada = sum((L - carga) ** 2 for carga in carga_por_bin.values())
        fitness.append(perda_quadrada / len(bins_usados))
    return fitness

# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Avalia o filho gerado 
def fitness_offspring(individuo, l, L):
    bins_usados = set([b for b in individuo if b != -1])
    if not bins_usados:
        return float('inf')
    carga_por_bin = {}
    for i, bin_id in enumerate(individuo):
        if bin_id == -1:
            continue
        carga_por_bin.setdefault(bin_id, 0)
        carga_por_bin[bin_id] += l[i]
    perda_quadrada = sum((L - carga) ** 2 for carga in carga_por_bin.values())
    return perda_quadrada / len(bins_usados)

# Substitui o pior indivíduo
def replacement(pop, fitness, offspring, fitness_off):    
    worst_idx = np.argmax(fitness)  # pior = maior valor
    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off
    return pop, fitness

# Seleção por torneio (problema de maximização)
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] > fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] > fitness[candidates[3]] else candidates[3]
    return parent1, parent2

def uniform_crossover(n, pop, parent1, parent2, l, L, n_bins):
    offspring = [-1] * n
    bin_loads = [0] * n_bins
    for j in range(n):
        gene = pop[parent1][j] if random.randint(0, 1) == 0 else pop[parent2][j]
        # Tenta alocar o item no bin herdado se for viável
        if bin_loads[gene] + l[j] <= L:
            offspring[j] = gene
            bin_loads[gene] += l[j]
        else:
            # Tenta alocar em outro bin viável aleatório
            bins_viaveis = [b for b in range(n_bins) if bin_loads[b] + l[j] <= L]
            if bins_viaveis:
                b = random.choice(bins_viaveis)
                offspring[j] = b
                bin_loads[b] += l[j]
            # Se não couber em nenhum bin, permanece -1
    return np.array(offspring)

def mutation(prob_mut, offspring, l, L, n_bins):

    if random.random() <= prob_mut:
        idx = random.randint(0, len(offspring) - 1)  # item a ser mutado
        bin_atual = offspring[idx]

        # Calcula carga atual por bin
        bin_loads = [0] * n_bins
        for i, b in enumerate(offspring):
            if b != -1:
                bin_loads[b] += l[i]
        # Tenta mover o item para outro bin viável
        bins_viaveis = [b for b in range(n_bins) if b != bin_atual and bin_loads[b] + l[idx] <= L]
        if bins_viaveis:
            novo_bin = random.choice(bins_viaveis)
            offspring[idx] = novo_bin
    return offspring

def fitness_offspring(offspring, l, L):
    bins_usados = set([b for b in offspring if b != -1])
    if not bins_usados:
        return float('inf')
    carga_por_bin = {}
    for i, bin_id in enumerate(offspring):
        if bin_id == -1:
            continue
        carga_por_bin.setdefault(bin_id, 0)
        carga_por_bin[bin_id] += l[i]
    perda_quadrada = sum((L - carga) ** 2 for carga in carga_por_bin.values())
    return perda_quadrada / len(bins_usados)
