# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:20:59 2016

@author: brunoprata
"""
import numpy as np

def random_route_tsp (n):
    s = [0 for i in range(n)]
    s = np.random.permutation(n)
    return(s)