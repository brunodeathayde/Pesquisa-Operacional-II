from random import randint, seed
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_lot_sizing_instances(N, T, m, max_demand, seed_value=None, prefix="LS"):
    if seed_value is not None:
        seed(seed_value)
    
    for k in range(m):
        file_name = f"{prefix}-{k+1}.txt"
        with open(file_name, "w") as file:
            # N e T
            file.write(f"{N}\n")
            file.write(f"{T}\n\n")
            
            # Demanda
            file.write("# demanda\n")
            for i in range(N):
                row = [str(randint(0, max_demand)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo de produção
            file.write("# custo de produção\n")
            for i in range(N):
                row = [str(randint(1, 20)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo de estoque
            file.write("# custo de estoque\n")
            for i in range(N):
                row = [str(randint(1, 10)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo fixo (setup)
            file.write("# custo fixo (setup)\n")
            for i in range(N):
                row = [str(randint(5, 30)) for t in range(T)]
                file.write(" ".join(row) + "\n")


def read_lot_sizing_instance(file_name):
    with open(file_name, "r") as f:
        # Remove linhas vazias e espaços
        lines = [line.strip() for line in f if line.strip()]
    
    # N e T
    N = int(lines[0])
    T = int(lines[1])
    
    # Localiza seções
    idx_demand = lines.index("# demanda") + 1
    idx_prod = lines.index("# custo de produção") + 1
    idx_stock = lines.index("# custo de estoque") + 1
    idx_setup = lines.index("# custo fixo (setup)") + 1
    
    # Lê matrizes
    def read_matrix(start_idx):
        mat = []
        for i in range(N):
            row = list(map(int, lines[start_idx + i].split()))
            if len(row) != T:
                raise ValueError(f"Linha {start_idx + i} tem {len(row)} valores, esperado {T}.")
            mat.append(row)
        return mat
    
    d = read_matrix(idx_demand)
    p = read_matrix(idx_prod)
    h = read_matrix(idx_stock)
    f_cost = read_matrix(idx_setup)
    
    return N, T, d, p, h, f_cost

# Gera uma população inicial de forma aleatória
def genpop_lotsizing(pop_size, N, T, demand):
    pop = []
    for _ in range(pop_size):
        individuo = []
        for t in range(T):
            for i in range(N):
                # produção aleatória entre 0 e 150% da demanda
                prod = random.randint(0, int(demand[i][t] * 1.5))
                individuo.append(prod)
        pop.append(individuo)
    return np.array(pop)

# Calcula o fitness (custo total) de cada indivíduo da população
def fitness_population(pop, N, T, demand, p, h, f_cost, penalty=1000):
    fitness = []
    
    for individuo in pop:
        custo_total = 0.0
        
        # Reconstruir matriz de produção do cromossomo
        prod_matrix = np.array(individuo).reshape(T, N).T  # N x T
        
        # Estoque inicial = 0
        estoque = np.zeros((N, T))
        
        for i in range(N):
            estoque_acumulado = 0
            for t in range(T):
                producao = prod_matrix[i, t]
                demanda = demand[i][t]
                
                # Produção
                custo_total += p[i][t] * producao
                
                # Setup
                if producao > 0:
                    custo_total += f_cost[i][t]
                
                # Atualiza estoque
                estoque_acumulado += producao - demanda
                if estoque_acumulado < 0:
                    # Penalização por não atender demanda
                    custo_total += penalty * abs(estoque_acumulado)
                    estoque_acumulado = 0  # não pode ser negativo
                estoque[i, t] = estoque_acumulado
                
                # Custo de estoque
                custo_total += h[i][t] * estoque[i, t]
        
        fitness.append(custo_total)
    
    return fitness

# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Cruzamento uniforme
def uniform_crossover_lotsizing(pop, parent1, parent2, N, T):
    n_genes = N * T
    offspring = [-1] * n_genes
    
    # Passo 1: herdar genes dos pais
    for j in range(n_genes):
        gene = pop[parent1][j] if random.randint(0, 1) == 0 else pop[parent2][j]
        offspring[j] = gene
    
    return offspring

# Mutação
def mutation_lotsizing(prob_mut, offspring, N, T, demand):
    if random.random() <= prob_mut:
        # Seleciona item e período aleatoriamente
        i = random.randint(0, N-1)
        t = random.randint(0, T-1)
        
        # Produção total atual do item
        prod_matrix = np.array(offspring).reshape(T, N).T  # N x T
        total_prod = sum(prod_matrix[i])
        total_demand = sum(demand[i])
        
        gene_index = t * N + i  # posição do gene no vetor
        
        if total_prod < total_demand:
            # aumentar produção para ajudar a atender demanda
            deficit = total_demand - total_prod
            offspring[gene_index] += deficit
        elif total_prod > total_demand:
            # reduzir produção para diminuir excesso
            excess = total_prod - total_demand
            offspring[gene_index] = max(0, offspring[gene_index] - excess)
        # se total_prod == total_demand, não faz nada
    
    return offspring

# calcula do fitness do filho gerado
def fitness_offspring_lotsizing(offspring, N, T, demand, p, h, f_cost, penalty=1000):
    custo_total = 0.0
    
    # Reconstruir matriz de produção do cromossomo
    prod_matrix = np.array(offspring).reshape(T, N).T  # N x T
    
    # Estoque inicial = 0
    estoque = np.zeros((N, T))
    
    for i in range(N):
        estoque_acumulado = 0
        for t in range(T):
            producao = prod_matrix[i, t]
            demanda = demand[i][t]
            
            # Custo de produção
            custo_total += p[i][t] * producao
            
            # Custo de setup
            if producao > 0:
                custo_total += f_cost[i][t]
            
            # Atualiza estoque
            estoque_acumulado += producao - demanda
            if estoque_acumulado < 0:
                # Penalização por não atender demanda
                custo_total += penalty * abs(estoque_acumulado)
                estoque_acumulado = 0  # não pode ser negativo
            estoque[i, t] = estoque_acumulado
            
            # Custo de estoque
            custo_total += h[i][t] * estoque[i, t]
    
    return custo_total

# Substitui o pior indivíduo
def replacement(pop, fitness, offspring, fitness_off):    
    worst_idx = np.argmax(fitness)  # pior = maior valor
    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off
    return pop, fitness

# Operador de reinicialziação
def restart_operator_lotsizing(pop, pop_size, fitness, N, T, demand):
    # Guarda o melhor indivíduo
    idx_melhor = fitness.index(min(fitness))
    melhor_individuo = pop[idx_melhor]
    
    # Gera nova população
    new_pop = genpop_lotsizing(pop_size, N, T, demand)
    
    # Escolhe posição aleatória para inserir o melhor indivíduo
    pos = random.randint(0, len(new_pop) - 1)
    new_pop[pos] = melhor_individuo
    
    return new_pop

# Vizualização da melhor solução obtida
def plot_lotsizing_solution(best_individual, N, T):
    # Reconstruir matriz de produção N x T
    prod_matrix = np.array(best_individual).reshape(T, N).T  # N x T
    
    # Plotar gráfico de barras empilhadas
    periods = np.arange(1, T+1)
    bottom = np.zeros(T)
    
    plt.figure(figsize=(10,6))
    
    for i in range(N):
        plt.bar(periods, prod_matrix[i], bottom=bottom, label=f"Item {i+1}")
        bottom += prod_matrix[i]
    
    plt.xlabel("Períodos")
    plt.ylabel("Quantidade produzida")
    
    # Legenda fora do gráfico (à direita)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    
    plt.xticks(periods)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()  # ajusta layout para não cortar legenda
    plt.show()




