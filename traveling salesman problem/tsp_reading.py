# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:58:57 2016

@author: brunoprata
"""

from numpy import loadtxt

def tsp_reading(file_name):
    data = loadtxt(file_name);
    return(data);