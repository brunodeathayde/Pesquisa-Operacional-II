from mip import Model, xsum, minimize, BINARY

# Conjuntos
I = range(1, 4)  # itens: 1, 2, 3
T = range(1, 5)  # períodos: 1 a 4

# Parâmetros bidimensionais: f[i][t], p[i][t], h[i][t], d[i][t], C[i][t]
f = {i: {t: 2 + i + t for t in T} for i in I}  # custo fixo de produção
p = {i: {t: 1 + i for t in T} for i in I}      # custo unitário de produção
h = {i: {t: 2 + t for t in T} for i in I}      # custo unitário de estocagem
d = {i: {t: 3 + i + t for t in T} for i in I}  # demanda por item e período
C = {i: {t: 10 for t in T} for i in I}         # capacidade por item e período

# Criação do modelo
model = Model("multi_item_lot_sizing_2D")

# Variáveis de decisão
x = {(i, t): model.add_var(name=f"x_{i}_{t}") for i in I for t in T}                  # produção
s = {(i, t): model.add_var(name=f"s_{i}_{t}") for i in I for t in T}                  # estoque
y = {(i, t): model.add_var(var_type=BINARY, name=f"y_{i}_{t}") for i in I for t in T} # produção ativa

# Função objetivo
model.objective = minimize(
    xsum(p[i][t] * x[i, t] + h[i][t] * s[i, t] + f[i][t] * y[i, t] for i in I for t in T)
)

# Balanço de estoque
for i in I:
    for t in T:
        if t == 1:
            model.add_constr(x[i, t] == d[i][t] + s[i, t], name=f"estoque_{i}_{t}")
        else:
            model.add_constr(s[i, t - 1] + x[i, t] == d[i][t] + s[i, t], name=f"estoque_{i}_{t}")

# Ativação da produção
for i in I:
    for t in T:
        model.add_constr(x[i, t] <= C[i][t] * y[i, t], name=f"ativacao_{i}_{t}")

# Otimização
model.optimize()

# Resultados
print("Solução encontrada:", model.objective_value)
for i in I:
    for t in T:
        print(f"Item {i}, Período {t}: Produção = {x[i, t].x:.2f}, Estoque = {s[i, t].x:.2f}, Produz? = {int(y[i, t].x)}")
from mip import Model, xsum, minimize, BINARY

# Conjuntos
I = range(1, 4)  # itens: 1, 2, 3
T = range(1, 5)  # períodos: 1 a 4

# Parâmetros bidimensionais: f[i][t], p[i][t], h[i][t], d[i][t], C[i][t]
f = {i: {t: 2 + i + t for t in T} for i in I}  # custo fixo de produção
p = {i: {t: 1 + i for t in T} for i in I}      # custo unitário de produção
h = {i: {t: 2 + t for t in T} for i in I}      # custo unitário de estocagem
d = {i: {t: 3 + i + t for t in T} for i in I}  # demanda por item e período
C = {i: {t: 10 for t in T} for i in I}         # capacidade por item e período

# Criação do modelo
model = Model("multi_item_lot_sizing_2D")

# Variáveis de decisão
x = {(i, t): model.add_var(name=f"x_{i}_{t}") for i in I for t in T}                  # produção
s = {(i, t): model.add_var(name=f"s_{i}_{t}") for i in I for t in T}                  # estoque
y = {(i, t): model.add_var(var_type=BINARY, name=f"y_{i}_{t}") for i in I for t in T} # produção ativa

# Função objetivo
model.objective = minimize(
    xsum(p[i][t] * x[i, t] + h[i][t] * s[i, t] + f[i][t] * y[i, t] for i in I for t in T)
)

# Balanço de estoque
for i in I:
    for t in T:
        if t == 1:
            model.add_constr(x[i, t] == d[i][t] + s[i, t], name=f"estoque_{i}_{t}")
        else:
            model.add_constr(s[i, t - 1] + x[i, t] == d[i][t] + s[i, t], name=f"estoque_{i}_{t}")

# Ativação da produção
for i in I:
    for t in T:
        model.add_constr(x[i, t] <= C[i][t] * y[i, t], name=f"ativacao_{i}_{t}")

# Otimização
model.optimize()

# Resultados
print("Solução encontrada:", model.objective_value)
for i in I:
    for t in T:
        print(f"Item {i}, Período {t}: Produção = {x[i, t].x:.2f}, Estoque = {s[i, t].x:.2f}, Produz? = {int(y[i, t].x)}")
