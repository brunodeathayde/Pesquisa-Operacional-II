from mip import Model, xsum, BINARY
import math

# Dimensões dos itens
w = [1.5, 2.8, 2.4, 3.3, 3.5, 1.25, 0.85, 2.45, 4.1, 3.6, 2.7, 1.3, 3.8, 1.75, 3.8, 0.75, 1.85, 2.1]
h = [1.0, 1.2, 1.1, 1.5, 1.3, 0.9, 0.6, 1.0, 1.8, 1.4, 1.2, 0.8, 1.6, 1.0, 1.7, 0.5, 0.9, 1.1]

# Dimensões do bin
W = 6
H = 4

n = len(w)
m = n  # número máximo de bins

model = Model("bin2D")

# Variáveis de decisão
q = [model.add_var(var_type=BINARY) for k in range(m)]  # bin k é usado
y = [model.add_var(var_type=BINARY) for i in range(n)]  # item i inicia empilhamento
x = [[model.add_var(var_type=BINARY) for j in range(n)] for i in range(n)]  # item j empilhado sobre i
z = [[model.add_var(var_type=BINARY) for i in range(n)] for k in range(m)]  # item i alocado no bin k

# Função objetivo: minimizar número de bins usados
model.objective = xsum(q[k] for k in range(m))

# Cada item deve ser empilhado sobre outro ou iniciar empilhamento
for j in range(n):
    model.add_constr(xsum(x[i][j] for i in range(j)) + y[j] == 1)

# Largura acumulada da pilha sobre item i não excede espaço restante
for i in range(n - 1):
    model.add_constr(xsum(w[j] * x[i][j] for j in range(i + 1, n)) <= (W - w[i]) * y[i])

# Cada item é alocado em um bin
for i in range(n):
    model.add_constr(xsum(z[k][i] for k in range(i)) + q[i] == y[i])

# Altura acumulada dos itens no bin k não excede H
for k in range(n - 1):
    model.add_constr(xsum(h[i] * z[k][i] for i in range(k + 1, n)) <= (H - h[k]) * q[k])

# Otimização
model.optimize()

# Resultados
bins_usados = [k for k in range(m) if q[k].x >= 0.99]
print("Bins utilizados:", bins_usados)
print("Valor objetivo:", model.objective_value)
