import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Leitura da instância
def read_instance_rcpsp(file_name):
    """
    Lê uma instância RCPSP em formato texto.
    Retorna:
      - n_activities: número de atividades
      - n_resources: número de recursos
      - resource_capacities: lista com capacidades dos recursos
      - activities: dicionário com dados das atividades
    """
    activities = {}

    with open(file_name, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Cabeçalho
    n_activities = int(lines[0].split("=")[1].strip())
    n_resources = int(lines[1].split("=")[1].strip())
    resource_capacities = list(eval(lines[2].split("=")[1].strip()))  # Convertido para lista

    # Atividades
    for line in lines[3:]:
        parts = line.split()
        act_id = int(parts[0])
        duration = int(parts[1])
        resources = list(map(int, parts[2:2+n_resources]))
        
        # CORREÇÃO: O índice para predecessores estava errado
        preds_raw = parts[2+n_resources] if len(parts) > 2+n_resources else "-"
        if preds_raw == "-":
            predecessors = []
        else:
            predecessors = list(map(int, preds_raw.split(",")))

        activities[act_id] = {
            "duration": duration,
            "resources": resources,
            "predecessors": predecessors
        }

    return n_activities, n_resources, resource_capacities, activities

# Geração da população inicial de forma aletatória
def genpop_rcpsp(pop_size, activities):
    """
    Gera população inicial para RCPSP.
    Cada indivíduo é uma lista de atividades (activity list) válida.
    
    :param pop_size: tamanho da população
    :param activities: dicionário {id: {"predecessors": [...], "duration":..., "resources":[...]}}
    :return: população como lista de listas
    """
    pop = []
    n_nodes = len(activities)

    for _ in range(pop_size):
        # lista de atividades ainda não inseridas
        remaining = set(activities.keys())
        individuo = []

        while remaining:
            # atividades candidatas: sem predecessores pendentes
            candidatos = [a for a in remaining if all(p in individuo for p in activities[a]["predecessors"])]
            
            # escolhe aleatoriamente uma das candidatas
            escolhido = random.choice(candidatos)
            individuo.append(escolhido)
            remaining.remove(escolhido)

        pop.append(individuo)

    return np.array(pop, dtype=object)  # dtype=object para arrays de diferentes tamanhos

# Gera o cronograma a partir de uma lista de atividades. Retorna o makespan.
def schedule_generation(individuo, activities, resource_capacities):
    n_resources = len(resource_capacities)

    # Linha do tempo de uso dos recursos (vai crescendo conforme necessário)
    resource_usage = []  # cada posição é um vetor: [r0_used, r1_used, ..., rk_used]

    schedule = {}

    for act in individuo:
        duration = activities[act]["duration"]
        needed = activities[act]["resources"]
        preds = activities[act]["predecessors"]

        # earliest start
        est = 0
        if preds:
            est = max(schedule[p]["end"] for p in preds)

        t = est

        # busca tempo viável
        while True:
            # garante timeline longa o suficiente
            while len(resource_usage) <= t + duration:
                resource_usage.append([0] * n_resources)

            # verifica recursos durante todo o intervalo
            feasible = True
            for tau in range(t, t + duration):
                for r in range(n_resources):
                    if resource_usage[tau][r] + needed[r] > resource_capacities[r]:
                        feasible = False
                        break
                if not feasible:
                    break

            if feasible:
                break
            else:
                t += 1

        # aloca recursos
        for tau in range(t, t + duration):
            for r in range(n_resources):
                resource_usage[tau][r] += needed[r]

        schedule[act] = {"start": t, "end": t + duration}

    makespan = max(schedule[a]["end"] for a in schedule)
    return makespan

# Calcula a aptidão da população
def fitness_population(pop, activities, resource_capacities):
    fitness = []
    for individuo in pop:
        try:
            makespan = schedule_generation(individuo, activities, resource_capacities)
            fitness.append(makespan)
        except Exception:
            fitness.append(float("inf"))  # solução inválida
    return np.array(fitness)

# Operador de seleção por torneio binário
def selection(pop_size, fitness):
    candidates = np.random.permutation(pop_size)[:4]
    parent1 = candidates[0] if fitness[candidates[0]] < fitness[candidates[1]] else candidates[1]
    parent2 = candidates[2] if fitness[candidates[2]] < fitness[candidates[3]] else candidates[3]
    return parent1, parent2

# Precedence Preserving Crossover para RCPSP. Garante que o filho respeita todas as precedências.
def ppc_crossover(parent1, parent2, activities):
    n = len(parent1)
    offspring = []
    used = set()

    # enquanto ainda houver genes para escolher
    while len(offspring) < n:
        # candidatos válidos: não usados e todos predecessores já no offspring
        candidates = []
        for a in parent1:
            if a not in used:
                preds = activities[a]["predecessors"]
                if all(p in offspring for p in preds):
                    candidates.append(a)

        # Se não encontrar candidatos no pai1, tenta no pai2
        if not candidates:
            for a in parent2:
                if a not in used:
                    preds = activities[a]["predecessors"]
                    if all(p in offspring for p in preds):
                        candidates.append(a)

        if not candidates:
            raise RuntimeError("Nenhum candidato válido encontrado (crossover inválido).")

        # escolha determina qual pai guia
        if len(offspring) % 2 == 0:
            # segue ordem do pai 1
            for a in parent1:
                if a in candidates:
                    chosen = a
                    break
        else:
            # segue ordem do pai 2
            for a in parent2:
                if a in candidates:
                    chosen = a
                    break

        offspring.append(chosen)
        used.add(chosen)

    return offspring

# Mutação por swap, garantindo que a lista permaneça válida.
def mutation_swap(prob_mut, offspring, activities):
    if random.random() <= prob_mut:
        n = len(offspring)
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            idx1, idx2 = random.sample(range(n), 2)
            
            # Verifica se o swap mantém a validade das precedências
            temp = offspring.copy()
            temp[idx1], temp[idx2] = temp[idx2], temp[idx1]
            
            # Verifica validade
            valid = True
            for i, act in enumerate(temp):
                preds = activities[act]["predecessors"]
                for p in preds:
                    if p in temp[:i]:  # predecessor deve aparecer antes
                        continue
                    else:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                offspring = temp
                break
            attempts += 1
    
    return offspring

# Avalia o fitness de um único indivíduo (offspring) para RCPSP.
def fitness_offspring(individuo, activities, resource_capacities):
    try:
        makespan = schedule_generation(individuo, activities, resource_capacities)
        return makespan
    except Exception:
        return float("inf")  # solução inválida

#  Substitui o pior indivíduo.
def replacement(pop, fitness, offspring, fitness_off, activities, resource_capacities):
    # Avalia fitness da população atualizada se necessário
    if len(fitness) != len(pop):
        fitness = fitness_population(pop, activities, resource_capacities)
    
    worst_idx = np.argmax(fitness)  # pior = maior valor
    
    # Só substitui se o filho gerado for melhor que o pior
    if fitness_off < fitness[worst_idx]:
        pop[worst_idx] = offspring
        fitness[worst_idx] = fitness_off
    
    return pop, fitness
    
#  Igual ao schedule_generation, mas retorna também o dicionário de schedule.
def build_schedule(individuo, activities, resource_capacities):
    n_resources = len(resource_capacities)
    resource_usage = []
    schedule = {}

    for act in individuo:
        duration = activities[act]["duration"]
        needed = activities[act]["resources"]
        preds = activities[act]["predecessors"]

        est = 0
        if preds:
            est = max(schedule[p]["end"] for p in preds)

        t = est
        while True:
            while len(resource_usage) <= t + duration:
                resource_usage.append([0] * n_resources)

            feasible = True
            for tau in range(t, t + duration):
                for r in range(n_resources):
                    if resource_usage[tau][r] + needed[r] > resource_capacities[r]:
                        feasible = False
                        break
                if not feasible:
                    break

            if feasible:
                break
            else:
                t += 1

        for tau in range(t, t + duration):
            for r in range(n_resources):
                resource_usage[tau][r] += needed[r]

        schedule[act] = {"start": t, "end": t + duration, "duration": duration}

    makespan = max(schedule[a]["end"] for a in schedule)
    return schedule, resource_usage, makespan

# Plota diagrama de Gantt a partir de um dicionário {act_id: {start, end, duration}}.
def plot_gantt(schedule, title="RCPSP - Gantt chart"):
    # Ordena por início
    tasks = sorted(schedule.items(), key=lambda kv: kv[1]["start"])
    ids = [f"A{act_id}" for act_id, _ in tasks]
    starts = [data["start"] for _, data in tasks]
    durations = [data["duration"] for _, data in tasks]

    fig, ax = plt.subplots(figsize=(10, max(4, len(tasks) * 0.4)))
    y_pos = np.arange(len(tasks))

    ax.barh(y_pos, durations, left=starts, height=0.6, color="#69b3a2", edgecolor="black")

    # Rótulos
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ids)
    ax.invert_yaxis()  # atividade no topo começa primeiro
    ax.set_xlabel("Time")
    ax.set_title(title)

    # Grade leve
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

