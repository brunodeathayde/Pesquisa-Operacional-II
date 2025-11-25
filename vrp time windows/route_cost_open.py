import numpy as np

def route_cost_open(route, P, capacity, deposito, destino_final, tempo_servico=0):
    """
    Versão para Open Vehicle Routing Problem (OVRP).
    - deposito: tupla (x_dep, y_dep)
    - destino_final: tupla (x_dest, y_dest)
    - P: lista de pontos [x, y, demanda, inicio_janela, fim_janela]
    """
    dist_total = 0.0
    todas_rotas = []   # Lista para armazenar todas as rotas (sub-rotas)
    rota_atual = []    # Rota atual do veículo
    carga_atual = 0
    tempo_atual = 0
    atual_x, atual_y = deposito  # Posição inicial no depósito
    
    for i, ponto in enumerate(route):
        x, y, demanda, inicio_janela, fim_janela = P[ponto - 1]
        
        # Distância até o próximo ponto
        distancia_para_ponto = np.hypot(x - atual_x, y - atual_y)
        tempo_chegada = tempo_atual + distancia_para_ponto
        
        # Verifica necessidade de novo veículo
        precisa_novo_veiculo = False
        if carga_atual + demanda > capacity:
            precisa_novo_veiculo = True
        elif tempo_chegada > fim_janela:
            precisa_novo_veiculo = True
        
        if precisa_novo_veiculo and rota_atual:
            # Finaliza rota atual (sem retorno ao depósito)
            # Vai direto para o destino final
            dist_to_destino = np.hypot(destino_final[0] - atual_x, destino_final[1] - atual_y)
            dist_total += dist_to_destino
            todas_rotas.append(rota_atual)
            
            # Reinicia para novo veículo
            rota_atual = []
            carga_atual = 0
            tempo_atual = 0
            atual_x, atual_y = deposito
            
            # Recalcula distância do depósito para o ponto atual
            distancia_para_ponto = np.hypot(x - atual_x, y - atual_y)
            tempo_chegada = distancia_para_ponto
        
        # Adiciona ponto à rota atual
        rota_atual.append(ponto)
        dist_total += distancia_para_ponto
        carga_atual += demanda
        
        # Ajusta tempo pela janela
        if tempo_chegada < inicio_janela:
            tempo_partida = inicio_janela + tempo_servico
        else:
            tempo_partida = tempo_chegada + tempo_servico
        
        tempo_atual = tempo_partida
        atual_x, atual_y = x, y
    
    # Finaliza última rota indo ao destino final (não retorna ao depósito)
    if rota_atual:
        dist_to_destino = np.hypot(destino_final[0] - atual_x, destino_final[1] - atual_y)
        dist_total += dist_to_destino
        todas_rotas.append(rota_atual)
    
    viavel = True  # Simplificação
    
    return dist_total, viavel, todas_rotas
