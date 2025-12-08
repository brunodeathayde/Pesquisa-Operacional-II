# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 08:21:53 2016

@author: brunoprata
"""
import numpy as np
from leftovers import leftovers


def fitness_evaluation(A,c,pop,popsize,penalty):
    fitness = np.array([0 for j in range (popsize)])   
    for j in range(popsize):
        x=pop[j]
        k=leftovers(A,x)
        #print(u,k)
        fitness[j]=sum(c*x)+(penalty*k)
    return(fitness)