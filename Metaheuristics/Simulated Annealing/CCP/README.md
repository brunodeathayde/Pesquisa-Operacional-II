# 📌 Simulated Annealing para o Problema de Agrupamento Capacitado (CCP)

Este repositório contém uma implementação do **Simulated Annealing (SA)** aplicada ao **Problema de Agrupamento Capacitado (Capacitated Clustering Problem, CCP)**, um problema clássico de otimização combinatória em Pesquisa Operacional.
O algoritmo particiona um conjunto de clientes em `p` clusters com capacidade limitada, minimizando a soma das distâncias de cada cliente ao centro do seu cluster. A busca é guiada por um critério de aceitação probabilístico (Metropolis) e um resfriamento geométrico 🌡️🔥, que equilibra **exploração** 🔍 e **intensificação** 🎯 ao longo das iterações.

### Funcionamento Resumido do Simulated Annealing (SA) para o CCP

* **Representação da Solução:** Cada solução é uma partição dos $n$ clientes em $p$ clusters, onde cada cluster tem um **centro** (mediana) escolhido entre seus próprios membros. A solução é viável se a soma das demandas de cada cluster não exceder a capacidade $Q$.

* **Função Objetivo ($f$):** Soma das distâncias euclidianas de cada cliente ao centro do cluster ao qual foi alocado:
  $$f(S) = \sum_{k=1}^{n} D_{k,\,\text{centro}(S_k)}$$
  Quanto menor $f(S)$, melhor a solução.

* **Solução Inicial (Heurística Construtiva H.OC):**
  * **FIND:** Escolhe $p$ centros bem espalhados (par mais distante, depois maximiza o produto das distâncias aos centros já escolhidos).
  * **ASSIGN:** Atribui cada cliente ao centro mais próximo que ainda tenha capacidade disponível.
  * **RE-COMPUTE:** Para cada cluster, recalcula o centro como o cliente que minimiza a soma das distâncias aos demais membros.

* **Vizinhança ($\lambda$-interchange, $\lambda = 1$):** Sorteia um par de clusters $(C_i, C_j)$ e um dos operadores:
  * **$(0,1)$ Shift:** Move um cliente de $C_i$ para $C_j$.
  * **$(1,0)$ Shift:** Move um cliente de $C_j$ para $C_i$.
  * **$(1,1)$ Interchange:** Troca um cliente de $C_i$ com um de $C_j$.
  * Se o movimento violar a capacidade, tenta um **reparo** (move o excedente para um cluster com folga). Se o reparo for inviável, o movimento é descartado.

* **Critério de Aceitação (Metropolis):** Um vizinho $S'$ é aceito se:
  * $f(S') < f(S)$ (melhora), **ou**
  * $f(S') \geq f(S)$ com probabilidade $e^{-\Delta/T}$, onde $\Delta = f(S') - f(S)$ e $T$ é a temperatura atual.
  Isso permite escapar de ótimos locais aceitando movimentos piores no início.

* **Resfriamento:** A temperatura é reduzida geometricamente a cada iteração:
  $$T \leftarrow \alpha \cdot T, \quad \alpha \in (0,1)$$
  Com $T$ alto, aceita-se muitos movimentos ruins (exploração); com $T$ baixo, o algoritmo se comporta como busca gulosa (intensificação).

* **Melhor Solução Global:** Independentemente de o movimento ser aceito ou não, a melhor solução encontrada até o momento é sempre armazenada e retornada ao final.

* **Critério de Parada:** Número máximo de iterações (`max_iter`) ou temperatura mínima (`T_f`).

📂 Estrutura dos Arquivos

- **`distance_matrix.py`**
  Gera a matriz de distâncias euclidianas entre os clientes.

- **`objective_function_ccp.py`**
  Calcula o custo total (scatter) de uma solução: soma das distâncias de cada cliente ao centro do seu cluster.

- **`constructive_heuristic_ccp.py`**
  Heurística construtiva H.OC (FIND → ASSIGN → RE-COMPUTE) para gerar a solução inicial viável.

- **`lambda_interchange_ccp.py`**
  Mecanismo de vizinhança λ-interchange (λ=1): operadores de shift $(0,1)$, $(1,0)$ e interchange $(1,1)$, com reparo de capacidade.

- **`plotting_ccp.py`**
  Função para plotar graficamente a solução: clientes coloridos por cluster, centros destacados e arestas de alocação.

- **`ccp_generation.py`**
  Utilitário para gerar instâncias sintéticas do CCP (coordenadas, demandas e capacidade).

- **`ccp_reading.py`**
  Leitura de instâncias do CCP a partir de arquivos `.txt`.

- **`main_SA_CCP.py`**
  Script principal que executa o Simulated Annealing, controla as iterações, imprime os custos e plota os resultados.

- **`CCP-50.txt`**
  Exemplo de instância do problema de agrupamento capacitado.

---

## ⚙️ Operadores

| Operador | Descrição |
|----------|-----------|
| **`constructive_heuristic_ccp`** | Gera solução inicial: escolhe `p` centros bem espalhados, atribui clientes respeitando capacidade e recomputa centros. |
| **`objective_function_ccp`** | Soma das distâncias de cada cliente ao centro do seu cluster. |
| **`lambda_interchange_ccp`** | Gera vizinho via `(0,1)`, `(1,0)` ou `(1,1)` entre dois clusters, respeitando capacidade (com reparo). |
| **`repair_capacity`** | Move clientes excedentes para clusters com folga quando um movimento viola a capacidade. |
| **`recompute_centers`** | Recalcula o centro apenas dos clusters afetados pelo movimento (mediana local). |
| **`plotting_ccp`** | Desenha clientes, centros e arestas de alocação da melhor solução. |

---

## 📊 Parâmetros do SA

| Parâmetro | Símbolo | Valor |
|---|---|---|
| Temperatura inicial | $T_0$ | 1000 |
| Temperatura final | $T_f$ | 0.01 |
| Fator de resfriamento | $\alpha$ | 0.95 |
| Número máximo de iterações | — | 10000 |
| Número de clientes | $n$ | 50 |
| Número de clusters | $p$ | 5 |

---

## ▶️ Como executar

```bash
pip install numpy matplotlib
python main_SA_CCP.py
