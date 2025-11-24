## 🔥🌡️ Simulated Annealing para o Problema do Caixeiro Viajante

Este repositório contém uma implementação do **Simulated Annealing (SA)** aplicada ao **Problema do Caixeiro Viajante (TSP)**.  
O algoritmo busca minimizar a distância total percorrida, explorando vizinhos com probabilidade controlada pela temperatura e refinando a solução com heurísticas locais. O algoritmo utiliza uma temperatura inicial 🌡️ que vai sendo reduzida 🔥❄️ ao longo das iterações.

---

## 📂 Estrutura do Repositório

- `TSP-1.txt` → Instância do problema TSP (coordenadas das cidades).
- `main_SA.py` → Script principal que executa o Simulated Annealing.
- `best_solutions.jpg` → Gráfico da evolução do melhor fitness ao longo das iterações.
- `distance_matrix.py` → Gera a matriz de distâncias entre as cidades.
- `objective_function_tsp.py` → Calcula o custo total (distância) de uma rota.
- `plotting_route.py` → Função para plotar graficamente a rota final.
- `random_initial_solution_tsp.py` → Gera uma solução inicial aleatória.
- `swap_permutation.py` → Operador de vizinhança (troca de duas cidades).
- `tsp_generation.py` → Utilitário para gerar instâncias TSP.
- `tsp_reading.py` → Lê instâncias TSP a partir de arquivo `.txt`.
- `two_opt_best_improvement.py` → Implementação da heurística 2‑opt (best improvement).

---
