# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 08:35:55 2016

@author: brunoprata
"""
import numpy 

def gillet_miller(n, P):
    s = [0 for i in range(n)]
    for i in range(n):
        # Evita divisão por zero e calcula ângulo polar
        x, y = P[i][0], P[i][1]
        #s[i] = numpy.arctan2(y, x)
        #s[i] = numpy.degrees(numpy.arctan2(y, x))
        #s[i] = round(numpy.degrees(numpy.arctan2(y, x)), 2)
        s[i] = numpy.degrees(numpy.arctan2(y, x)) % 360


    print(", ".join(f"{valor:.1f}" for valor in s))
 


    route = [i + 1 for i in sorted(range(n), key=lambda k: s[k])]
    return route

