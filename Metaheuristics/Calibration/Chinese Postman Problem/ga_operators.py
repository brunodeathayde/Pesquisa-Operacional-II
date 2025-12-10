import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Geração da população inicial
def genpop(pop_size, n_nodes):
    pop = []
    nodes = list(range(n_nodes))
    for _ in range(pop_size):
        individuo = nodes[:]          
        random.shuffle(individuo)     
        pop.append(individuo)
    return np.array(pop)

# Fitness da população inicial
def fitness_population(pop, G):
    fitness = []
    for individuo in pop:
        custo_total = 0
        valido = True        
        for i in range(len(individuo)-1):
            u, v = individuo[i], individuo[i+1]
            try:                
                caminho_custo = nx.shortest_path_length(G, source=u, target=v, weight="weight")
                custo_total += caminho_custo
            except nx.NetworkXNoPath:                
                valido = False
                break
        if valido:
            fitness.append(custo_total)
        else:
            fitness.append(float("inf"))  
    return fitness

# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Cruzamento OX (Order Crossover)
def order_crossover(parent1, parent2):
    n = len(parent1)    
    cut1, cut2 = sorted(random.sample(range(n), 2))    
    offspring = [None] * n    
    offspring[cut1:cut2+1] = parent1[cut1:cut2+1]    
    segment_set = set(parent1[cut1:cut2+1])    
    remaining_genes = [gene for gene in parent2 if gene not in segment_set]    
    idx = 0
    for i in range(n):
        pos = (cut2 + 1 + i) % n
        if offspring[pos] is None:
            offspring[pos] = remaining_genes[idx]
            idx += 1    
    return offspring

# Mutação (movimento de swap entre dois genes)
def mutation_swap(prob_mut, offspring):
    if random.random() <= prob_mut:
        idx1, idx2 = random.sample(range(len(offspring)), 2)        
        offspring[idx1], offspring[idx2] = offspring[idx2], offspring[idx1]    
    return offspring

# Fitness do filho gerado
def fitness_offspring(individuo, G):
    custo_total = 0
    valido = True
    for i in range(len(individuo)-1):
        u, v = individuo[i], individuo[i+1]
        try:
            caminho_custo = nx.shortest_path_length(G, source=u, target=v, weight="weight")
            custo_total += caminho_custo
        except nx.NetworkXNoPath:
            valido = False
            break
    if valido:
        return custo_total
    else:
        return float("inf")  

# Substitui o pior indivíduo
def replacement(pop, fitness, offspring, fitness_off):    
    worst_idx = np.argmax(fitness)  # pior = maior valor
    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off
    return pop, fitness

# Vizualização da solução
def plot_solution(G, permutation):    
    # Layout para posicionar os nós
    pos = nx.spring_layout(G, seed=42)    
    # Desenhar o grafo completo
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=600, edge_color="gray")    
    # Desenhar pesos das arestas
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)    
    # Construir lista de arcos da permutação (apenas consecutivos)
    path_edges = [(permutation[i], permutation[i+1]) for i in range(len(permutation)-1)]    
    # Destacar a rota em vermelho
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)    
    plt.title("Permutação destacada no grafo")
    plt.show()
