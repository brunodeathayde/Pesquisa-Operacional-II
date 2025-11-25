"""
Gerador de população inicial para o problema de p-medianas
@author: brunoprata
"""

import numpy as np
import random
import matplotlib.pyplot as plt

# Geração da população inicial p-medianas
def genpop(pop_size, n_points, p):
    pop = []
    for _ in range(pop_size):
        # Seleciona aleatoriamente p medianas distintas
        medianas = random.sample(range(n_points), p)
        
        # Cria cromossomo: cada ponto é alocado a uma das medianas escolhidas
        individuo = []
        for i in range(n_points):
            # Se o ponto é uma mediana, ele se aloca a si mesmo
            if i in medianas:
                individuo.append(i)
            else:
                # Caso contrário, aloca a uma mediana aleatória
                individuo.append(random.choice(medianas))        
        pop.append(individuo)    
    return np.array(pop)

# Calcula o fitness da população 
def fitness_population(pop, dist_matrix):
    dist_matrix = np.array(dist_matrix)
    fitness = []
    for individuo in pop:
        custo_total = 0.0
        for cliente, mediana in enumerate(individuo):
            custo_total += dist_matrix[cliente, mediana]
        fitness.append(custo_total)
    return fitness

# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Operador de cruzamento para o problema de p-medianas
def uniform_crossover_pmedian(n_points, pop, parent1, parent2, p): 
    offspring = [-1] * n_points
    
    # Passo 1: herdar genes dos pais
    for j in range(n_points):
        gene = pop[parent1][j] if random.randint(0, 1) == 0 else pop[parent2][j]
        offspring[j] = gene
    
    # Passo 2: identificar medianas usadas
    medianas_usadas = set(offspring)
    
    # Passo 3: ajustar para manter exatamente p medianas
    if len(medianas_usadas) > p:
        # reduzir aleatoriamente
        medianas_usadas = set(random.sample(medianas_usadas, p))
    elif len(medianas_usadas) < p:
        # adicionar medianas aleatórias
        candidatos = set(range(n_points)) - medianas_usadas
        adicionais = random.sample(candidatos, p - len(medianas_usadas))
        medianas_usadas.update(adicionais)
    
    medianas_usadas = list(medianas_usadas)
    
    # Passo 4: reatribuir clientes às medianas válidas
    for j in range(n_points):
        if offspring[j] not in medianas_usadas:
            offspring[j] = random.choice(medianas_usadas)
    
    return np.array(offspring)

# Operador de mutação para o problema de p-medianas
def mutation_pmedian(prob_mut, offspring, p):
    if random.random() <= prob_mut:
        # Identificar medianas usadas no cromossomo
        medianas_usadas = set(offspring)
        
        # Selecionar candidatos à mutação: pontos que não são medianas
        candidatos = [i for i in range(len(offspring)) if i not in medianas_usadas]
        
        if len(candidatos) >= 2:
            # Escolher dois pontos distintos
            i, j = random.sample(candidatos, 2)
            
            # Verificar se estão alocados a medianas diferentes
            if offspring[i] != offspring[j]:
                # Trocar as alocações
                offspring[i], offspring[j] = offspring[j], offspring[i]
    
    return np.array(offspring)

# Calcula o fitness do filho gerado
def fitness_offspring_pmedian(offspring, dist_matrix):
    dist_matrix = np.array(dist_matrix)  # garante que seja NumPy
    custo_total = 0.0
    for cliente, mediana in enumerate(offspring):
        custo_total += dist_matrix[cliente, mediana]
    return custo_total

# Substitui o pior indivíduo
def replacement(pop, fitness, offspring, fitness_off):    
    worst_idx = np.argmax(fitness)  # pior = maior valor
    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off
    return pop, fitness

# Operador de restart

def restart_operator(pop, pop_size, fitness, n_points, p):
    # Guarda o melhor indivíduo
    idx_melhor = fitness.index(min(fitness))
    melhor_individuo = pop[idx_melhor]

    # Gera nova população (usando genpop_pmedian internamente)
    new_pop = genpop(pop_size, n_points, p)

    # Escolhe posição aleatória para inserir o melhor indivíduo
    pos = random.randint(0, len(new_pop) - 1)
    new_pop[pos] = melhor_individuo

    return new_pop

import matplotlib.pyplot as plt

def plot_best_solution(coords, best_solution):
    # Identificar medianas usadas
    medianas = set(best_solution)

    plt.figure(figsize=(6,6))
    for i, (x,y) in enumerate(coords):
        if i in medianas:
            # Medianas em vermelho (quadrado)
            plt.scatter(x, y, c='red', marker='s', s=120,
                        label='Mediana' if i == list(medianas)[0] else "")
        else:
            # Clientes em azul (círculo)
            plt.scatter(x, y, c='blue', marker='o', s=80,
                        label='Cliente' if i == 0 else "")
            
            # Só desenhar linha se o ponto não for mediana
            mediana = best_solution[i]
            mx, my = coords[mediana]
            plt.plot([x, mx], [y, my], 'k--', alpha=0.5)

    plt.legend()
    plt.title("Alocação dos pontos às medianas (melhor solução)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()







