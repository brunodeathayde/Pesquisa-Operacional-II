# Iterated Local Search (ILS) para Problema de Layout

Este projeto implementa um **Iterated Local Search (ILS)** para resolver o problema de **layout de instalações**.  
O objetivo é minimizar o custo total de movimentação considerando distâncias e fluxos entre unidades.

---

## 📂 Estrutura dos Arquivos

- **`ILS_layout_operators.py`**  
  Contém a implementação dos operadores do ILS (geração de solução inicial, cálculo de custo, perturbação, busca local e plotagem).

- **`read_layout.py`**  
  Função para leitura de instâncias de layout (matriz de distâncias e fluxos).

- **`layout-1.txt`**  
  Exemplo de instância contendo dados de distâncias e fluxos.

- **`main.py`**  
  Script principal que executa o algoritmo ILS:
  - Lê instância
  - Gera solução inicial
  - Aplica busca local
  - Executa perturbações e aceita melhorias
  - Plota evolução da função objetivo e layout final

- **`Figure_1.png`**  
  Exemplo de solução gerada pelo algoritmo, mostrando o layout final.

---

## ⚙️ Fluxo do Algoritmo

1. **Leitura da instância** (`read_layout`)  
2. **Geração da solução inicial** (`random_initial_solution`)  
3. **Cálculo do custo** (`cost_layout`)  
4. **Busca local** (`two_opt_qap_best_improvement`)  
5. **Perturbação** (`perturbation`)  
6. **Aceitação da nova solução** se houver melhoria  
7. **Iterações** até atingir o número máximo definido  
8. **Plotagem** da evolução do custo e do layout final  

---

## 🧩 Operadores ILS

| Operador | Função | Descrição |
|----------|--------|-----------|
| `random_initial_solution` | Inicialização | Gera uma solução inicial aleatória para o layout. |
| `cost_layout` | Avaliação | Calcula o custo total do layout com base em distâncias e fluxos. |
| `perturbation` | Perturbação | Aplica uma modificação aleatória na solução atual para escapar de ótimos locais. |
| `two_opt_qap_best_improvement` | Busca local | Aplica o movimento 2-opt adaptado ao QAP para melhorar a solução. |
| `plot_layout` | Visualização | Plota graficamente o layout final encontrado pelo algoritmo. |


