├── dantzig_heuristic.py     # Implementação da heurística gulosa

├── mip_model.py             # Modelo exato com Python MIP

├── README.md                # Este arquivo

- Knapsack Problem in Python

Este repositório apresenta duas abordagens para resolver o clássico **Problema da Mochila 0–1**:

1. **Heurística de Dantzig (Guloso por valor unitário)**
2. **Modelo exato com Python MIP**

---

- Descrição do Problema

Dado um conjunto de itens, cada um com um valor `p[i]` e um peso `w[i]`, e uma capacidade máxima da mochila `c`, o objetivo é selecionar um subconjunto de itens que maximize o valor total sem ultrapassar a capacidade.

---

# Heurística de Dantzig

A heurística implementada segue o princípio guloso proposto por Dantzig:

- Calcula o valor por unidade de peso para cada item.
- Ordena os itens por esse valor (do maior para o menor).
- Seleciona os itens enquanto houver capacidade disponível.
