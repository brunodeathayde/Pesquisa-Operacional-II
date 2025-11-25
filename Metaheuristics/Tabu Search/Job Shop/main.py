from scheptk.scheptk import JobShop
import numpy as np
import matplotlib.pyplot as plt

from ts_operators import (
    generate_neighbors,
    select_best
)

# Leitura da instância
instance = JobShop('instance.txt')
n = instance.jobs
m = instance.machines


# Parâmetros
num_neighbors = 20
tabu_tenure = 20
max_iter = 100

# Solução inicial
best_solution = [3,7,1,4,0,2,9,5,6,8,0,3,7,1,4,9,2,6,5,8,1,0,4,7,3,5,2,9,6,8,7,4,0,3,1,6,5,2,9,8,8,6,5,2,9,4,7,3,0,1]
cmax = instance.Cmax(best_solution) 
best_makespan = cmax
print("The initial solution is: ", cmax)

# Inicializando a lista de movimentos proibidos
tabu_list = []
best_solution_found = []

for iteration in range(1, max_iter + 1): 
    neighbors = generate_neighbors(best_solution, num_neighbors)
    chosen_solution, chosen_makespan, chosen_move = select_best(neighbors, instance, tabu_list, best_makespan)
    tabu_list.append(chosen_move)
    if len(tabu_list) > tabu_tenure:
        tabu_list.pop(0) # Remove o primeiro elemento da lista            
    if chosen_makespan < best_makespan:
            best_solution, best_makespan = chosen_solution, chosen_makespan
    best_solution_found.append(best_makespan)


# Resultado final
print("The best solution found: ", best_makespan)
plt.plot(best_solution_found, color='blue')
plt.xlabel('Iteração')
plt.ylabel('Makespan')
plt.legend()
plt.grid(True)
plt.show()

instance.print_schedule(best_solution, 'Makespan.png')
