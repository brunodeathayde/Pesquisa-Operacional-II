# 📌 Algoritmo Genético para o Problema de P-Medianas

Este repositório contém uma implementação de um **Algoritmo Genético (GA)** para resolver o problema das **p-medianas**, um problema clássico de otimização combinatória em Pesquisa Operacional.

## 📂 Estrutura dos Arquivos

- **`distance_matrix.py`**  
  Gera a matriz de distâncias euclidianas entre os pontos.

- **`ga_operators.py`**  
  Implementa os operadores genéticos (seleção, crossover, mutação, substituição, restart) e funções auxiliares.

- **`main.py`**  
  Script principal para execução do algoritmo genético, controle das gerações e plotagem da melhor solução.

- **`pmed_generation.py`**  
  Funções para geração da população inicial e cálculo de fitness.

- **`pmedian_reading.py`**  
  Leitura de instâncias do problema a partir de arquivos `.txt`.

- **`pmedian-1.txt`**  
  Exemplo de instância do problema de p-medianas.

---

## ⚙️ Operadores Genéticos

| Operador | Descrição |
|----------|-----------|
| **`genpop`** | Gera a população inicial escolhendo aleatoriamente `p` medianas e alocando cada cliente a uma delas. |
| **`fitness_population`** | Calcula o custo total da população, somando as distâncias de cada cliente à sua mediana. |
| **`selection`** | Seleção por torneio: escolhe dois pais entre quatro candidatos aleatórios, mantendo os de menor fitness. |
| **`uniform_crossover_pmedian`** | Crossover uniforme: combina genes dos pais e ajusta para manter exatamente `p` medianas válidas. |
| **`mutation_pmedian`** | Mutação: seleciona dois clientes não-medianas alocados a medianas diferentes e troca suas alocações. |
| **`fitness_offspring_pmedian`** | Calcula o fitness de um único indivíduo (offspring). |
| **`replacement`** | Substitui o pior indivíduo da população pelo offspring, caso este seja melhor. |
| **`restart_operator`** | Reinicia a população quando há estagnação, preservando o melhor indivíduo em posição aleatória. |
| **`plot_best_solution`** | Gera um gráfico mostrando a alocação dos clientes às medianas na melhor solução encontrada. |

---


