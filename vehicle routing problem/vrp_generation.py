# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:53:57 2016

@author: brunoprata
"""
from random import randint 

n = 5   # número de clientes
K = 20   # capacidade máxima
m = 1    # número de instâncias a gerar

for k in range(m):
    file_name = f"VRP-{k+1}.txt"
    
    with open(file_name, "w") as file:
        for i in range(n):
            r1 = randint(-10*n, 10*n)      # coordenada x
            r2 = randint(-10*n, 10*n)      # coordenada y
            r3 = randint(1, K//2)          # demanda (inteiro)
            
            file.write(f"{r1}  {r2}  {r3}\n")
