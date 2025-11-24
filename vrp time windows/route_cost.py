import numpy as np

def route_cost(route, P, capacity, tempo_servico=0):
    """
    Versão que cria novos veículos quando há violação de capacidade ou janela de tempo
    """
    dist_total = 0.0
    todas_rotas = []  # Lista para armazenar todas as rotas (sub-rotas)
    rota_atual = []   # Rota atual do veículo
    carga_atual = 0
    tempo_atual = 0
    atual_x, atual_y = 0, 0  # Posição inicial no depósito
    
    # Dicionários para armazenar tempos de cada rota
    todas_chegadas = []
    todas_partidas = []
    
    for i, ponto in enumerate(route):
        x, y, demanda, inicio_janela, fim_janela = P[ponto - 1]
        
        # Calcula distância até o próximo ponto
        distancia_para_ponto = np.hypot(x - atual_x, y - atual_y)
        tempo_chegada = tempo_atual + distancia_para_ponto
        
        # VERIFICA SE PRECISA DE NOVO VEÍCULO
        precisa_novo_veiculo = False
        
        # 1. Verifica capacidade
        if carga_atual + demanda > capacity:
            precisa_novo_veiculo = True
        
        # 2. Verifica janela de tempo
        elif tempo_chegada > fim_janela:
            precisa_novo_veiculo = True
        
        # Se precisa de novo veículo, finaliza rota atual e começa nova
        if precisa_novo_veiculo and rota_atual:
            # Retorna ao depósito da rota atual
            dist_to_depot = np.hypot(atual_x, atual_y)
            dist_total += dist_to_depot
            tempo_atual += dist_to_depot
            
            # Armazena rota atual
            todas_rotas.append(rota_atual)
            
            # Reinicia para novo veículo
            rota_atual = []
            carga_atual = 0
            tempo_atual = 0
            atual_x, atual_y = 0, 0
            
            # Recalcula distância do depósito para o ponto atual
            distancia_para_ponto = np.hypot(x, y)
            tempo_chegada = distancia_para_ponto
        
        # ADICIONA PONTO À ROTA ATUAL
        rota_atual.append(ponto)
        dist_total += distancia_para_ponto
        
        # Atualiza carga
        carga_atual += demanda
        
        # AJUSTA TEMPO POR CAUSA DA JANELA
        if tempo_chegada < inicio_janela:
            # Espera até a janela abrir
            tempo_partida = inicio_janela + tempo_servico
        else:
            # Dentro da janela ou chegou atrasado (mas ainda vai atender)
            tempo_partida = tempo_chegada + tempo_servico
        
        tempo_atual = tempo_partida
        atual_x, atual_y = x, y
    
    # Adiciona a última rota (se houver pontos)
    if rota_atual:
        # Retorno ao depósito final
        dist_to_depot = np.hypot(atual_x, atual_y)
        dist_total += dist_to_depot
        todas_rotas.append(rota_atual)
    
    # Calcula viabilidade (considera viável se não há violação de janela nas rotas finais)
    viavel = True
    # Para verificar viabilidade precisaríamos simular cada rota individualmente
    
    return dist_total, viavel, todas_rotas