from mip import Model, xsum, minimize

s = [40, 60]
d = [25, 35, 40]
c = [[6, 4, 8],
     [3, 2, 5]]
M = len(s)
N = len(d)

model = Model("transport")

x = [[model.add_var() for j in range(N)] for i in range(M)]

model.objective = minimize(xsum(c[i][j]*x[i][j] for i in range(M) for j in range(N)))

for i in range(M):
    model.add_constr(xsum(x[i][j] for j in range(N)) == s[i])

for j in range(N):
    model.add_constr(xsum(x[i][j] for i in range(M)) == d[j])

model.optimize()

print("Solution found: ", model.objective_value)
for i in range(M):
     for j in range(N):
          print("Flow from ",i+1,"to ",j+1,":",x[i][j].x)