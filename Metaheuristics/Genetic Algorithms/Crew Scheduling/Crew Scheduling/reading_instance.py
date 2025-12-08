import numpy as np

def reading_instance(arquivo="matrix_services.csv"):
    """
    Lê um arquivo no formato:
    - Primeira linha: vetor de custos dos serviços
    - Linhas seguintes: matriz binária (viagens x serviços)
    """
    with open(arquivo, "r") as f:
        linhas = [line.strip() for line in f if line.strip()]

    # Primeira linha = custos
    custos = np.array(list(map(int, linhas[0].split(","))))

    # Restante = matriz binária
    matriz = np.array([list(map(int, linha.split(","))) for linha in linhas[1:]])

    return custos, matriz


