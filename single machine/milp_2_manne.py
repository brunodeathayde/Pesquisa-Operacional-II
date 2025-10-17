from mip import Model, xsum, minimize, BINARY

# Dados
p = [64, 53, 63, 99, 189, 44, 50, 22]  # tempos de processamento
d = [100, 70, 150, 601, 118, 590, 107, 180]  # prazos
n = len(p)
M = sum(p)   # constante grande

# Modelo
model = Model("single_machine_ordering")

# Variáveis
T = [model.add_var(name=f"T_{i}", lb=0) for i in range(n)]  # atraso
C = [model.add_var(name=f"C_{i}", lb=0) for i in range(n)]  # tempo de conclusão
x = [[model.add_var(var_type=BINARY, name=f"x_{i}_{j}") if i < j else None for j in range(n)] for i in range(n)]  # precedência

# Função objetivo
model.objective = minimize(xsum(T[i] for i in range(n)))

# Restrições
for i in range(n):
    model.add_constr(T[i] >= C[i] - d[i], name=f"atraso_{i}")
    model.add_constr(C[i] >= p[i], name=f"tempo_min_{i}")

for i in range(n - 1):
    for j in range(i + 1, n):
        model.add_constr(C[i] <= C[j] - p[j] + M * (1 - x[i][j]), name=f"precede_{i}_{j}")
        model.add_constr(C[j] <= C[i] - p[i] + M * x[i][j], name=f"precede_{j}_{i}")

# Otimização
model.optimize()

# Resultados
print("Solução encontrada:", model.objective_value)
for i in range(n):
    print(f"C[{i+1}] = {C[i].x:.2f}, T[{i+1}] = {T[i].x:.2f}")
for i in range(n - 1):
    for j in range(i + 1, n):
        if x[i][j].x >= 0.99:
            print(f"Tarefa {i+1} precede {j+1}")
        elif x[i][j].x <= 0.01:
            print(f"Tarefa {j+1} precede {i+1}")
