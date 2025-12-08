# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 07:44:02 2016

@author: baprata
"""

from random import randint
import numpy as np; 

def genpop (n,popsize):
    pop = np.array([[randint(0,1) for j in range (n)] for i in range (popsize)])
    return (pop)