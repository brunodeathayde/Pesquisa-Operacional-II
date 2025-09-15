def best_fit(itens, capacidade):
    bins = []  # Lista de bins, cada bin é uma lista de itens

    for item in itens:
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