# Plota o uso de cada recurso ao longo do tempo comparando com a capacidade.
def plot_resource_usage(resource_usage, resource_capacities, title="Resource usage over time"):
    time = np.arange(len(resource_usage))
    usage = np.array(resource_usage)  # shape: (T, R)

    fig, ax = plt.subplots(len(resource_capacities), 1, figsize=(10, 2.5 * len(resource_capacities)), sharex=True)
    if len(resource_capacities) == 1:
        ax = [ax]

    for r, capacity in enumerate(resource_capacities):
        ax[r].plot(time, usage[:, r], label=f"Resource {r} usage", color="#3366cc")
        ax[r].hlines(capacity, xmin=time[0], xmax=time[-1], colors="red", linestyles="--", label="Capacity")
        ax[r].set_ylabel("Units")
        ax[r].grid(True, linestyle="--", alpha=0.4)
        # legenda fora do gráfico (à direita)
        ax[r].legend(loc="center left", bbox_to_anchor=(1, 0.5))
    
    ax[-1].set_xlabel("Time")
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

# Exemplo de uso dentro do algoritmo
def evolutionary_algorithm_rcpsp(file_name, pop_size=50, generations=100, prob_mut=0.1):
    """
    Algoritmo evolucionário completo para RCPSP.
    """
    # Lê instância
    n_activities, n_resources, resource_capacities, activities = read_instance_rcpsp(file_name)
    
    # Gera população inicial
    pop = genpop_rcpsp(pop_size, activities)
    
    # Avalia fitness inicial
    fitness = fitness_population(pop, activities, resource_capacities)
    
    # Loop evolucionário
    for gen in range(generations):
        parent1_idx, parent2_idx = selection(pop_size, fitness)
        parent1 = pop[parent1_idx]
        parent2 = pop[parent2_idx]
        offspring = ppc_crossover(parent1, parent2, activities)
        offspring = mutation_swap(prob_mut, offspring, activities)
        fitness_off = fitness_offspring(offspring, activities, resource_capacities)
        pop, fitness = replacement(pop, fitness, offspring, fitness_off, activities, resource_capacities)
        
        if gen % 10 == 0:
            print(f"Generation {gen}: Best fitness = {np.min(fitness)}")
    
    # Melhor solução
    best_idx = np.argmin(fitness)
    best_solution = pop[best_idx]
    best_makespan = fitness[best_idx]
    
    print(f"\nBest solution found: Makespan = {best_makespan}")
    #print(f"Activity order: {best_solution}")
    
    #  Plotar solução
    # plot_solution(best_solution, activities)
    
    return best_solution, best_makespan


