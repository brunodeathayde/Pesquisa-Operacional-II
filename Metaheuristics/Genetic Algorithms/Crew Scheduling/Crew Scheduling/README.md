# Algoritmo Genético para Crew Scheduling

Este projeto implementa um **algoritmo genético** para resolver o problema de *crew scheduling* (alocação de tripulação).  
O objetivo é encontrar uma solução que minimize os custos de alocação e penalize escalas que deixem tarefas descobertas.

---

## 📌 Descrição

O problema de *crew scheduling* pode ser modelado como uma instância de **Set Covering Problem (SCP)**, onde:

- Cada coluna da matriz `A` representa uma possível escala de tripulação.
- Cada linha da matriz `A` representa uma tarefa (voo, turno, etc.) que precisa ser coberta.
- O vetor `c` contém os custos associados a cada escala.
- O algoritmo busca uma combinação de escalas que cubra todas as tarefas com o menor custo possível.

---

## ⚙️ Função Objetivo

A função objetivo avalia a qualidade de uma solução candidata (indivíduo da população):



\[
f(x) = \sum (c \cdot x) + \text{penalty} \cdot k
\]



Onde:
- \(x\) → vetor binário que indica quais escalas foram escolhidas.
- \(c\) → vetor de custos das escalas.
- \(k\) → número de tarefas **não cobertas** pela solução.
- `penalty` → valor de penalização aplicado para cada tarefa descoberta.

👉 Em resumo:
- O **primeiro termo** soma os custos das escalas escolhidas.
- O **segundo termo** adiciona uma penalização proporcional ao número de tarefas não atendidas.
- O algoritmo busca **minimizar** essa função.

---

## 🔄 Componentes do Algoritmo Genético

- **Geração inicial (`genpop`)**: cria uma população aleatória de soluções binárias.
- **Avaliação (`fitness_evaluation`)**: calcula o valor da função objetivo para cada indivíduo.
- **Seleção (`selection`)**: escolhe os melhores indivíduos para reprodução.
- **Crossover (`uniform_crossover`)**: combina genes de dois pais para gerar um novo indivíduo.
- **Mutação (`mutation`)**: altera aleatoriamente um gene para manter diversidade.
- **Substituição (`replacement`)**: insere o novo indivíduo na população, substituindo o pior.
- **Controle de tempo**: o algoritmo roda até atingir o limite de tempo definido.

---

## 📊 Resultados

- O algoritmo imprime:
  - Fitness da população inicial.
  - Melhor solução encontrada.
  - Número de gerações executadas.
  - Tempo computacional gasto.
- Também gera um **gráfico da evolução do melhor fitness** ao longo das gerações.

---

## 🧬 Operadores do Algoritmo Genético

| Operador            | Função                                                                 | Implementação no Código |
|---------------------|-------------------------------------------------------------------------|--------------------------|
| **Geração Inicial** | Cria a população inicial de soluções binárias aleatórias.               | `genpop(n, popsize)` |
| **Avaliação (Fitness)** | Calcula o valor da função objetivo para cada indivíduo, somando custos e penalidades. | `fitness_evaluation(A, c, pop, popsize, penalty)` |
| **Seleção**         | Escolhe os pais com base no desempenho (torneio entre indivíduos).      | `selection(popsize, fitness)` |
| **Crossover (Recombinação)** | Combina genes de dois pais para gerar um novo indivíduo (uniforme). | `uniform_crossover(n, pop, parent1, parent2)` |
| **Mutação**         | Altera aleatoriamente um gene do indivíduo para manter diversidade.     | `mutation(pmut, offspring)` |
| **Substituição (Replacement)** | Insere o novo indivíduo na população, substituindo o pior.         | `replacement(pop, fitness, offspring, fitness_offspring)` |
| **Função Objetivo** | Soma dos custos das escalas escolhidas + penalidade por tarefas não cobertas. | `fitness_evaluation` / `fitness_offspring` |
| **Leftovers**       | Conta quantas tarefas não foram cobertas pela solução.                  | `leftovers(A, x)` |


