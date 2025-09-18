def guillotine_bfdh(itens, largura_bin, altura_bin, allow_rotation=True):
    # Normaliza itens (considerando rotação)
    itens_rotacionados = []
    for w, h in itens:
        if w <= largura_bin and h <= altura_bin:
            itens_rotacionados.append((w, h))
        elif allow_rotation and h <= largura_bin and w <= altura_bin:
            itens_rotacionados.append((h, w))  # rotaciona
        else:
            raise ValueError(f"Item {(w,h)} não cabe no bin ({largura_bin}x{altura_bin}), mesmo com rotação.")

    # Ordena por altura decrescente
    itens_ordenados = sorted(itens_rotacionados, key=lambda x: x[1], reverse=True)

    bins = []

    for w, h in itens_ordenados:
        melhor_bin = None
        melhor_espaco = None
        menor_sobra_altura = float('inf')

        # Busca o melhor espaço entre todos os bins
        for b in bins:
            for espaco in b["livres"]:
                ew, eh = espaco["dimensoes"]
                ex, ey = espaco["posicao"]
                if w <= ew and h <= eh:
                    sobra_altura = eh - h
                    if sobra_altura < menor_sobra_altura:
                        menor_sobra_altura = sobra_altura
                        melhor_bin = b
                        melhor_espaco = {
                            "dimensoes": (ew, eh),
                            "posicao": (ex, ey)
                        }

        if melhor_bin and melhor_espaco:
            ew, eh = melhor_espaco["dimensoes"]
            ex, ey = melhor_espaco["posicao"]

            # Coloca item no melhor espaço
            melhor_bin["itens"].append({"dimensoes": (w, h), "posicao": (ex, ey)})
            melhor_bin["livres"].remove(melhor_espaco)

            # Corte vertical (à direita do item)
            if ew - w > 0:
                melhor_bin["livres"].append({
                    "dimensoes": (ew - w, h),
                    "posicao": (ex + w, ey)
                })
            # Corte horizontal (acima do item)
            if eh - h > 0:
                melhor_bin["livres"].append({
                    "dimensoes": (ew, eh - h),
                    "posicao": (ex, ey + h)
                })

        else:
            # Cria novo bin
            new_bin = {
                "itens": [{"dimensoes": (w, h), "posicao": (0, 0)}],
                "livres": []
            }

            # Cortes iniciais do bin
            if largura_bin - w > 0:
                new_bin["livres"].append({
                    "dimensoes": (largura_bin - w, h),
                    "posicao": (w, 0)
                })
            if altura_bin - h > 0:
                new_bin["livres"].append({
                    "dimensoes": (largura_bin, altura_bin - h),
                    "posicao": (0, h)
                })

            bins.append(new_bin)

    return bins
