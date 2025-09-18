├── bin1D.py                # Modelo exato com programação inteira (Python MIP)

├── next_fit.py             # Heurística Next Fit

├── first_fit.py            # Heurística First Fit

├── best_fit.py             # Heurística Best Fit

├── first_fit_decreasing.py # Heurística First Fit com ordenação decrescente

├── best_fit_decreasing.py  # Heurística Best Fit com ordenação decrescente

├── README.md               # Este arquivo

🧩 Descrição do Problema

Dado um conjunto de itens com diferentes larguras e uma largura fixa de rolo (bin), o objetivo é alocar os itens em rolos de forma que:

    Nenhum rolo ultrapasse sua capacidade.

    O número total de rolos utilizados seja minimizado.

Este problema é amplamente aplicado em logística, produção industrial e corte de materiais.

🧠 Abordagens Implementadas
1. Modelo Exato com Python MIP (bin1D.py)

Utiliza programação inteira para encontrar a solução ótima:

    Cada rolo é representado por uma variável binária.

    Cada item é alocado exatamente uma vez.

    A função objetivo minimiza o número total de rolos utilizados.

2. Heurísticas Clássicas

As heurísticas são algoritmos rápidos que produzem boas soluções (não necessariamente ótimas):

| Heurística                | Estratégia                                                                 |
|--------------------------|----------------------------------------------------------------------------|
| `next_fit.py`            | Aloca itens sequencialmente no rolo atual até não caber mais.              |
| `first_fit.py`           | Coloca o item no primeiro rolo disponível com espaço suficiente.           |
| `best_fit.py`            | Coloca o item no rolo que deixará o menor espaço restante.                 |
| `first_fit_decreasing.py`| Ordena os itens em ordem decrescente antes de aplicar First Fit.           |
| `best_fit_decreasing.py` | Ordena os itens em ordem decrescente antes de aplicar Best Fit.            |
