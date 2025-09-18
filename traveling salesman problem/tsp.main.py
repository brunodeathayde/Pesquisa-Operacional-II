# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:52:37 2016

@author: brunoprata
"""

from tsp_reading import tsp_reading
from distance_matrix import distance_matrix
from random_route_tsp import random_route_tsp
from plotting_route import plotting_route


file_name= "TSP-1.txt"
data=tsp_reading(file_name)
n = len(data)
route = random_route_tsp(n)
plotting_route(n,route,data)