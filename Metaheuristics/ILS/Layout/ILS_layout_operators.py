import numpy as np
import matplotlib.pyplot as plt
import random

# Gera solução inicial aleatória
def random_initial_solution(n):
    return list(np.random.permutation(n))  # retorna lista em vez de array

# Custo de uma configuração de arranjo físico
def cost_layout(distancias, fluxos, layout):
    n = len(layout)
    valor = 0
    for i in range(n):
        for j in range(n):
            dept_i = i
            dept_j = j
            loc_i = layout[dept_i]
            loc_j = layout[dept_j]
            valor += fluxos[dept_i][dept_j] * distancias[loc_i][loc_j]
    return valor

#   Aplica uma perturbação em uma solução (layout) para ILS.
#   Seleciona um trecho proporcional ao parâmetro 'intensidade' e embaralha.
#   Garante que o trecho embaralhado seja diferente do original.
def perturbation(layout, intensidade):
    n = len(layout)
    tamanho_trecho = max(1, int(n * intensidade))
    inicio = random.randint(0, n - tamanho_trecho)
    fim = inicio + tamanho_trecho

    novo_layout = layout[:]
    trecho = novo_layout[inicio:fim]

    # Garante que o shuffle produza algo diferente
    nova_ordem = trecho[:]
    while True:
        random.shuffle(nova_ordem)
        if nova_ordem != trecho:
            break

    novo_layout[inicio:fim] = nova_ordem
    return novo_layout

# Aplica busca local 2-opt (swap)
def two_opt_qap_best_improvement(layout, distancias, fluxos, best_cost):
    n = len(layout)
    improved = True

    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                # criar nova solução trocando dept_i e dept_j
                new_layout = layout[:]
                new_layout[i], new_layout[j] = new_layout[j], new_layout[i]

                # calcular custo da nova solução
                new_cost = 0
                for a in range(n):
                    for b in range(n):
                        new_cost += fluxos[a][b] * distancias[new_layout[a]][new_layout[b]]

                # verificar melhoria
                if new_cost < best_cost:
                    layout = new_layout
                    best_cost = new_cost
                    improved = True
                    break  # reinicia busca após melhoria
            if improved:
                break

    return layout, best_cost

# Plota o layout da solução 
def plot_layout(layout, title="Layout"):
    n = len(layout)
    lado = int(np.sqrt(n))  # aqui será 12
    
    plt.figure(figsize=(8,8))
    for dept, loc in enumerate(layout):
        x, y = loc % lado, loc // lado
        plt.scatter(x, y, s=500, c="skyblue", edgecolors="black")
        plt.text(x, y, str(dept), ha="center", va="center", fontsize=10, fontweight="bold")
    
    plt.title(title)
    plt.xticks(range(lado))
    plt.yticks(range(lado))
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

    