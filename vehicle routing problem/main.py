# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:52:37 2016

@author: brunoprata
"""

import matplotlib.pyplot as plt

from vrp_reading import vrp_reading
from gillet_miller import gillet_miller
from route_cost import route_cost
from plotting_route_vrp import plotting_route_vrp

# Capacidade do veículo (frota homogênea)
K=20

# Lendo a instância
file_name= "VRP-1.txt"
P=vrp_reading(file_name)
n=len(P)

# Gerando uma rota com a heurística de Gillet & Miller
route=gillet_miller(n,P)
plotting_route_vrp(P, route, K)

# Imprimindo a solução gerada
dist = route_cost(route, P, K)
print("Rota gerada: ",route)
print("Distância total percorrida: ", dist)

