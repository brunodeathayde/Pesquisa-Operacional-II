
from mip import Model, xsum, minimize, BINARY

p = [64, 53, 63, 99, 189, 44, 50, 22]
d = [100, 70, 150, 601, 118, 590, 107, 180]

#p = [2,3,5,1,4]
#d = [3,5,6,8,9]


n = len(p)

model = Model("single_machine")

T = [model.add_var() for j in range(n)]
C = [model.add_var() for j in range(n)]
x = [[model.add_var(var_type=BINARY) for j in range(n)] for i in range(n)]

model.objective = minimize(xsum(T[j] for j in range(n)))

# constraints
for j in range(n):
    model.add_constr(xsum(x[i][j] for i in range(n)) == 1)

for i in range(n):
    model.add_constr(xsum(x[i][j] for j in range(n)) == 1)

model.add_constr(C[0] == xsum(p[i]*x[i][0] for i in range(n)))

for j in range(1,n):
    model.add_constr(C[j] >= C[j-1] + xsum(p[i]*x[i][j] for i in range(n)))

for j in range(n):
    model.add_constr(T[j] >= C[j] - xsum(d[i]*x[i][j] for i in range(n)))

model.optimize()

print("Solution found: ", model.objective_value)

for j in range(n):
          print("C[",j+1,"] =",C[j].x)

for j in range(n):
          print("T[",j+1,"] =",T[j].x)

for i in range(n):
    for j in range(n):
        if x[i][j].x >= 0.99:
            print("x[",i,"][",j,"]")
