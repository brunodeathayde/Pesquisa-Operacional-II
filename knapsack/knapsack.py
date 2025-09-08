from mip import Model, xsum, maximize, BINARY

p = [1, 10,	12,	8,	5,	16,	11,	17,	4,	6]
w = [3,	12,	20,	15,	8,	14,	9,	22,	7,	13]

W, I = 104, range(len(w))

m = Model("knapsack")

x = [m.add_var(var_type=BINARY) for i in I]

m.objective = maximize(xsum(p[i] * x[i] for i in I))

m += xsum(w[i] * x[i] for i in I) <= W

m.optimize()

selected = [i for i in I if x[i].x >= 0.99]
print("selected items: {}".format(selected))
print("Solution found: ", m.objective_value)
