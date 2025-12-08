
import numpy as np;

def selection(popsize,fitness):
    #random_permutation = np.array([0 for j in range (popsize)])
    parents = np.array([0 for j in range (4)])
    random_permutation = np.random.permutation(popsize)
    for i in range(4):
        parents[i] = random_permutation[i]

    if (fitness[parents[0]]< fitness[parents[1]]):
        parent1 = parents[0]
    else:
        parent1 = parents[1]

    if (fitness[parents[2]]< fitness[parents[3]]):
        parent2 = parents[2]
    else:
        parent2 = parents[3]

    return(parent1,parent2) 
