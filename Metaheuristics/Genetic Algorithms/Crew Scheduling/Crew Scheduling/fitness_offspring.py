# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 06:43:39 2016

@author: brunoprata
"""

from leftovers import leftovers


def fitness_offspring(A,c,offspring,penalty):
    x=offspring
    k=leftovers(A,x)
    #print(u,k)
    fitness_offspring=sum(offspring*c)+(penalty*k)
    return(fitness_offspring)