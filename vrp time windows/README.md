# 🚚 Vehicle Routing Problem with Time Windows (VRPTW)

Este repositório contém uma implementação do **Problema de Roteamento de Veículos com Janelas de Tempo (VRPTW)**.  
O objetivo é encontrar rotas para uma frota de veículos que atendam clientes em horários específicos, minimizando o custo total.

---

## 📂 Estrutura do Repositório

- `VRPTW-1.txt` → Instância do problema (clientes, coordenadas, demandas, janelas de tempo).
- `main.py` → Script principal.
- `route_cost.py` → Função para calcular o custo total de uma rota (distância, capacidade dos veículos, janelas de tempo).
- `vrptw_generation.py` → Utilitário para gerar instâncias VRPTW artificiais.
- `vrptw_reading.py` → Função para ler instâncias VRPTW a partir de arquivo `.txt`.

---

# Open Vehicle Routing Problem with Time Windows (OVRPTW) 

Este repositório inclui uma implementação simples em Python para cálculo de rotas no **Open Vehicle Routing Problem** com janelas de tempo. 
Diferente do VRP clássico, no OVRP os veículos **não retornam ao depósito** após atender os clientes: cada rota começa no depósito e termina em um cliente final.

---

## 📌 Funcionalidade

A função principal é:

```python
def route_cost_open(route, P, capacity, deposito, destino_final, tempo_servico=0)

## 📌 Parâmetros

```python
route: lista de índices dos clientes na ordem de atendimento.

P: lista de pontos, onde cada ponto é definido como 
   [x, y, demanda, inicio_janela, fim_janela].

capacity: capacidade máxima do veículo.

deposito: tupla (x_dep, y_dep) com coordenadas do depósito.

destino_final: tupla (x_dest, y_dest) com coordenadas do cliente final 
               (onde a rota termina).

tempo_servico (opcional): tempo de atendimento em cada cliente (default = 0).

