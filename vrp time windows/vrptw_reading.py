from numpy import loadtxt
import numpy as np

def vrptw_reading(file_name):
    data = np.loadtxt(file_name)

    # Converte cada linha em lista [x, y, demanda, inicioTW, fimTW]
    P = data.tolist()

    return P

