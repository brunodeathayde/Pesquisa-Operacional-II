import numpy as np
import random
from random import randint
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Leitura de instância para o problema de Bin Packing 2D
def binpacking2d_reading(file_name):
    data = {}
    with open(file_name, "r") as f:
        code = f.read()
        # interpreta o conteúdo como código Python e armazena em 'data'
        exec(code, {}, data)

    itens = data["itens"]
    largura_bin = data["largura_bin"]
    altura_bin = data["altura_bin"]

    return itens, largura_bin, altura_bin

# Geração da população inicial para o Bin Packing 2D
# Cada indivíduo é composto por:
# Uma permutação representando a ordem dos itens
# Uma lista binária representando a orientação (0 = sem rotação, 1 = rotacionado 90°)
def genpop_binpacking2d(pop_size, n_items):
    population = []
    nodes = list(range(n_items))

    for _ in range(pop_size):
        # Permutação da ordem dos itens
        order = nodes[:]
        random.shuffle(order)

        # Orientação binária dos itens
        orientation = [randint(0, 1) for _ in range(n_items)]

        # Cada indivíduo é uma tupla (ordem, orientação)
        population.append((order, orientation))

    return population

# Calcula a aptidão da população
def fitness_population_2d(pop, itens, largura_bin, altura_bin):
    fitness = []
    area_bin = largura_bin * altura_bin

    for order, orientation in pop:
        bins = []  # cada bin = lista de retângulos colocados [(x,y,w,h)]
        perdas = []

        for item_id in order:
            w, h = itens[item_id]
            if orientation[item_id] == 1:
                w, h = h, w

            # se item não cabe individualmente → inviável
            if w > largura_bin or h > altura_bin:
                fitness.append(float("inf"))
                break

            placed = False
            # tenta colocar em bins existentes
            for bin_rects in bins:
                # procura posição livre simples (varrendo x,y)
                x, y = 0, 0
                while y + h <= altura_bin:
                    while x + w <= largura_bin:
                        # verifica colisão com outros itens
                        overlap = False
                        for (bx, by, bw, bh) in bin_rects:
                            if not (x + w <= bx or bx + bw <= x or
                                    y + h <= by or by + bh <= y):
                                overlap = True
                                break
                        if not overlap:
                            bin_rects.append((x, y, w, h))
                            placed = True
                            break
                        x += 1
                    if placed:
                        break
                    x = 0
                    y += 1
                if placed:
                    break

            # se não coube em nenhum bin, abre novo
            if not placed:
                bins.append([(0, 0, w, h)])

        else:
            # calcula perdas por bin
            for bin_rects in bins:
                area_ocupada = sum(w*h for (_, _, w, h) in bin_rects)
                perdas.append((area_bin - area_ocupada) ** 2)

            fitness.append(sum(perdas) / len(bins))

    return fitness

# Seleção por torneio
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Order Crossover (OX) para ordem de empacotamento dos itens
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

# Crossover uniforme para orientação dos itens 
def uniform_crossover(n, parent1, parent2):
    return np.array([
        parent1[j] if random.randint(0, 1) == 0 else parent2[j]
        for j in range(n)
    ])

# Crossover combinado: OX para a sequência e uniforme para a orientação
def combined_crossover(parent1, parent2):
    ordem1, orient1 = parent1
    ordem2, orient2 = parent2

    # aplica OX na ordem
    ordem_child = order_crossover(ordem1, ordem2)

    # aplica uniforme na orientação
    orient_child = uniform_crossover(len(orient1), orient1, orient2)

    return (ordem_child, orient_child)

# Calcula a aptidão do filho gerado
def fitness_offspring_2d(individuo, itens, largura_bin, altura_bin):
    ordem, orientation = individuo
    area_bin = largura_bin * altura_bin
    bins = []  # cada bin = lista de retângulos colocados [(x,y,w,h)]
    perdas = []

    for item_id in ordem:
        w, h = itens[item_id]
        if orientation[item_id] == 1:
            w, h = h, w

        # se item não cabe individualmente → inviável
        if w > largura_bin or h > altura_bin:
            return float("inf")

        placed = False
        # tenta colocar em bins existentes
        for bin_rects in bins:
            x, y = 0, 0
            while y + h <= altura_bin:
                while x + w <= largura_bin:
                    # verifica colisão com outros itens
                    overlap = False
                    for (bx, by, bw, bh) in bin_rects:
                        if not (x + w <= bx or bx + bw <= x or
                                y + h <= by or by + bh <= y):
                            overlap = True
                            break
                    if not overlap:
                        bin_rects.append((x, y, w, h))
                        placed = True
                        break
                    x += 1
                if placed:
                    break
                x = 0
                y += 1
            if placed:
                break

        # se não coube em nenhum bin, abre novo
        if not placed:
            bins.append([(0, 0, w, h)])

    # calcula perdas por bin
    for bin_rects in bins:
        area_ocupada = sum(w*h for (_, _, w, h) in bin_rects)
        perdas.append((area_bin - area_ocupada) ** 2)

    return sum(perdas) / len(bins)


# operador de motação: muda a orientação de um item selecionado aleatoriamente
def mutation(pmut, individuo):
    ordem, orientation = individuo   # desempacota corretamente

    # garante que orientation seja lista mutável
    orientation = list(orientation)

    # flip em orientação
    if random.random() < pmut:
        idx = random.randint(0, len(orientation) - 1)
        orientation[idx] = 1 - orientation[idx]

    return (ordem, orientation)


# Substitui o pior indivíduo da população se o filho for melhor
def replacement(pop, fitness, offspring, fitness_off):
    worst_idx = np.argmax(fitness)  # índice do pior (maior fitness)

    # Só substitui se o filho for melhor
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off

    return pop, fitness


# Construir os bins para plotar a solução obtida
def construir_bins(individuo, itens, largura_bin, altura_bin):
    ordem, orientation = individuo
    bins = []

    for item_id in ordem:
        w, h = itens[item_id]
        if orientation[item_id] == 1:
            w, h = h, w

        placed = False
        for bin in bins:
            for y in range(0, altura_bin - h + 1):
                for x in range(0, largura_bin - w + 1):
                    overlap = False
                    for item in bin["itens"]:
                        bx, by = item["posicao"]
                        bw, bh = item["dimensoes"]
                        if not (x + w <= bx or bx + bw <= x or
                                y + h <= by or by + bh <= y):
                            overlap = True
                            break
                    if not overlap:
                        bin["itens"].append({"posicao": (x, y),
                                             "dimensoes": (w, h)})
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break

        if not placed:
            bins.append({"itens": [{"posicao": (0, 0),
                                    "dimensoes": (w, h)}]})

    return bins

# Plota a melhor solução encontrada
def plot_best_solution(individuo, itens, largura_bin, altura_bin):
    bins = construir_bins(individuo, itens, largura_bin, altura_bin)

    for i, bin in enumerate(bins, start=1):
        fig, ax = plt.subplots(figsize=(6, 4))

        for item in bin["itens"]:
            x, y = item['posicao']
            w, h = item['dimensoes']

            rect = patches.Rectangle((x, y), w, h,
                                     edgecolor='black', facecolor='skyblue')
            ax.add_patch(rect)

            font_size = max(6, 0.3 * min(w, h))
            ax.text(x + w/2, y + h/2, f"{int(w)}x{int(h)}",
                    ha='center', va='center',
                    fontsize=font_size, color='black',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_xlim(0, largura_bin)
        ax.set_ylim(0, altura_bin)
        ax.set_title(f"Bin {i}")
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()

        plt.savefig(f"best_bin_{i}.png", dpi=150)
        plt.close()
