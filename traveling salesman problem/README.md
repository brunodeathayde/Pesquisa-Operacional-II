# Traveling Salesman Problem (TSP)

Este diretório contém diversas abordagens para resolver o clássico problema do caixeiro viajante (Traveling Salesman Problem - TSP), que consiste em encontrar o menor caminho possível que visita um conjunto de cidades exatamente uma vez e retorna à cidade de origem.

## 📁 Estrutura dos Arquivos

| Arquivo                         | Descrição                                                                 |
|--------------------------------|---------------------------------------------------------------------------|
| `distance_matrix.py`           | Gera a matriz de distâncias entre cidades com base em coordenadas.       |
| `farthest_insertion_tsp.py`    | Implementa a heurística de inserção do ponto mais distante.              |
| `milp_TSP.py`                  | Formulação exata do TSP via programação inteira mista (MILP).            |
| `nearest_neighbor_tsp.py`      | Algoritmo do vizinho mais próximo para construção de rotas iniciais.     |
| `plotting_route.py`            | Funções para visualização gráfica da rota gerada.                        |
| `random_route_tsp.py`          | Gera rotas aleatórias para fins de comparação ou inicialização.          |
| `route_distance.py`            | Calcula a distância total de uma rota dada.                              |
| `tsp.main.py`                  | Script principal para execução dos algoritmos e visualização dos resultados. |
| `tsp_generation.py`            | Gera instâncias sintéticas de cidades com coordenadas aleatórias.        |
| `tsp_reading.py`               | Lê instâncias de arquivos `.txt` e converte para estruturas utilizáveis. |
| `two_opt_best_improvement.py`  | Implementa a heurística de 2-opt com melhor melhoria para refinamento de rotas. |

## 🧠 Algoritmos Implementados

- **Vizinho Mais Próximo (Nearest Neighbor)**
- **Inserção do Ponto Mais Distante (Farthest Insertion)**
- **2-opt com Melhor Melhoria**
- **Rotas Aleatórias**
- **Formulação MILP com solver para solução exata**
