import numpy as np

def read_layout(arquivo):
    # Lê todas as linhas do arquivo
    with open(arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Separar blocos de acordo com os comentários
    matriz_distancias = []
    matriz_fluxos = []
    bloco = None

    for linha in linhas:
        linha = linha.strip()
        if not linha:  # pula linhas vazias
            continue
        if linha.startswith("#"):
            if "distâncias" in linha.lower():
                bloco = "dist"
            elif "fluxos" in linha.lower():
                bloco = "flux"
            else:
                bloco = None
            continue

        # Converte números da linha em lista de inteiros
        valores = list(map(int, linha.split()))
        if bloco == "dist":
            matriz_distancias.append(valores)
        elif bloco == "flux":
            matriz_fluxos.append(valores)

    return np.array(matriz_distancias), np.array(matriz_fluxos)


