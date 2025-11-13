# 🎒 Algoritmo Genético para o Problema da Mochila

Este projeto implementa um algoritmo genético para resolver o clássico problema da mochila 0-1, onde o objetivo é maximizar o lucro total dos itens escolhidos sem ultrapassar a capacidade da mochila.

## 📁 Estrutura dos Arquivos

| Arquivo           | Descrição                                                                 |
|-------------------|---------------------------------------------------------------------------|
| `main.py`         | Executa o ciclo evolutivo do algoritmo genético.                         |
| `ga_operators.py` | Define os operadores genéticos e funções auxiliares para o problema da mochila. |

## ⚙️ Funções em `ga_operators.py`

| Função                          | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| `fitness_population(pop, p, w, W)` | Avalia a população com penalidade para soluções inviáveis. Maximiza o lucro. |
| `fitness_offspring(p, w, W, offspring)` | Avalia o fitness de um único indivíduo com penalidade proporcional ao excesso de peso. |
| `genpop(n, pop_size)`          | Gera população inicial aleatória com indivíduos de `n` genes.             |
| `mutation(prob_mut, offspring)`| Aplica mutação simples com probabilidade `prob_mut`.                      |
| `replacement(pop, fitness, offspring, fitness_off)` | Substitui o pior indivíduo se o filho for melhor.                          |
| `selection(pop_size, fitness)` | Seleciona dois pais por torneio (problema de maximização).                |
| `uniform_crossover(n, pop, parent1, parent2)` | Realiza crossover uniforme entre dois pais.                              |
| `genpop_feasible(n, pop_size, w, W)` | Gera população inicial apenas com soluções viáveis.                       |
| `uniform_crossover_feasible(n, pop, parent1, parent2, w, W)` | Gera filhos viáveis via crossover uniforme.                     |
| `mutation_feasible(prob_mut, offspring, w, W)` | Aplica mutação sem violar a restrição de peso.                           |

## 📌 Parâmetros do Problema

- `p`: lista de lucros dos itens
- `w`: lista de pesos dos itens
- `W`: capacidade máxima da mochila
- `n`: número de itens
- `pop_size`: tamanho da população
- `prob_mut`: taxa de mutação

## 🚀 Como Executar

1. Instale o NumPy:
   ```bash
   pip install numpy
