def next_fit(itens, capacidade):
    bins = [[]]  # Lista de bins, cada bin é uma lista de itens
    free_bin = capacidade

    for item in itens:
        if free_bin >= item:
            bins[-1].append(item)
            free_bin -= item
        else:
            bins.append([item])
            free_bin = capacidade - item

    return bins
