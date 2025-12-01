# GRASP para o Open Vehicle Routing Problem (OVRP)

Este repositório implementa uma metaheurística **GRASP (*Greedy Randomized Adaptive Search Procedures*)** para resolver o *Open Vehicle Routing Problem* (OVRP).  

No OVRP, os veículos partem de um **depósito**, visitam um conjunto de **clientes** e finalizam suas rotas em um **ponto de entrega**. O objetivo é minimizar o custo total das rotas, respeitando a capacidade dos veículos.

---

## 📂 Estrutura do Repositório

- **OVRP-1.txt** → Instância de teste com coordenadas e demandas dos clientes  
- **grasp_operators.py** → Implementação dos operadores do GRASP (construção, reallocation, swap, 2-opt, etc.)  
- **main.py** → Script principal para execução do GRASP  
- **ovrp_generation.py** → Geração de instâncias do problema  
- **ovrp_reading.py** → Leitura de instâncias do problema  
- **routes.png** → Exemplo de rotas geradas e plotadas  

---

## ⚙️ Funcionamento

1. **Construção inicial (GRASP)**  
   - Gera rotas viáveis usando uma lista de candidatos restrita (RCL).  
2. **Busca local**  
   - Aplica operadores de vizinhança para melhorar a solução inicial.  
3. **Melhor solução global**  
   - Mantém sempre a melhor solução encontrada ao longo das iterações.  

---

## 🛠️ Operadores do GRASP

| Operador        | Descrição                                                                 |
|-----------------|---------------------------------------------------------------------------|
| **Construction** | Constrói rotas iniciais usando RCL e respeitando capacidade dos veículos. |
| **Reallocation** | Move um cliente de uma rota para outra rota com capacidade disponível.    |
| **Swap**         | Troca dois clientes de rotas diferentes, respeitando a capacidade.        |
| **2-opt**        | Otimiza cada rota individualmente, removendo cruzamentos e reduzindo custo.|

---

## 🎨 Visualização

As rotas podem ser plotadas com cores distintas usando `plot_routes`.  
Exemplo de saída gráfica:

![Rotas geradas](routes.png)

# 🚚 Interface OVRP - Tkinter

Este projeto implementa uma **interface gráfica em Python** para resolver o **Open Vehicle Routing Problem (OVRP)** utilizando o algoritmo **GRASP** com operadores de melhoria (Reallocation, Swap e 2-opt).  
A interface foi construída com **Tkinter** e integra visualização de rotas com **Matplotlib**.

---

## ✨ Funcionalidades

- 📂 **Carregar instância** de problema a partir de arquivo `.txt`
- ⚙️ **Configurar parâmetros** do algoritmo:
  - `Alpha` (parâmetro de aleatoriedade da fase de construção)
  - `Max Iter` (número máximo de iterações)
- 🧮 **Executar algoritmo GRASP** com heurísticas de melhoria:
  - Reallocation
  - Swap
  - 2-opt
- 📊 **Visualização gráfica das rotas** em tempo real
- 📑 **Tabela da instância** mostrando depósito, entrega e clientes
- 📝 **Listagem textual das rotas** encontradas
- 📏 **Cálculo da distância total** da solução

---

## 🖼️ Estrutura da Interface

A interface é dividida em três áreas principais:

1. **Painel de parâmetros**  
   - Entrada de valores para `Alpha` e `Max Iter`  
   - Botões para abrir instância e rodar algoritmo  

2. **Tabela da instância (lado esquerdo)**  
   - Exibe depósito, ponto de entrega e clientes com coordenadas e demanda  

3. **Painel de rotas (lado direito)**  
   - Gráfico das rotas geradas  
   - Texto listando clientes em cada rota  
   - Distância total da solução  

---

![Rotas geradas](interface.png)

