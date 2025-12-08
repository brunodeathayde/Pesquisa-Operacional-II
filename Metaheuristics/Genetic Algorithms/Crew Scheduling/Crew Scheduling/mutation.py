
from random import randint

def mutation(pmut,offspring):
    rand = randint(1,100)    
    if (rand<=pmut):
        rand = randint(0,len(offspring)-1)
        if (offspring[rand]==0):
            offspring[rand]=1
        else:
            offspring[rand]=0
    return(offspring)
