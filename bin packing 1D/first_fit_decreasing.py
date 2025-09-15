def first_fit_decreasing(itens, capacidade):
    # Ordena os itens em ordem decrescente
    itens_ordenados = sorted(itens, reverse=True)
    bins = []  # Lista de bins, cada bin é uma lista de itens

    for item in itens_ordenados:
        colocado = False

        # Tenta colocar o item na primeira bin que tenha espaço
        for bin in bins:
            espaco_livre = capacidade - sum(bin)
            if espaco_livre >= item:
                bin.append(item)
                colocado = True
                break

        # Se não couber em nenhuma bin existente, cria uma nova
        if not colocado:
            bins.append([item])

    return bins
