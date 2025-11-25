# -*- coding: utf-8 -*-
"""
Gerador de instâncias para o problema de p-medianas
@author: brunoprata
"""

from random import randint 

n = 50   # número de pontos (clientes)
m = 1   # número de instâncias a gerar
p = 10   # número de medianas

for k in range(m):
    str_file_name = "pmedian-"
    file_name = str_file_name + str(k+1) + ".txt"
    with open(file_name, "w") as file:
        
        # primeira linha: número de medianas
        file.write("%i\n" % p)
        
        # matriz de coordenadas (x, y)
        for i in range(n):
            r1 = randint(-10*n, 10*n)
            r2 = randint(-10*n, 10*n)
            file.write("%i  %i\n" % (r1, r2))


