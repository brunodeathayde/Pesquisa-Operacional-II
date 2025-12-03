from numpy import loadtxt
import numpy as np
import matplotlib.pyplot as plt
import random

def vrppd_reading(file_name):
    data = loadtxt(file_name)
    return(data)

def flatten_routes(rotas):
    return [c for r in rotas for c in r]

# Constrói rotas viáveis para VRPSPD u
# Cada rota inicia com carga = soma das entregas dos clientes da rota.
# Retorna rotas, distância total e viabilidade.
def route_cost(clientes, P, capacidade):
    if not clientes:
        return [], 0.0, True

    todas_rotas = []
    rota_atual = []
    dist_total = 0.0
    viavel = True

    # Posição do depósito
    depo_x, depo_y = 0, 0
    
    # Para a primeira rota
    atual_x, atual_y = depo_x, depo_y  # Começa do depósito
    soma_entregas_rota = 0
    carga_atual = 0
    primeira_iteracao = True

     # SE vier como lista de listas
    if len(clientes) > 0 and isinstance(clientes[0], list):
        clientes = flatten_routes(clientes)

    for idx, cliente in enumerate(clientes):
        x, y, entrega, coleta = P[cliente - 1]
        
        # Verifica se cliente individualmente excede capacidade
        if entrega > capacidade or coleta > capacidade:
            viavel = False
            continue
            
        # Calcula carga necessária para este cliente na rota atual
        nova_soma_entregas = soma_entregas_rota + entrega
        
        # Verifica se pode adicionar à rota atual considerando:
        # 1. Capacidade inicial (soma das entregas)
        # 2. Capacidade ao longo da rota (carga atual + coletas)
        
        # Simula a rota atual com este cliente adicionado
        carga_simulada = nova_soma_entregas
        rota_simulada = rota_atual + [cliente]
        
        # Verifica se em algum ponto a carga excede a capacidade
        carga_maxima = nova_soma_entregas
        
        # Calcula carga máxima durante a rota simulada
        for c in rota_simulada:
            cx, cy, e, c = P[c - 1]
            carga_simulada = carga_simulada - e + c
            carga_maxima = max(carga_maxima, carga_simulada)
        
        # Se exceder a capacidade em qualquer ponto, fecha rota atual
        if nova_soma_entregas > capacidade or carga_maxima > capacidade:
            # Fecha rota atual (retorna ao depósito)
            if rota_atual:
                # Distância do último cliente ao depósito
                ultimo_cliente = rota_atual[-1]
                ult_x, ult_y, _, _ = P[ultimo_cliente - 1]
                dist_total += np.hypot(ult_x - atual_x, ult_y - atual_y)  # Última distância entre clientes
                dist_total += np.hypot(ult_x - depo_x, ult_y - depo_y)    # Volta ao depósito
                
                todas_rotas.append(rota_atual)
                
                # Inicia nova rota começando do depósito
                rota_atual = [cliente]
                soma_entregas_rota = entrega
                atual_x, atual_y = depo_x, depo_y  # Reinicia no depósito
                
                # Distância do depósito ao primeiro cliente da nova rota
                dist_total += np.hypot(x - atual_x, y - atual_y)
                atual_x, atual_y = x, y
            else:
                # Primeiro cliente da primeira rota (não deveria acontecer aqui)
                rota_atual = [cliente]
                soma_entregas_rota = entrega
                # Distância do depósito ao primeiro cliente
                dist_total += np.hypot(x - atual_x, y - atual_y)
                atual_x, atual_y = x, y
        else:
            # Pode adicionar à rota atual
            if not rota_atual:
                # Primeiro cliente da rota
                rota_atual.append(cliente)
                soma_entregas_rota = entrega
                # Distância do depósito ao primeiro cliente
                dist_total += np.hypot(x - atual_x, y - atual_y)
                atual_x, atual_y = x, y
            else:
                # Cliente adicional na rota
                dist_total += np.hypot(x - atual_x, y - atual_y)
                rota_atual.append(cliente)
                soma_entregas_rota = nova_soma_entregas
                atual_x, atual_y = x, y
    
    # Fecha última rota
    if rota_atual:
        # Distância do último cliente ao depósito
        ultimo_cliente = rota_atual[-1]
        ult_x, ult_y, _, _ = P[ultimo_cliente - 1]
        
        # Se houver mais de um cliente na rota, já temos a última distância entre clientes
        if len(rota_atual) > 1:
            # A última distância entre clientes já foi adicionada no loop
            # Só precisa adicionar o retorno ao depósito
            dist_total += np.hypot(ult_x - depo_x, ult_y - depo_y)
        else:
            # Para rota com apenas um cliente
            # A distância do depósito ao cliente já foi adicionada
            # Só precisa do retorno ao depósito
            dist_total += np.hypot(ult_x - depo_x, ult_y - depo_y)
            
        todas_rotas.append(rota_atual)
    
    # Verifica viabilidade final de todas as rotas
    for rota in todas_rotas:
        if not rota:
            continue
            
        # Calcula soma das entregas (carga inicial)
        soma_entregas = sum(P[cliente-1][2] for cliente in rota)
        
        # Verifica se excede capacidade
        if soma_entregas > capacidade:
            viavel = False
            break
        
        # Simula a rota para verificar capacidade ao longo do percurso
        carga_atual = soma_entregas
        for cliente in rota:
            _, _, entrega, coleta = P[cliente-1]
            carga_atual = carga_atual - entrega + coleta
            
            # Verifica se carga fica negativa (impossível)
            if carga_atual < 0:
                viavel = False
                break
            
            # Verifica se excede capacidade
            if carga_atual > capacidade:
                viavel = False
                break
    
    return todas_rotas, dist_total, viavel


