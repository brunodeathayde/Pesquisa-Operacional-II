
import numpy as np
from random import randint

def uniform_crossover(n,pop,parent1,parent2):
    offspring = np.array([0 for j in range (n)])
    for j in range(n):
        rand = randint(0,1)
        if (rand==0):
            offspring[j]=pop[parent1][j]
        else:
            offspring[j]=pop[parent2][j]
    #print(offspring)
    return(offspring)
    
    
