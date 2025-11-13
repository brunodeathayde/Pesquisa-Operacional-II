# 🧬 Algoritmo Genético em Python

Este projeto implementa um algoritmo genético simples para minimizar a função \( f(x) = x^2 \), utilizando representação binária, seleção por torneio, crossover uniforme e mutação.

## 📁 Estrutura dos Arquivos

| Arquivo           | Descrição                                                                 |
|-------------------|---------------------------------------------------------------------------|
| `main.py`         | Executa o ciclo evolutivo do algoritmo genético.                         |
| `ga_operators.py` | Define as funções utilizadas para operar sobre a população genética.     |

## ⚙️ Funções em `ga_operators.py`

| Função                          | Descrição                                                                 |
|---------------------------------|---------------------------------------------------------------------------|
| `bits_to_float(bits)`           | Converte uma lista de bits em um número float no intervalo [-10, 10].     |
| `fitness_population(pop, pop_size)` | Calcula o valor de fitness para cada indivíduo da população. Minimiza \( x^2 \). |
| `fitness_offspring(offspring)`  | Avalia o fitness de um único indivíduo (filho). Minimiza \( x^2 \).       |
| `genpop(n, popsize)`            | Gera uma população inicial aleatória com `popsize` indivíduos de `n` bits. |
| `mutation(pmut, offspring)`     | Aplica mutação simples em um indivíduo com probabilidade `pmut`.          |
| `replacement(pop, fitness, offspring, fitness_off)` | Substitui o pior indivíduo da população se o filho for melhor.         |
| `selection(pop_size, fitness)`  | Seleciona dois pais por torneio entre quatro candidatos aleatórios.       |
| `uniform_crossover(n, pop, parent1, parent2)` | Realiza crossover uniforme entre dois pais para gerar um novo indivíduo. |

## 🚀 Como Executar

1. Instale o NumPy:
   ```bash
   pip install numpy
