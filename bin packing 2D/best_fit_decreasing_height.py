def best_fit_decreasing_height(itens, largura_bin, altura_bin, allow_rotation=True):
    """
    Heurística Best Fit Decreasing Height (BFDH).
    - Ordena itens por altura decrescente.
    - Coloca cada item no bin/shelf onde "se ajusta melhor" (menor altura sobrando).
    """
    # Pré-processamento: rotação se necessário
    itens_rotacionados = []
    for w, h in itens:
        if w <= largura_bin and h <= altura_bin:
            itens_rotacionados.append((w, h))
        elif allow_rotation and h <= largura_bin and w <= altura_bin:
            itens_rotacionados.append((h, w))
        else:
            raise ValueError(f"Item {(w,h)} não cabe no bin ({largura_bin}x{altura_bin}), mesmo com rotação.")
    
    # Ordena por altura decrescente
    itens_ordenados = sorted(itens_rotacionados, key=lambda x: x[1], reverse=True)

    bins = []

    for w, h in itens_ordenados:
        melhor_bin = None
        melhor_shelf = None
        melhor_sobra = None

        # Examina cada bin existente
        for b in bins:
            # 1) tentar nas shelves existentes
            for shelf in b["shelves"]:
                if h <= shelf["altura"] and shelf["ocupado"] + w <= largura_bin:
                    sobra = largura_bin - (shelf["ocupado"] + w)  # sobra horizontal
                    if melhor_sobra is None or sobra < melhor_sobra:
                        melhor_bin = b
                        melhor_shelf = shelf
                        melhor_sobra = sobra

            # 2) tentar abrir nova shelf
            used_height = sum(s["altura"] for s in b["shelves"])
            if used_height + h <= altura_bin:
                sobra = altura_bin - (used_height + h)  # sobra vertical no bin
                if melhor_sobra is None or sobra < melhor_sobra:
                    melhor_bin = b
                    melhor_shelf = None
                    melhor_sobra = sobra

        # Se achou lugar em algum bin existente
        if melhor_bin is not None:
            if melhor_shelf is not None:  # coloca na shelf existente
                x = melhor_shelf["ocupado"]
                y = melhor_shelf["y"]
                melhor_bin["itens"].append({"dimensoes": (w, h), "posicao": (x, y)})
                melhor_shelf["ocupado"] += w
            else:  # abre nova shelf
                used_height = sum(s["altura"] for s in melhor_bin["shelves"])
                y_new = used_height
                melhor_bin["shelves"].append({"y": y_new, "altura": h, "ocupado": w})
                melhor_bin["itens"].append({"dimensoes": (w, h), "posicao": (0, y_new)})
        else:
            # Se não couber em nenhum bin, cria um novo
            new_bin = {
                "itens": [{"dimensoes": (w, h), "posicao": (0, 0)}],
                "shelves": [{"y": 0, "altura": h, "ocupado": w}]
            }
            bins.append(new_bin)

    return bins
