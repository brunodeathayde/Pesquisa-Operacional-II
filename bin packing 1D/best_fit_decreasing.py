def best_fit_decreasing(itens, capacidade):
    # Ordena os itens em ordem decrescente
    itens_ordenados = sorted(itens, reverse=True)
    bins = []  # Lista de bins, cada bin é uma lista de itens

    for item in itens_ordenados:
        melhor_bin = None
        menor_sobra = capacidade + 1  # Inicializa com valor maior que qualquer sobra possível

        # Procura a bin com menor sobra de espaço que ainda caiba o item
        for bin in bins:
            espaco_livre = capacidade - sum(bin)
            if espaco_livre >= item and espaco_livre - item < menor_sobra:
                melhor_bin = bin
                menor_sobra = espaco_livre - item

        # Se encontrou uma bin adequada, coloca o item nela
        if melhor_bin is not None:
            melhor_bin.append(item)
        else:
            bins.append([item])  # Caso contrário, cria uma nova bin

    return bins
