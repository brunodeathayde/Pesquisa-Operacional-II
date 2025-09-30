🚚 Vehicle Routing Problem (VRP) 
Este repositório contém uma implementação do Problema de Roteamento de Veículos (VRP), utilizando heurísticas e ferramentas de visualização para gerar, resolver e analisar instâncias do problema.

📁 Estrutura dos Arquivos

| Arquivo                | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| `main.py`              | Script principal que integra todas as etapas do processo.                |
| `gillet_miller.py`     | Implementação da heurística de Gillet-Miller para construção de rotas.   |
| `plotting_route_vrp.py`| Funções de visualização das rotas geradas em gráficos.                   |
| `route_cost.py`        | Cálculo do custo total das rotas (distância, número de veículos, etc).   |
| `vrp_generation.py`    | Geração de instâncias do VRP com clientes, depósitos e capacidades.       |
| `vrp_reading.py`       | Leitura de instâncias a partir de arquivos ou formatos específicos.       |


🧠 Metodologia
A abordagem utilizada envolve:
Geração de instâncias aleatórias ou leitura de arquivos.
Aplicação da heurística de Gillet-Miller para construção inicial das rotas.
Cálculo do custo total das rotas.
Visualização gráfica das soluções.
