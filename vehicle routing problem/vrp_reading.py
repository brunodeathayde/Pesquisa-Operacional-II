# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 09:18:18 2016

@author: brunoprata
"""

from numpy import loadtxt

def vrp_reading(file_name):
    data = loadtxt(file_name);
    return(data);