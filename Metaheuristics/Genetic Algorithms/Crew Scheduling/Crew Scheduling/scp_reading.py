import numpy as np

def scp_reading(file_name):
    # Lê todo o arquivo, números separados por espaço
    data = np.loadtxt(file_name, dtype=int)

    # Última linha = vetor de custos
    c = data[-1, :]            # vetor de custos (1D)

    # Todas as linhas anteriores = matriz binária
    A = data[:-1, :]           # matriz de restrições (2D)

    return A, c
