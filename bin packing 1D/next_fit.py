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




"""
Definir capacidade_da_caixa ← C
Inicializar lista_de_itens ← [i₁, i₂, ..., iₙ]
Inicializar número_de_caixas ← 1
Inicializar espaço_disponível ← C

PARA cada item em lista_de_itens FAÇA:
    SE item ≤ espaço_disponível ENTÃO
        Colocar item na caixa atual
        Atualizar espaço_disponível ← espaço_disponível - item
    SENÃO
        Abrir nova caixa
        número_de_caixas ← número_de_caixas + 1
        espaço_disponível ← C - item
        Colocar item na nova caixa
FIM PARA

Exibir número_de_caixas
"""
