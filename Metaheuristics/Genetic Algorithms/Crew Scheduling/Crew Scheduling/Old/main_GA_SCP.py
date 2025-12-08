# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 07:45:22 2016

@author: baprata
"""
import time
#from scp_generation import scp_generation
#from scp_reading import scp_reading
from genpop import genpop
from fitness_evaluation import fitness_evaluation
from fitness_offspring import fitness_offspring
from selection import selection
from uniform_crossover import uniform_crossover
from mutation import mutation
from replacement import replacement

time_start = time.clock() # Computing initial time

A=[[1,0,0,1,0,1],
   [0,1,0,0,1,1],
   [0,0,1,0,0,0],
   [1,0,0,0,1,0],
   [0,1,0,1,0,1]]
c=[5,3,2,6,1,4]
m=len(A)
n=len(A[0])
"""
A=[[1,0,0,0,1,0,0,0,1,0],
   [0,1,0,0,0,0,0,1,0,1],
   [0,0,0,1,0,0,0,0,0,0],
   [0,0,1,0,1,0,0,1,0,0],
   [0,1,0,0,1,1,0,1,0,1],
   [1,0,0,1,0,0,1,0,1,0],
   [0,0,1,0,0,0,0,1,1,1],
   [0,0,0,1,0,1,0,0,0,0],
   [1,1,0,0,1,0,0,1,0,1],
   [0,0,0,0,0,1,1,1,1,0]]
c=[5,8,10,5,12,4,6,11,13,9]
m=len(A)
n=len(A[0])
"""

#inst=1
#m=20
#n=50
#scp_generation(inst,m,n)
#A,c=scp_reading("SCP-1.txt")


# GA parameters:
popsize=10
gen=100
penalty=1000
pmut=5


pop=genpop(n,popsize)
fitness=fitness_evaluation(A,c,pop,popsize,penalty)

print("Fitness - populacao inicial:")
print(fitness)
#print(fitness)

cont=1
while (cont<=gen):
    #print(cont)
    parent1,parent2=selection(popsize,fitness)
    offspring=uniform_crossover(n,pop,parent1,parent2)
    offspring=mutation(pmut,offspring)
    fo=fitness_offspring(A,c,offspring,penalty)
    #print(fo)
    pop,fitness=replacement(pop,fitness,offspring,fo)
    cont +=1

print("Fitness - populacao final:")
print(fitness)

time_elapsed = (time.clock() - time_start) # Computing finish time
print("Tempo computacional (s):")
print("%.2f" %time_elapsed)

    



