import numpy as np
import matplotlib.pyplot as plt
import copy
import random

# Cáclulo da matriz de distâncias
def distance_matrix(deposito, entrega, clientes):
    pontos = np.vstack([deposito, entrega, clientes])
    
    n = len(pontos)
    matriz_dist = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = pontos[i, 0] - pontos[j, 0]
                dy = pontos[i, 1] - pontos[j, 1]
                matriz_dist[i, j] = np.sqrt(dx**2 + dy**2)
    
    return matriz_dist

# Fase de construção GRASP
def construction_phase(alpha, capacidade, matriz_dist, demandas):
    n_clientes = len(demandas)
    clientes_restantes = set(range(2, n_clientes+2))  # índices dos clientes
    rotas = []
    
    while clientes_restantes:
        carga = 0
        rota = [0]  # começa no depósito
        atual = 0
        
        while clientes_restantes:
            # calcula distâncias para clientes restantes
            distancias = [(c, matriz_dist[atual, c]) for c in clientes_restantes]
            custos = [d for _, d in distancias]
            cmin, cmax = min(custos), max(custos)
            
            # cria lista de candidatos restrita (RCL)
            limite = cmin + alpha * (cmax - cmin)
            rcl = [c for c, d in distancias if d <= limite]
            
            if not rcl:
                break
            
            # escolhe aleatoriamente um cliente da RCL
            candidato = random.choice(rcl)
            
            # verifica capacidade
            if carga + demandas[candidato-2] <= capacidade:
                rota.append(candidato)
                carga += demandas[candidato-2]
                atual = candidato
                clientes_restantes.remove(candidato)
            else:
                break
        
        # fecha rota no ponto de entrega final
        rota.append(1)
        rotas.append(rota)
    
    return rotas

# Cálculo do custo de uma rota individual
def cost_route(rota, matriz_dist):
    custo_total = 0
    for i in range(len(rota)-1):
        custo_total += matriz_dist[int(rota[i]), int(rota[i+1])]
    return custo_total

# Cálculo da dist6ancia total de todas as rotas
def cost_solution(rotas, matriz_dist):
    return sum(cost_route(r, matriz_dist) for r in rotas)

# Plotar rotas
def plot_routes(rotas, deposito, entrega, clientes):
    pontos = np.vstack([deposito, entrega, clientes])
    
    plt.figure(figsize=(8, 6))
    
    # Plota depósito
    plt.scatter(deposito[0], deposito[1], c='green', marker='s', s=200, label='Depósito (0)')
    
    # Plota entrega final
    plt.scatter(entrega[0], entrega[1], c='red', marker='*', s=200, label='Entrega (1)')
    
    # Plota clientes
    plt.scatter(clientes[:,0], clientes[:,1], c='blue', marker='o', s=100, label='Clientes (2..N)')
    
    # Plota rotas
    cores = [
    'orange', 'purple', 'cyan', 'magenta', 'brown', 'gray',
    'red', 'blue', 'green', 'yellow', 'pink', 'olive',
    'teal', 'navy', 'gold', 'lime', 'indigo', 'coral',
    'turquoise', 'maroon', 'violet', 'darkgreen', 'darkblue'
]
    for i, rota in enumerate(rotas):
        cor = cores[i % len(cores)]
        xs = [pontos[n][0] for n in rota]
        ys = [pontos[n][1] for n in rota]
        plt.plot(xs, ys, color=cor, linewidth=2, label=f'Rota {i+1}')
    
    # Ajustes finais
    plt.xlabel("X")
    plt.ylabel("Y")
    #plt.title("Rotas do OVRP")
    plt.grid(True)
    
    # Legenda fora da área útil
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.show()

# Cálculo da carga total de uma rota
def demanda_rota(rota, demandas):
    return sum(demandas[c-2] for c in rota if c >= 2)

# Movimento de realocação: pega um cliente de uma rota e insere em outra
# rota com capacidade disponível.
def reallocation(rotas, capacidade, demandas, matriz_dist):
    nova_solucao = copy.deepcopy(rotas)

    # escolhe uma rota origem e um cliente dela (não depósito nem entrega)
    rota_origem = random.choice([r for r in nova_solucao if len(r) > 2])
    cliente = random.choice([c for c in rota_origem if c not in (0,1)])

    # remove cliente da rota origem
    rota_origem.remove(cliente)

    # escolhe rota destino com capacidade disponível
    rotas_destino = [r for r in nova_solucao 
                     if demanda_rota(r, demandas) + demandas[cliente-2] <= capacidade]
    if not rotas_destino:
        return nova_solucao  # não há rota viável

    rota_destino = random.choice(rotas_destino)

    # insere cliente em posição aleatória da rota destino (antes do ponto de entrega final)
    pos = random.randint(1, len(rota_destino)-1)
    rota_destino.insert(pos, cliente)

    return nova_solucao

# Movimento de troca: seleciona dois clientes de rotas diferentes e troca-os,
#    respeitando a capacidade dos veículos.
def swap(rotas, capacidade, demandas, matriz_dist):
    nova_solucao = copy.deepcopy(rotas)

    # escolhe duas rotas diferentes com pelo menos um cliente cada
    rotas_validas = [r for r in nova_solucao if len(r) > 2]
    if len(rotas_validas) < 2:
        return nova_solucao

    rota1, rota2 = random.sample(rotas_validas, 2)
    cliente1 = random.choice([c for c in rota1 if c not in (0,1)])
    cliente2 = random.choice([c for c in rota2 if c not in (0,1)])

    # verifica capacidade após troca
    carga1 = demanda_rota(rota1, demandas) - demandas[cliente1-2] + demandas[cliente2-2]
    carga2 = demanda_rota(rota2, demandas) - demandas[cliente2-2] + demandas[cliente1-2]

    if carga1 <= capacidade and carga2 <= capacidade:
        # realiza troca
        idx1 = rota1.index(cliente1)
        idx2 = rota2.index(cliente2)
        rota1[idx1], rota2[idx2] = cliente2, cliente1

    return nova_solucao

# Aplicação do 2-opt em uma rota individual para o open vehicle routing problem.
def two_opt_route(rota, matriz_dist):
    melhor_rota = rota
    melhor_custo = cost_route(rota, matriz_dist)
    melhorou = True

    while melhorou:
        melhorou = False
        for i in range(1, len(melhor_rota) - 2):   # não mexe no depósito (0)
            for j in range(i+1, len(melhor_rota) - 1):  # não mexe no delivery (1)
                if j - i == 1:  # evita troca de vizinhos consecutivos
                    continue
                nova_rota = melhor_rota[:i] + melhor_rota[i:j][::-1] + melhor_rota[j:]
                novo_custo = cost_route(nova_rota, matriz_dist)
                if novo_custo < melhor_custo:
                    melhor_rota = nova_rota
                    melhor_custo = novo_custo
                    melhorou = True
    return melhor_rota