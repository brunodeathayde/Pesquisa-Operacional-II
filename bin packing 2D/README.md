├── milp_bin_2D.py                # Modelo exato com programação inteira para o problema não-guilhotinado

├── first_fit_decreasing_height.py # Heurística FFDH (First Fit Decreasing Height)

├── best_fit_decreasing_height.py  # Heurística BFDH (Best Fit Decreasing Height)

├── guillotine_ffdh.py             # Heurística FFDH com cortes guilhotinados

├── guillotine_bfdh.py             # Heurística BFDH com cortes guilhotinados

├── README.md                      # Este arquivo

🧩 Descrição do Problema
Dado um conjunto de retângulos com diferentes larguras e alturas, e um espaço bidimensional fixo (bin), o objetivo é alocar os itens de forma que:
Nenhum item ultrapasse os limites do bin.
Os itens não se sobreponham.
O número total de bins utilizados seja minimizado.
Esse problema é comum em aplicações como corte de chapas metálicas, embalagens, impressão gráfica e alocação de recursos visuais.
🧠 Abordagens Implementadas
1. Modelo Exato com Python MIP (milp_bin_2D.py)
Utiliza programação inteira para encontrar a solução ótima:
Cada bin é representado por uma variável binária.
Cada item é alocado exatamente uma vez.
Restrições garantem que os itens não se sobreponham.
A função objetivo minimiza o número total de bins utilizados.
O modelo considera o problema não-guilhotinado, ou seja, sem restrições de corte contínuo.

3. Heurísticas Clássicas
## ⚡ Algoritmos Heurísticos

Algoritmos rápidos que produzem boas soluções (não necessariamente ótimas):

| Heurística                      | Estratégia                                                                 |
|--------------------------------|----------------------------------------------------------------------------|
| `first_fit_decreasing_height.py` | Ordena os itens por altura decrescente e aloca no primeiro bin disponível. |
| `best_fit_decreasing_height.py`  | Ordena por altura decrescente e aloca no bin que deixa o menor espaço livre. |
| `guillotine_ffdh.py`             | Variante FFDH com cortes guilhotinados (cortes retos horizontais/verticais). |
| `guillotine_bfdh.py`             | Variante BFDH com cortes guilhotinados.                                     |



