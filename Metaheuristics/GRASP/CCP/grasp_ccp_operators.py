import numpy as np
import copy
import random
import matplotlib.pyplot as plt


# Leitura de instância para o problema de agrupamento capacitado (CCP)
def ccp_reading(file_name):
    with open(file_name, "r") as f:
        # primeira linha = número de clusters e número de clientes
        p, n = map(int, f.readline().strip().split())
        
        # ignorar linha de comentário "# Clientes"
        f.readline()
        
        # carregar clientes
        clientes = []
        for _ in range(n):
            x, y, d = map(int, f.readline().strip().split())
            clientes.append((x, y, d))
        
        # ignorar linha de comentário "# Clusters"
        f.readline()
        
        # carregar clusters
        clusters = []
        for _ in range(p):
            x, y, c = map(int, f.readline().strip().split())
            clusters.append((x, y, c))
    
    # converter para numpy arrays para facilitar cálculos
    clientes = np.array(clientes) # formato: [ [x,y,d], ... ]
    clusters = np.array(clusters) # formato: [ [x,y,c], ... ]
    
    return p, n, clientes, clusters

# Cálculo da matriz de distâncias cliente–cluster para o CCP
def distance_matrix_ccp(clientes, clusters):
    n = clientes.shape[0]
    p = clusters.shape[0]
    
    matriz_dist = np.zeros((n, p))
    
    for i in range(n):
        for j in range(p):
            dx = clientes[i, 0] - clusters[j, 0]
            dy = clientes[i, 1] - clusters[j, 1]
            matriz_dist[i, j] = np.sqrt(dx**2 + dy**2)
    
    return matriz_dist


# Cálculo do custo da solução
def cost_solution_ccp(solution, dist_matrix):
    total_cost = 0.0
    for cliente_idx, cluster_idx in enumerate(solution):
        total_cost += dist_matrix[cliente_idx, cluster_idx]
    return total_cost

# Fase de construção GRASP para o problema de agrupamento capacitado (CCP)
def construction_phase_ccp(alpha, matriz_dist, demandas, capacidades):
    n_clientes = len(demandas)
    p_clusters = len(capacidades)
    
    # capacidade residual de cada cluster
    capacidade_residual = list(capacidades)
    
    # solução inicial (não atribuído = -1)
    solucao = [-1] * n_clientes
    
    # clientes restantes
    clientes_restantes = set(range(n_clientes))
    
    while clientes_restantes:
        cliente = clientes_restantes.pop()
        
        # distâncias desse cliente para todos os clusters
        distancias = [(j, matriz_dist[cliente, j]) for j in range(p_clusters)]
        custos = [d for _, d in distancias]
        cmin, cmax = min(custos), max(custos)
        
        # cria lista de candidatos restrita (RCL)
        limite = cmin + alpha * (cmax - cmin)
        rcl = [j for j, d in distancias if d <= limite]
        
        # filtra clusters viáveis (capacidade suficiente)
        rcl_viavel = [j for j in rcl if capacidade_residual[j] >= demandas[cliente]]
        
        if not rcl_viavel:
            # fallback: escolher qualquer cluster com capacidade suficiente
            candidatos = [j for j in range(p_clusters) if capacidade_residual[j] >= demandas[cliente]]
            if not candidatos:
                raise ValueError("Instância inviável: cliente não pode ser alocado em nenhum cluster.")
            escolhido = random.choice(candidatos)
        else:
            # escolhe aleatoriamente da RCL viável
            escolhido = random.choice(rcl_viavel)
        
        # atribui cliente ao cluster escolhido
        solucao[cliente] = escolhido
        capacidade_residual[escolhido] -= demandas[cliente]
    
    return solucao

# Movimento de realocação para o problema de agrupamento capacitado (CCP)
def reallocation_ccp(solucao, demandas, capacidades, matriz_dist):
    n_clientes = len(demandas)
    p_clusters = len(capacidades)
    
    # capacidade residual atual
    capacidade_residual = list(capacidades)
    for i in range(n_clientes):
        capacidade_residual[solucao[i]] -= demandas[i]
    
    nova_solucao = copy.deepcopy(solucao)
    
    # escolhe cliente aleatório
    cliente = random.randint(0, n_clientes-1)
    cluster_origem = nova_solucao[cliente]
    
    # clusters candidatos (com capacidade suficiente para receber o cliente)
    candidatos = [j for j in range(p_clusters) 
                  if j != cluster_origem and capacidade_residual[j] >= demandas[cliente]]
    
    if not candidatos:
        return nova_solucao # não há realocação viável
    
    # cria lista de candidatos restrita (RCL) com base nas distâncias
    distancias = [(j, matriz_dist[cliente, j]) for j in candidatos]
    custos = [d for _, d in distancias]
    cmin, cmax = min(custos), max(custos)
    limite = cmin + 0.3 * (cmax - cmin) # alpha fixo, pode ser parâmetro
    rcl = [j for j, d in distancias if d <= limite]
    
    if not rcl:
        return nova_solucao
    
    # escolhe cluster destino da RCL
    cluster_destino = random.choice(rcl)
    
    # atualiza solução
    nova_solucao[cliente] = cluster_destino
    
    return nova_solucao


# Busca local - Movimento de troca (swap) + 2-opt: tenta trocar clientes entre clusters diferentes
def swap_ccp(solucao, demandas, capacidades, matriz_dist):
    n_clientes = len(demandas)
    p_clusters = len(capacidades)
    
    # capacidade residual atual
    capacidade_residual = list(capacidades)
    for i in range(n_clientes):
        capacidade_residual[solucao[i]] -= demandas[i]
    
    nova_solucao = copy.deepcopy(solucao)
    
    # escolhe dois clientes de clusters diferentes
    cliente1, cliente2 = random.sample(range(n_clientes), 2)
    cluster1, cluster2 = nova_solucao[cliente1], nova_solucao[cliente2]
    
    if cluster1 == cluster2:
        return nova_solucao # não há troca se estão no mesmo cluster
    
    # capacidade após troca
    carga1 = capacidade_residual[cluster1] + demandas[cliente1] - demandas[cliente2]
    carga2 = capacidade_residual[cluster2] + demandas[cliente2] - demandas[cliente1]
    
    if carga1 >= 0 and carga2 >= 0:
        # realiza troca
        nova_solucao[cliente1], nova_solucao[cliente2] = cluster2, cluster1
        return nova_solucao
    
    return nova_solucao

# Plotar soluçOes
def plot_clusters_assignment(solucao, clientes, clusters):
    clientes = np.array(clientes)
    clusters = np.array(clusters)

    p = clusters.shape[0]
    colors = plt.cm.get_cmap('tab20', p)

    plt.figure(figsize=(7, 7))

    # Plota clusters (quadrados)
    for j in range(p):
        x, y, cap = clusters[j]
        plt.scatter(x, y, marker='s', s=150,
                    color=colors(j), edgecolor='k',
                    label=f"Cluster {j} (cap={cap})")

    # Plota clientes (círculos) e ligações
    for i in range(clientes.shape[0]):
        x, y, d = clientes[i]
        cl = solucao[i]
        cx, cy, _ = clusters[cl]
        plt.scatter(x, y, marker='o', s=60,
                    color=colors(cl), edgecolor='none',
                    label='Cliente' if i == 0 else "")
        plt.plot([x, cx], [y, cy], 'k--', alpha=0.4)

    plt.title("Alocação dos clientes aos clusters")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)

    # Legenda fora do gráfico (lado direito)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
    
    plt.tight_layout()
    plt.show()


