# 📦 Algoritmo Genético para Bin Packing 1D

Este projeto implementa um algoritmo genético para o problema de Bin Packing unidimensional, onde o objetivo é distribuir itens em bins de capacidade fixa de forma balanceada, minimizando a perda quadrática média entre os bins utilizados.

## 📁 Estrutura dos Arquivos

| Arquivo           | Descrição                                                                 |
|-------------------|---------------------------------------------------------------------------|
| `main.py`         | Executa o ciclo evolutivo do algoritmo genético.                         |
| `ga_operators.py` | Define os operadores genéticos e funções auxiliares para o problema de Bin Packing. |

## ⚙️ Funções em `ga_operators.py`

| Função                          | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| `genpop(pop_size, n_itens, n_bins, l, L)` | Gera população inicial com indivíduos viáveis, respeitando a capacidade dos bins. |
| `fitness_population(pop, l, L)` | Avalia a população com base na perda quadrática média entre bins utilizados. |
| `fitness_offspring(offspring, l, L)` | Avalia um único indivíduo (filho) com a mesma métrica de perda quadrática. |
| `selection(pop_size, fitness)` | Seleciona dois pais por torneio entre quatro candidatos aleatórios.       |
| `uniform_crossover(n, pop, parent1, parent2, l, L, n_bins)` | Realiza crossover uniforme gerando filhos viáveis. |
| `mutation(prob_mut, offspring, l, L, n_bins)` | Aplica mutação tentando realocar um item para outro bin viável.           |
| `replacement(pop, fitness, offspring, fitness_off)` | Substitui o pior indivíduo da população se o filho for melhor.           |

## 🧮 Função Objetivo: Perda Quadrática Média


A função de fitness utilizada busca minimizar o desbalanceamento entre os bins utilizados. A equação é:



\[
\text{Fitness} = \frac{1}{|B|} \sum_{b \in B} (L - C_b)^2
\]



Onde:

- \( B \): conjunto de bins utilizados (aqueles com pelo menos um item)
- \( L \): capacidade máxima de cada bin
- \( C_b \): carga total do bin \( b \)
- \( (L - C_b)^2 \): penalidade quadrática para o desvio da carga ideal

Essa métrica favorece soluções onde os bins estão igualmente preenchidos, evitando tanto bins muito cheios quanto muito vazios.


## ⚠️ Por que não minimizar apenas o número de bins?

Minimizar apenas o número de bins utilizados não é uma boa função de fitness para algoritmos genéticos, pois:

- Muitos indivíduos diferentes podem usar o mesmo número de bins, tornando-os indistinguíveis para o algoritmo.
- Isso prejudica a seleção natural e a convergência, pois não há gradiente de qualidade entre soluções.
- A perda quadrática média fornece uma métrica contínua e diferenciável, ideal para orientar a evolução genética.

## 📌 Parâmetros do Problema

- `l`: lista de tamanhos dos itens
- `L`: capacidade máxima de cada bin
- `n_itens`: número total de itens
- `n_bins`: número de bins disponíveis
- `pop_size`: tamanho da população
- `prob_mut`: taxa de mutação

## 🚀 Como Executar

1. Instale o NumPy:
   ```bash
   pip install numpy
