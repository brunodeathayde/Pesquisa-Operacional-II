# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:01:56 2016

@author: brunoprata
"""
import numpy as np

def replacement (pop,fitness,offspring,fitness_offspring):
    worse = np.argmax(fitness)
    #print(worse)
    #print(fitness)
    pop[worse]=offspring
    #print(pop[worse])
    fitness[worse]=fitness_offspring
    return(pop,fitness)