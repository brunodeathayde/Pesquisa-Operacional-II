from mip import Model, xsum, minimize, BINARY

# Conjuntos
I = range(1, 4)  # itens
T = range(1, 5)  # períodos

# Parâmetros bidimensionais
f = {i: {t: 2 + i + t for t in T} for i in I}
p = {i: {t: 1 + i for t in T} for i in I}
h = {i: {t: 2 + t for t in T} for i in I}
d = {i: {t: 3 + i + t for t in T} for i in I}
C = {i: {t: 10 for t in T} for i in I}
s0 = {i: 0 for i in I}  # estoque inicial fixo

# Modelo
model = Model("multi_item_lot_sizing_with_initial_stock")

# Variáveis
x = {(i, t): model.add_var(name=f"x_{i}_{t}") for i in I for t in T}
s = {(i, t): model.add_var(name=f"s_{i}_{t}") for i in I for t in range(0, 5)}  # inclui t=0
y = {(i, t): model.add_var(var_type=BINARY, name=f"y_{i}_{t}") for i in I for t in T}

# Função objetivo
model.objective = minimize(
    xsum(p[i][t] * x[i, t] + h[i][t] * s[i, t] + f[i][t] * y[i, t] for i in I for t in T)
)

# Estoque inicial fixo
#for i in I:
    #model.add_constr(s[i, 0] == s0[i], name=f"estoque_inicial_{i}")

# Balanço de estoque
for i in I:
    for t in T:
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

