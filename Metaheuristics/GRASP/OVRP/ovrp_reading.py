from numpy import loadtxt

def ovrp_reading(file_name):
    # Lê todo o arquivo como matriz (cada linha: x, y, demanda)
    data = loadtxt(file_name)
    
    # Separação
    deposito = data[0]          # primeira linha
    entrega = data[1]           # segunda linha
    clientes = data[2:]         # demais linhas
    
    return deposito, entrega, clientes