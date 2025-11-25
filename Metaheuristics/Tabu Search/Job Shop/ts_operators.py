import random
import numpy as np
import random

# Gera um conjunto de soluções vizinhas usando swap
def generate_neighbors(solution, num_neighbors=10):
    neighbors = []
    moves = []   # guarda os movimentos realizados
    n = len(solution)

    for _ in range(num_neighbors):
        new_sol = solution.copy()
        i, j = random.sample(range(n), 2)
        new_sol[i], new_sol[j] = new_sol[j], new_sol[i]

        neighbors.append((new_sol, (min(i,j), max(i,j))))  # solução + movimento
        moves.append((min(i,j), max(i,j)))

    return neighbors

# Seleciona a melhor solução na vizinhança avaliada
def select_best(neighbors, instance, tabu_list, best_makespan):
    chosen_solution, chosen_makespan = None, float("inf")
    chosen_move = None

    for sol, move in neighbors:   # agora cada vizinho tem (solução, movimento)
        fit = instance.Cmax(sol)  # calcula makespan

        if move in tabu_list:
            # Aspiração: aceita se melhora o melhor global
            if fit < best_makespan and fit < chosen_makespan:
                chosen_solution, chosen_makespan, chosen_move = sol, fit, move
        else:
            if fit < chosen_makespan:
                chosen_solution, chosen_makespan, chosen_move = sol, fit, move

    return chosen_solution, chosen_makespan, chosen_move



