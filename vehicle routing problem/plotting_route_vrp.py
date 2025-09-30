import matplotlib.pyplot as plt

def plotting_route_vrp(P, route, capacidade):
    """
    Plota rotas do VRP RESPEITANDO a capacidade do veículo
    Cada viagem ganha uma cor diferente.
    """
    # Converte a rota para o formato correto
    if isinstance(route, int):
        rotas = [[route]]
    elif all(isinstance(item, int) for item in route):
        rotas = [route]
    else:
        rotas = route
    
    cores = ['red', 'blue', 'green', 'orange', 'purple', 
             'brown', 'pink', 'gray', 'olive', 'cyan']
    
    plt.figure(figsize=(10, 8))
    
    # Depósito
    plt.plot(0, 0, 's', markersize=12, color='black', label="Depósito")
    
    # Clientes
    for i, (x, y, demanda) in enumerate(P):
        plt.plot(x, y, 'o', markersize=8, color='blue')
        plt.text(x, y, f' {i+1}(d:{int(demanda)})', fontsize=10)
    
    cor_idx = 0  # índice global de cor
    
    # Plota cada rota RESPEITANDO a capacidade
    for rota in rotas:
        x_rota = [0]  # Começa no depósito
        y_rota = [0]
        demanda_atual = 0
        
        for cliente in rota:
            idx = cliente - 1
            demanda_cliente = P[idx][2]
            
            # VERIFICA SE EXCEDE A CAPACIDADE
            if demanda_atual + demanda_cliente > capacidade:
                # Finaliza viagem atual
                x_rota.append(0)
                y_rota.append(0)
                plt.plot(x_rota, y_rota, color=cores[cor_idx % len(cores)], linewidth=2)
                
                # Adiciona setas
                for j in range(len(x_rota)-1):
                    dx = x_rota[j+1] - x_rota[j]
                    dy = y_rota[j+1] - y_rota[j]
                    if dx != 0 or dy != 0:
                        plt.arrow(x_rota[j], y_rota[j], dx*0.7, dy*0.7, 
                                 head_width=0.2, head_length=0.2, 
                                 fc=cores[cor_idx % len(cores)], 
                                 ec=cores[cor_idx % len(cores)], alpha=0.7)
                
                # Avança para a próxima cor
                cor_idx += 1
                x_rota, y_rota = [0], [0]
                demanda_atual = 0
            
            # Adiciona cliente à rota atual
            x_rota.append(P[idx][0])
            y_rota.append(P[idx][1])
            demanda_atual += demanda_cliente
        
        # Finaliza viagem restante
        x_rota.append(0)
        y_rota.append(0)
        plt.plot(x_rota, y_rota, color=cores[cor_idx % len(cores)], linewidth=2)
        
        for j in range(len(x_rota)-1):
            dx = x_rota[j+1] - x_rota[j]
            dy = y_rota[j+1] - y_rota[j]
            if dx != 0 or dy != 0:
                plt.arrow(x_rota[j], y_rota[j], dx*0.7, dy*0.7, 
                         head_width=0.2, head_length=0.2, 
                         fc=cores[cor_idx % len(cores)], 
                         ec=cores[cor_idx % len(cores)], alpha=0.7)
        
        cor_idx += 1
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.show()