# Função auxiliar para calcular distância de uma rota específica
def calcular_distancia_rota(rota, P):
    if not rota:
        return 0.0
    
    dist = 0.0
    depo_x, depo_y = 0, 0
    
    # Primeiro cliente
    x1, y1, _, _ = P[rota[0] - 1]
    dist += np.hypot(x1 - depo_x, y1 - depo_y)
    
    # Clientes intermediários
    for i in range(len(rota) - 1):
        x1, y1, _, _ = P[rota[i] - 1]
        x2, y2, _, _ = P[rota[i + 1] - 1]
        dist += np.hypot(x2 - x1, y2 - y1)
    
    # Último cliente de volta ao depósito
    x_last, y_last, _, _ = P[rota[-1] - 1]
    dist += np.hypot(x_last - depo_x, y_last - depo_y)
    
    return dist

# Aplica uma perturbação em uma solução  para ILS.
# Seleciona um trecho proporcional ao parâmetro 'intensidade' e embaralha.
# Garante que o trecho embaralhado seja diferente do original.
def perturbation(route, intensidade):
    n = len(route)
    tamanho_trecho = max(1, int(n * intensidade))
    inicio = random.randint(0, n - tamanho_trecho)
    fim = inicio + tamanho_trecho

    new_route = route[:]
    trecho = new_route[inicio:fim]

    # Garante que o shuffle produza algo diferente
    nova_ordem = trecho[:]
    while True:
        random.shuffle(nova_ordem)
        if nova_ordem != trecho:
            break

    new_route[inicio:fim] = nova_ordem
    return new_route

# Busca local 2-opt
def two_opt_pdvrp(rota, P, capacidade):
    melhor_rota = rota[:]
    melhor_rota, melhor_custo, viavel = route_cost(melhor_rota, P, capacidade)
    melhorou = True

    while melhorou:
        melhorou = False

        for i in range(1, len(melhor_rota) - 2):
            for j in range(i + 1, len(melhor_rota) - 1):

                if j - i == 1:
                    continue

                nova_rota = (
                    melhor_rota[:i] +
                    melhor_rota[i:j][::-1] +
                    melhor_rota[j:]
                )

                nova_rota, novo_custo, viavel = route_cost(nova_rota, P, capacidade)

                # só aceita se viável e melhor
                if viavel and novo_custo < melhor_custo:
                    melhor_rota = nova_rota
                    melhor_custo = novo_custo
                    melhorou = True

    return melhor_rota, melhor_custo

