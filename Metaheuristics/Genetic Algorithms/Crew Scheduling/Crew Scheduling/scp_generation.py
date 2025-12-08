# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 07:48:21 2016

@author: baprata
"""

from random import randint

"""
inst: número de instâncias
m: número de linhas da matriz A
n: número de colunas da matriz A
"""
def scp_generation(inst,m,n):

    for k in range(inst):
        str_file_name = "SCP-"
        file_name = str_file_name + str(k+1)+ ".txt"
        file = open(file_name, "w")
    
        for i in range(m):
            for j in range(n):
                r=randint(0,1)
                file.write("%i" %(r))
                file.write("  ")
            file.write("\n") 

        for j in range(n):
            r=randint(1,10)
            file.write("%i" %(r))
            file.write("  ")
            
        file.close()
    print("Test instances were suscessfully generated!")