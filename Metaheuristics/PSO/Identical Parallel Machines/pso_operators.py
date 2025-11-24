import numpy as np
from random import randint


# Gera velocidades iniciais contínuas entre -0.1 e 0.1
def gen_velocities(n, popsize, vmin=-0.1, vmax=0.1):
    return np.random.uniform(vmin, vmax, (popsize, n))

# Gera população inicial contínua entre -5 e 5
def gen_population(n, popsize, xmin=-5, xmax=5):
    return np.random.uniform(xmin, xmax, (popsize, n))

# Converte população contínua em população de permutações
def to_permutations(pop):
    # argsort retorna os índices que ordenam cada linha
    return np.argsort(pop, axis=1)


# Converte um solução em permutação
def position_to_permutation(position):
    return np.argsort(position)


# Calcula o makespan para todos os indivíduos da população
def fitness_population(perms, instance):
    fitness = []
    for seq in perms:
        cmax = instance.Cmax(seq)   # calcula o makespan da sequência
        fitness.append(cmax)
    return np.array(fitness)

# Atualiza p_best e g_best
def update_best(positions, fitness, p_best_positions=None, p_best_fitness=None):
    if p_best_positions is None or p_best_fitness is None:
        p_best_positions = positions.copy()
        p_best_fitness = fitness.copy()
    else:
        for i in range(len(fitness)):
            if fitness[i] < p_best_fitness[i]:
                p_best_positions[i] = positions[i].copy()
                p_best_fitness[i] = fitness[i]    
    best_index = np.argmin(p_best_fitness)
    g_best_position = p_best_positions[best_index].copy()
    g_best_fitness = p_best_fitness[best_index]    
    return p_best_positions, p_best_fitness, g_best_position, g_best_fitness

# atualiza as velocidades
def update_velocities(velocities, positions, p_best_positions, g_best_position,
                      c1=1.5, c2=1.5):
    popsize, n = positions.shape
    r1 = np.random.rand(popsize, n)
    r2 = np.random.rand(popsize, n)
    
    new_velocities = (velocities +
                      c1 * r1 * (p_best_positions - positions) +
                      c2 * r2 * (g_best_position - positions))
    return new_velocities

# Atualiza as posições
def update_positions(positions, velocities, xmin=-5, xmax=5):
    new_positions = positions + velocities    
    new_positions = np.clip(new_positions, xmin, xmax)    
    return new_positions

# Garante o elitismo (guarda sempre a melhor solução na população)
def apply_elitism(positions, fitness, g_best_position, g_best_fitness):
    worst_index = np.argmax(fitness)    
    positions[worst_index] = g_best_position.copy()
    fitness[worst_index] = g_best_fitness    
    return positions, fitness
