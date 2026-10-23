# 🐜🔥 Ant Colony System (ACS) para o Problema do Caixeiro Viajante

Este repositório contém uma implementação do **Ant Colony System (ACS)** de Dorigo & Gambardella aplicada ao **Problema do Caixeiro Viajante (TSP)**.
O algoritmo simula o comportamento de formigas em busca de alimento: cada formiga constrói uma rota guiada por **feromônio** 🧪 e **visibilidade** (heurística gulosa) 👁️. A atualização local e global do feromônio equilibra **exploração** 🔍 e **explotação** 🎯 ao longo das iterações, convergindo para rotas de baixo custo.

### Funcionamento Resumido do Ant Colony System (ACS)

* **Matriz de Visibilidade ($\eta$):** Informação heurística baseada no inverso da distância ($\eta_{r,s} = 1 / D_{r,s}$). Quanto menor a distância, maior a atratividade da aresta.
* **Feromônio Inicial ($\tau_0$):** Inicializado de forma uniforme em todas as arestas com base no custo do vizinho mais próximo: $\tau_0 = 1 / (n \cdot L_{nn})$.
* **Construção das Rotas:** Cada formiga constrói sua rota cidade a cidade a partir de um nó inicial aleatório:
  * **Aproveitamento ($q \le q_0$):** Escolhe deterministicamente a melhor cidade combinando feromônio e visibilidade ($\tau \cdot \eta^\beta$).
  * **Exploração ($q > q_0$):** Escolhe a próxima cidade de forma probabilística.
* **Atualização Local do Feromônio:** A cada passo, a formiga reduz o feromônio da aresta percorrida ($\tau \leftarrow (1-\rho)\tau + \rho\tau_0$). Isso evita que outras formigas repitam o mesmo caminho na mesma iteração.
* **Atualização Global do Feromônio:** Ao fim de cada iteração, **apenas a melhor rota global** recebe reforço de feromônio ($\tau \leftarrow (1-\alpha)\tau + \alpha / f_{best}$).

📂 Estrutura do Repositório

    TSP-50.txt → Instância do problema TSP (50 cidades em espaço 2D, coordenadas geradas com semente fixa).
    main_ACS.py → Script principal que executa o Ant Colony System.
    best_solutions.jpg → Gráfico da evolução do melhor fitness ao longo das iterações.
    distance_matrix.py → Gera a matriz de distâncias entre as cidades.
    objective_function_tsp.py → Calcula o custo total (distância) de uma rota.
    plotting_route.py → Função para plotar graficamente a rota final e a rota inicial.
    acs.py → Implementação do núcleo do Ant Colony System (construção de rotas, regra pseudoaleatória proporcional, atualizações de feromônio).
    tsp_generation.py → Utilitário para gerar instâncias TSP.
    tsp_reading.py → Lê instâncias TSP a partir de arquivo .txt.

⚙️ Operadores e Parâmetros do ACS

| Componente | Arquivo | Descrição | Fórmula / Regra |
|---|---|---|---|
| Matriz de distâncias | `distance_matrix.py` | Distância euclidiana entre todas as cidades | $D_{ij} = \sqrt{(x_i-x_j)^2 + (y_i-y_j)^2}$ |
| Função objetivo | `objective_function_tsp.py` | Custo total do circuito fechado | $f(s) = \sum_{i=1}^{n-1} D_{s_i s_{i+1}} + D_{s_n s_1}$ |
| Visibilidade (heurística) | `acs.py` | Prioriza cidades próximas na construção | $\eta_{ij} = 1 / D_{ij}$ |
| Feromônio inicial | `acs.py` | Valor inicial uniforme em todas as arestas | $\tau_0 = 1 / (n \cdot L_{nn})$ |
| Regra pseudoaleatória proporcional | `acs.py` | Escolha entre explotação e exploração | $s = \arg\max \{\tau_{ij} \cdot \eta_{ij}^{\beta}\}$ se $q \le q_0$; caso contrário, amostragem proporcional |
| Atualização local do feromônio | `acs.py` | Aplicada a cada aresta percorrida durante a construção | $\tau_{ij} \leftarrow (1-\rho)\tau_{ij} + \rho\tau_0$ |
| Atualização global do feromônio | `acs.py` | Aplicada apenas à melhor rota global | $\tau_{ij} \leftarrow (1-\alpha)\tau_{ij} + \alpha/f_{best}$ |
| Construção de rota | `acs.py` | Cada formiga percorre todas as cidades uma vez | Seleção sucessiva de cidades não visitadas |
| Plotagem | `plotting_route.py` | Desenha cidades, arestas e rótulos da rota | — |

📊 Parâmetros Utilizados

| Parâmetro | Símbolo | Valor |
|---|---|---|
| Número de cidades | $n$ | **50** |
| Número de formigas | $m$ | 10 |
| Importância da visibilidade | $\beta$ | 2.0 |
| Probabilidade de explotação | $q_0$ | 0.9 |
| Taxa de decaimento global | $\alpha$ | 0.1 |
| Taxa de decaimento local | $\rho$ | 0.1 |
| Número de iterações | — | 100 |

### Observações sobre a estrutura

- **`main_ACS.py`** é o script que você executa (`python main_ACS.py`). Ele orquestra tudo: gera a instância de 50 cidades, monta a matriz de distâncias, roda o ACS, imprime os custos e plota os três gráficos (convergência, rota inicial e rota final).
- **`acs.py`** concentra o algoritmo em si (parâmetros, loop principal, construção de rotas e atualizações de feromônio), separado do script principal para manter a organização modular do template.
- **`plotting_route.py`** contém a função `plotting_route(...)`, usada tanto para a rota inicial (iteração 1) quanto para a rota final.
- **`tsp_generation.py`** gera o `TSP-50.txt` com `np.random.seed(42)` e `n = 50`.
- **`tsp_reading.py`** lê o `TSP-50.txt` de volta para um array NumPy.
- **`nearest_neighbor_tour_length.py`** calcula $L_{nn}$, o comprimento do tour pelo vizinho mais próximo, usado para inicializar $\tau_0$. **Essa rotina precisa voltar ao repositório**, já que a fórmula de $\tau_0$ que você descreveu depende dela.
- **Não há `two_opt_best_improvement.py`** — propositalmente, pois esta versão é **ACS puro**, sem 2-Opt.
- **Não há `random_initial_solution_tsp.py` nem `swap_permutation.py`** — o ACS constrói rotas probabilisticamente, não precisa de solução inicial aleatória nem de operador de swap.

### Como executar

```bash
pip install numpy matplotlib
python main_ACS.py
