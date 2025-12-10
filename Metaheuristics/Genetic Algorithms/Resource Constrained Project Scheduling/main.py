import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from rcpsp_operators import(
    read_instance_rcpsp,
    evolutionary_algorithm_rcpsp,
    build_schedule,
    plot_gantt,
    plot_resource_usage
)

# Exemplo de uso
file_name = "RCPSP-1.txt"  # substitua pelo nome do seu arquivo
n_activities, n_resources, resource_capacities, activities = read_instance_rcpsp(file_name)


# Parâmetros
pop_size = 20
prob_mut = 5
num_gen = 100

# Inicialização
best_solution, best_makespan = evolutionary_algorithm_rcpsp(file_name, pop_size, num_gen, prob_mut)


# Reconstituir activities e resource_capacities para o Gantt
# (se estiver fora de escopo, reler a instância)
_, _, resource_capacities, activities = read_instance_rcpsp(file_name)

schedule, resource_usage, makespan = build_schedule(best_solution, activities, resource_capacities)
print(f"Makespan (confirmado): {makespan}")

plot_gantt(schedule, title="RCPSP - Gantt chart (Best solution)")
plot_resource_usage(resource_usage, resource_capacities, title="RCPSP - Resource usage")