# Plota rotas do VRPSPD
def plotting_route_pick_up_and_delivery(P, rotas_input, capacidade):
    # Tratamento do input
    rotas_para_plotar = []
    
    if isinstance(rotas_input, tuple):
        # Se for uma tupla, extrai a lista de rotas
        # Verifica diferentes formatos possíveis
        if len(rotas_input) == 3:
            # Formato 1: (dist_total, viavel, rotas)
            dist, viavel, rotas = rotas_input
            print(f"Distância: {dist:.2f}, Viável: {viavel}")
            rotas_para_plotar = rotas
        elif len(rotas_input) == 2:
            # Formato 2: (rotas, dist_total)
            rotas, dist = rotas_input
            rotas_para_plotar = rotas
    elif isinstance(rotas_input, list):
        # Já é uma lista
        if len(rotas_input) > 0 and isinstance(rotas_input[0], list):
            # É uma lista de rotas: [[rota1], [rota2], ...]
            rotas_para_plotar = rotas_input
        elif len(rotas_input) > 0 and isinstance(rotas_input[0], int):
            # É uma única rota: [cliente1, cliente2, ...]
            rotas_para_plotar = [rotas_input]
        else:
            # Caso especial: [rotas] onde rotas já é lista de listas
            if len(rotas_input) == 1 and isinstance(rotas_input[0], list):
                if len(rotas_input[0]) > 0 and isinstance(rotas_input[0][0], list):
                    rotas_para_plotar = rotas_input[0]
                else:
                    rotas_para_plotar = rotas_input
    else:
        print(f"ERRO: Formato não reconhecido: {type(rotas_input)}")
        return
    
    # Agora temos rotas_para_plotar corretamente
    print(f"Plotando {len(rotas_para_plotar)} rotas: {rotas_para_plotar}")
    
    # Configuração do plot
    cores = ['red', 'blue', 'green', 'orange', 'purple', 
             'brown', 'pink', 'gray', 'olive', 'cyan']
    
    plt.figure(figsize=(12, 10))
    
    # Depósito
    plt.plot(0, 0, 's', markersize=15, color='black', markeredgewidth=2, 
             label="Depósito", zorder=5)
    
    # Plota todos os clientes
    for i, (x, y, entrega, coleta) in enumerate(P, start=1):
        plt.plot(x, y, 'o', markersize=10, color='blue', zorder=3)
        plt.text(x, y + 1, f'{i}\n(e:{entrega}, c:{coleta})', 
                fontsize=9, ha='center', va='bottom', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
    
    # Plota cada rota
    for rota_idx, rota in enumerate(rotas_para_plotar, start=1):
        cor = cores[(rota_idx - 1) % len(cores)]
        
        # Inicializa com depósito
        x_rota = [0]
        y_rota = [0]
        
        # Calcula carga inicial (soma das entregas)
        carga_inicial = 0
        if rota:  # Verifica se rota não está vazia
            for cliente in rota:
                idx = cliente - 1
                _, _, entrega, _ = P[idx]
                carga_inicial += entrega
        
        # Adiciona pontos da rota
        for cliente in rota:
            idx = cliente - 1
            x, y, _, _ = P[idx]
            x_rota.append(x)
            y_rota.append(y)
        
        # Retorno ao depósito
        x_rota.append(0)
        y_rota.append(0)
        
        # Plota a linha da rota
        plt.plot(x_rota, y_rota, color=cor, linewidth=2.5, 
                label=f"Rota {rota_idx} (clientes: {len(rota)}, carga inicial: {carga_inicial}/{capacidade})",
                zorder=1, alpha=0.8)
        
        # Plota setas de direção
        for j in range(len(x_rota) - 1):
            if x_rota[j] != x_rota[j + 1] or y_rota[j] != y_rota[j + 1]:
                dx = x_rota[j + 1] - x_rota[j]
                dy = y_rota[j + 1] - y_rota[j]
                plt.arrow(x_rota[j], y_rota[j], dx * 0.8, dy * 0.8,
                         head_width=0.5, head_length=0.5,
                         fc=cor, ec=cor, alpha=0.6, zorder=2)
    
    # Configurações do gráfico
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    
    # Adiciona grade
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Configura eixos iguais
    plt.axis('equal')
    
    # Legenda fora do gráfico
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0, fontsize=10)
    
    # Ajusta layout
    plt.tight_layout()
    
    # Mostra o gráfico
    plt.show()
