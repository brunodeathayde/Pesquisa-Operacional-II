# -*- coding: utf-8 -*-
"""
Leitura de instância para o problema de p-medianas
@author: brunoprata
"""

import numpy as np

def pmedian_reading(file_name):
    """
    Lê uma instância do problema de p-medianas.
    Formato esperado:
    - Primeira linha: número de medianas (p)
    - Linhas seguintes: coordenadas (x, y) dos clientes
    """
    with open(file_name, "r") as f:
        # primeira linha = número de medianas
        p = int(f.readline().strip())
    
    # carrega o restante como matriz de coordenadas
    coords = np.loadtxt(file_name, skiprows=1)
    
    return p, coords
