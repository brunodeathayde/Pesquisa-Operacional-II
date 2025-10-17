📦 Dimensionamento de Lotes — Heurísticas e Modelos MILP

Este repositório reúne heurísticas e modelos de programação matemática para o problema de dimensionamento de lotes, abordando diferentes políticas de reposição e restrições operacionais. Ele é útil para simulações logísticas, otimização de estoques e estudos acadêmicos.

| Arquivo                          | Descrição                                                                 |
|----------------------------------|---------------------------------------------------------------------------|
| `main_heuristics.py`             | Script principal que integra e executa as heurísticas de reposição.       |
| `balance_heuristic.py`           | Heurística de balanceamento de estoque ao longo do tempo.                 |
| `lot_for_lot_heuristic.py`       | Heurística "lote a lote", atende exatamente a demanda de cada período.    |
| `milp_capacitated.py`            | Modelo MILP com restrições de capacidade de produção ou entrega.          |
| `milp_capacitated_multi_item.py` | Extensão do modelo MILP capacitado para múltiplos itens simultâneos.      |
| `milp_uncapacitated.py`          | Modelo MILP sem restrições de capacidade, ideal para cenários flexíveis.  |

🧠 Metodologia

A abordagem utilizada envolve:

    Geração de parâmetros de demanda, lead time e capacidade.

    Aplicação de heurísticas simples para políticas de reposição.

    Formulação e resolução de modelos MILP (Mixed Integer Linear Programming).

    Comparação entre soluções heurísticas e exatas.

📊 Aplicações

    Planejamento de produção e compras.

    Otimização de estoques em cadeias de suprimentos.

    Avaliação de políticas de reposição sob diferentes restrições.

    Ensino e pesquisa em Logística e Gestão da Produção e Operações.
