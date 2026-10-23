# 🐜🔥 Ant Colony System (ACS) para o Problema do Caixeiro Viajante

Este repositório contém uma implementação do **Ant Colony System (ACS)** de Dorigo & Gambardella aplicada ao **Problema do Caixeiro Viajante (TSP)**.
O algoritmo simula o comportamento de formigas em busca de alimento, onde cada formiga constrói uma rota guiada por **feromônio** 🧪 e **visibilidade** (heurística gulosa) 👁️. A atualização local e global do feromônio permite equilibrar **exploração** 🔍 e **explotação** 🎯 ao longo das iterações, convergindo para rotas de baixo custo.
📂 Estrutura do Repositório

    TSP-30.txt → Instância do problema TSP (30 cidades em espaço 2D, coordenadas geradas com semente fixa).
    main_ACS.py → Script principal que executa o Ant Colony System.
    distance_matrix.py → Gera a matriz de distâncias euclidianas entre as cidades.
    objective_function_tsp.py → Calcula o custo total (distância) de uma rota (circuito fechado).
    plotting_route.py → Função para plotar graficamente a rota final e a rota inicial.
    acs.py → Implementação do núcleo do Ant Colony System (construção de rotas, regra pseudoaleatória proporcional, atualizações de feromônio).
    tsp_generation.py → Utilitário para gerar instâncias TSP.
    tsp_reading.py → Lê instâncias TSP a partir de arquivo .txt.
