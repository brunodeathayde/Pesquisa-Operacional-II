from mip import Model, xsum, minimize, BINARY

f = [0, 3, 1, 4, 6]
p = [0, 2, 1, 5, 8]
h = [0, 4, 2, 5, 5]
d = [0, 5, 3, 8, 10]
M = sum(d)
n = len(d)

model = Model("uncapacitated")

x = [model.add_var() for t in range(n)]
s = [model.add_var() for t in range(n)]
y = [model.add_var(var_type=BINARY) for t in range(n)] 

model.objective = minimize(xsum(p[t]*x[t] for t in range(1,n))+xsum(h[t]*s[t] for t in range(1,n))+xsum(f[t]*y[t] for t in range(1,n)))

for t in range(1,n):
    model.add_constr(s[t-1] +x[t] == d[t] + s[t])

for t in range(1,n):
    model.add_constr(x[t] <= M*y[t])

model.optimize()

print("Solution found: ", model.objective_value)

for t in range(1,n):
    print("x[",t,"]",x[t].x, "s[",t,"]",s[t].x)

for t in range(1,n):
    if y[t].x >= 0.99:
        print("y[",t,"]")