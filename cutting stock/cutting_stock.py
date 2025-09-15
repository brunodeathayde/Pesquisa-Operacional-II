from mip import Model, xsum, minimize, INTEGER

# Largura do rolo padrão
L = 12.0

# Comprimentos dos itens (em unidades)
l = [3.0, 4.5, 4.2, 5.0]  # l[j]

# Demandas de cada tipo de item
d = [10, 4, 5, 3]  # d[j]

# Custos unitários por padrão (aqui todos iguais)
c = [1, 1, 1, 1, 1, 1, 1, 1, 1]  # custo por padrão

# Matriz de padrões de corte (linhas = padrões, colunas = itens)
a = [
    [4, 0, 0, 0],
    [1, 2, 0, 0],
    [1, 0, 2, 0],
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [2, 1, 0, 0],
    [2, 0, 1, 0],
    [2, 0, 0, 1]
]

I = len(d)      # número de itens
M = len(a)      # número de padrões

m = Model("cutting_stock")

# Variável: quantas vezes usar cada padrão
x = [m.add_var(var_type=INTEGER) for i in range(M)]

# Minimizar o número total de rolos usados
m.objective = minimize(xsum(c[i] * x[i] for i in range(M)))

# Atender a demanda de cada item j
for j in range(I):
    m += xsum(a[i][j] * x[i] for i in range(M)) >= d[j]

m.optimize()

selected = [i for i in range(M) if x[i].x >= 1e-6]
print("Selected patterns: {}".format(selected))
print("Solution found: ", m.objective_value)
for i in selected:
    print(f"Pattern {i}: use {x[i].x} times")
