# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:52:37 2016

@author: brunoprata
"""

from tsp_reading import tsp_reading
from distance_matrix import distance_matrix
from random_route_tsp import random_route_tsp
from plotting_route import plotting_route
from nearest_neighbor_tsp import nearest_neighbor_tsp
from farthest_insertion_tsp import farthest_insertion_tsp
from route_distance import route_distance
from two_opt_best_improvement import two_opt_best_improvement


file_name = "TSP-1.txt"
data = tsp_reading(file_name)
n = len(data)
D = distance_matrix(n,data)
initial_route, initial_dist = nearest_neighbor_tsp(n,D)
plotting_route(n,initial_route,data)
route, best_dist = two_opt_best_improvement(initial_route, initial_dist, D)
plotting_route(n,route,data)
print("*******")
print(f"initial solution: {initial_dist:.2f}")
print("Initial route: ", initial_route)
print(f"Best solution: {best_dist:.2f}")
print("Best route: :", route)
print("*******")
