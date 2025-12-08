# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 20:02:04 2016

@author: brunoprata
"""
import numpy as np

def leftovers(A,x):
    uncovered = np.array([0 for j in range (len(A))])
    #covering = np.array([[0 for j in range (len(A[0]))] for i in range (len(A))])
    covering = A*x
    for i in range(len(A)):
        for j in range (len(A[0])):
            uncovered[i] = uncovered[i] + covering[i][j]   
    k=0
    for i in range(len(uncovered)):
        if (uncovered[i]==0):
            k+=1           
    return(k)
            
    