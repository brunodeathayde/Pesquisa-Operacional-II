import numpy as np

p = [1, 10,	12,	8,	5,	16,	11,	17,	4,	6]
w = [3,	12,	20,	15,	8,	14,	9,	22,	7,	13]
c, N = 104, len(w)

value_per_unit = [0]*N
selected_items = []
objective_function = 0

for i in range(N):
	value_per_unit[i] = p[i]/w[i]

items = np.flip(np.argsort(value_per_unit))

for i in range(N):
	if w[items[i]]<=c:
		selected_items.append(items[i])
		objective_function += p[items[i]]
		c = c - w[items[i]]
		
print("Total value: ", objective_function)
print("Selected items: ",selected_items)
