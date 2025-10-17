from lot_for_lot_heuristic import lot_for_lot_heuristic
from balance_heuristic import balance_heuristic

# Dados do problema
f = [0, 3, 1, 4, 6]   # custo fixo de produção
p = [0, 2, 1, 5, 8]   # custo unitário de produção
h = [0, 4, 2, 5, 5]   # custo de estocagem (não usado na heurística)
d = [0, 5, 3, 8, 10]  # demanda por período

# Executa a heurística lote-por-lote
x, s, y, custo_total = balance_heuristic(d, p, f, h)

# Exibe os resultados
print("Produção por período:", x[1:])
print("Estoque por período:", s[1:])
print("Indicador de produção:", y[1:])
print("Custo total:", custo_total)
