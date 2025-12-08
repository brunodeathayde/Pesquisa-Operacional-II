from numpy import loadtxt
import math
import matplotlib.pyplot as plt
import random
import numpy as np

# Leitura da instância
def tsp_reading(file_name):
    data = loadtxt(file_name)
    return(data)

# Cálculo da matriz de distâncias
def distance_matrix(n, P):
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = P[i][0] - P[j][0]
            dy = P[i][1] - P[j][1]
            D[i][j] = math.sqrt(dx*dx + dy*dy)
    return D

# Cálculo da função objetivo
def objective_function_tsp(n, route, D):
    dist = 0
    for i in range(n-1):
        dist += D[route[i]][route[i+1]]
    dist += D[route[-1]][route[0]]  # fecha o ciclo
    return dist

# Busca local 2-opt best improvement
def two_opt_best_improvement(n, route, best_dist, D):
    route = list(route)  # garante que é lista
    for i in range(n - 1):
        for j in range(i + 2, n): 
            if i == 0 and j == n - 1:
                continue  
            # custo antes
            a, b = route[i], route[i + 1]
            c, d = route[j], route[(j + 1) % n]
            old_cost = D[a][b] + D[c][d]
            new_cost = D[a][c] + D[b][d]
            new_dist = best_dist - old_cost + new_cost
            if new_dist < best_dist:                
                route[i + 1 : j + 1] = list(reversed(route[i + 1 : j + 1]))
                best_dist = new_dist

    return route, best_dist

# Vizinhanças para o TSP

# Trocar dois nós da rota (swap simples entre duas posições aleatórias)
def node_exchange(route):
    p1 = random.sample(range(len(route)), 2)  # seleciona duas posições distintas
    route[p1[0]], route[p1[1]] = route[p1[1]], route[p1[0]]  # troca os nós
    return route

# Inserir um nó em nova posição da rota (pega um nó e move para o início)
def node_insertion(route):
    n = len(route)
    k = random.randint(1, n-1)  # escolhe um nó aleatório (exceto o primeiro)
    route.insert(0, route[k])   # insere esse nó na primeira posição
    del route[k+1]              # remove a duplicata criada
    return route

# Troca de série de nós (divide a rota em duas partes e inverte a ordem delas)
def node_series_exchange(route):
    n = len(route)
    k = random.randint(1, n-2)  # ponto de corte aleatório
    part1 = route[:k+1]         # primeira parte da rota
    part2 = [x for x in route if x not in part1]  # segunda parte (restante)
    return part2 + part1        # concatena invertendo a ordem das partes

# Movimento de série (move um bloco de 4 nós para o início da rota)
def node_series_move_one(route):
    n = len(route)
    k = random.randint(1, n-5)  # posição inicial do bloco
    block = route[k+1:k+5]      # bloco de 4 nós consecutivos
    rest = [x for x in route if x not in block]  # restante da rota
    return block + rest         # coloca o bloco no início

# Movimento de série (move um bloco de 4 nós para o final da rota)
def node_series_move_two(route):
    n = len(route)
    k = random.randint(1, n-5)  # posição inicial do bloco
    block = route[k+1:k+5]      # bloco de 4 nós consecutivos
    rest = [x for x in route if x not in block]  # restante da rota
    return rest + block         # coloca o bloco no final

# Movimento shift (inserção de bloco de nós em posição aleatória)
def node_shift(route, block_size=3):
    n = len(route)
    if block_size >= n:         # se o bloco for maior que a rota, não faz nada
        return route
    start = random.randint(0, n - block_size)  # posição inicial do bloco
    block = route[start:start+block_size]      # bloco de nós consecutivos
    rest = route[:start] + route[start+block_size:]  # restante da rota
    insert_pos = random.randint(0, len(rest))  # nova posição para inserir o bloco
    return rest[:insert_pos] + block + rest[insert_pos:]  # insere o bloco

# Fase de construção GRASP
def construction_phase_tsp(alpha, matriz_dist):
    n = len(matriz_dist) # número de cidades
    cidades_restantes = set(range(1, n)) # todas exceto a cidade inicial (0)
    rota = [0] # começa na cidade 0
    atual = 0

    while cidades_restantes:
        # calcula distâncias para cidades restantes
        distancias = [(c, matriz_dist[atual][c]) for c in cidades_restantes]
        custos = [d for _, d in distancias]
        cmin, cmax = min(custos), max(custos)

        # cria lista de candidatos restrita (RCL)
        limite = cmin + alpha * (cmax - cmin)
        rcl = [c for c, d in distancias if d <= limite]

        if not rcl:
            break

        # escolhe aleatoriamente uma cidade da RCL
        candidato = random.choice(rcl)
        rota.append(candidato)
        atual = candidato
        cidades_restantes.remove(candidato)

    # fecha o ciclo voltando à cidade inicial
    rota.append(0)
    return rota

# Plotando rota obtida
def plotting_route(n, s, P):
    # Remove duplicatas mantendo a ordem
    seen = set()
    s_clean = []
    for v in s:
        if v not in seen:
            s_clean.append(v)
            seen.add(v)

    # Se tiver menos de n vértices, não há como consertar corretamente
    if len(s_clean) < n:
        raise ValueError("Rota possui menos vértices do que o necessário.")

    # Se tiver mais vértices, reduz para n+1 no máximo
    if len(s_clean) > n + 1:
        s_clean = s_clean[:n+1]

    # Se for permutação de tamanho n → rota aberta → FECHAR apenas no plot
    if len(s_clean) == n:
        route = s_clean + [s_clean[0]]   # fecha
    else:
        # Se veio rota n+1, mas não está fechada → fecha
        route = s_clean
        if route[0] != route[-1]:
            route[-1] = route[0]

    # Garantia final
    assert len(route) == n + 1
    assert set(route[:-1]) == set(range(n))

    # --- Plotagem ---
    for i in range(n):
        plt.scatter(P[i][0], P[i][1], color='red', s=30)
        plt.text(P[i][0] + 0.01, P[i][1] + 0.01, str(i), fontsize=9)

    for i in range(len(route) - 1):
        x = [P[route[i]][0], P[route[i+1]][0]]
        y = [P[route[i]][1], P[route[i+1]][1]]
        plt.plot(x, y, color='blue')

    plt.title("Rota obtida")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.show()
