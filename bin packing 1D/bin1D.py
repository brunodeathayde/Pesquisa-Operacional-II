from mip import Model, xsum, BINARY
import math

#l = [3, 4, 5, 2, 2, 1, 3, 3]
#L, N = 6, range(len(l))

l = [1.5, 2.8, 2.4, 3.3, 3.5, 1.25, 0.85, 2.45, 4.1, 3.6, 2.7, 1.3, 3.8, 1.75, 3.8, 0.75, 1.85, 2.1]
L, N = 12, range(len(l))

M = range(math.ceil(sum(l)/L))

model = Model("bin1D")

y = [model.add_var(var_type=BINARY) for i in M]
x = [[model.add_var(var_type=BINARY) for j in N] for i in M]

model.objective = xsum(y[i] for i in M)

for j in N:
    model.add_constr(xsum(x[i][j] for i in M) == 1)

for i in M:
    model.add_constr(xsum(l[j]*x[i][j] for i in M) <= L*y[i])

model.optimize()

bins = [i for i in M if y[i].x >= 0.99]
print("selected bins: {}".format(bins))
print("Solution found: ", model.objective_value)



