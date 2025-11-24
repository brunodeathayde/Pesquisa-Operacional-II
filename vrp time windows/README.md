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
