from tsp_reading import tsp_reading
from distance_matrix import distance_matrix
from mip import Model, xsum,  minimize, BINARY
import math


file_name = "TSP-1.txt"
data = tsp_reading(file_name)
N = len(data)
c = distance_matrix(N,data)

model = Model("TSP")

# variáveis auxiliares de eliminação de subciclo (MTZ)
u = [model.add_var(name=f"u({i})", lb=0, ub=N-1) for i in range(N)]

# variáveis binárias x[i][j] = 1 se a aresta (i,j) for usada
x = [[model.add_var(var_type=BINARY, name=f"x({i},{j})") for j in range(N)] for i in range(N)]

# função objetivo: minimizar custo total
model.objective = minimize(xsum(c[i][j] * x[i][j] for i in range(N) for j in range(N)))

# cada cidade deve ter exatamente uma saída
for i in range(N):
    model.add_constr(xsum(x[i][j] for j in range(N) if j != i) == 1)

# cada cidade deve ter exatamente uma entrada
for j in range(N):
    model.add_constr(xsum(x[i][j] for i in range(N) if i != j) == 1)

# restrições MTZ (eliminação de subciclos)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            model.add_constr(u[i] - u[j] + N * x[i][j] <= N - 1)

model.optimize()

print("Custo ótimo:", model.objective_value)

