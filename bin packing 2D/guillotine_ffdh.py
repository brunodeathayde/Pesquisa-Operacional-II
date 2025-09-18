def guillotine_ffdh(itens, largura_bin, altura_bin, allow_rotation=True):
    # normaliza itens (considerando rotação)
    itens_rotacionados = []
    for w, h in itens:
        if w <= largura_bin and h <= altura_bin:
            itens_rotacionados.append((w, h))
        elif allow_rotation and h <= largura_bin and w <= altura_bin:
            itens_rotacionados.append((h, w))  # rota
        else:
            raise ValueError(f"Item {(w,h)} não cabe no bin ({largura_bin}x{altura_bin}), mesmo com rotação.")

    # ordenar por altura decrescente (heurística FFDH)
    itens_ordenados = sorted(itens_rotacionados, key=lambda x: x[1], reverse=True)

    bins = []

    for w, h in itens_ordenados:
        colocado = False
        for b in bins:
            # tenta colocar em algum espaço livre
            for espaco in b["livres"]:
                ew, eh = espaco["dimensoes"]
                ex, ey = espaco["posicao"]
                if w <= ew and h <= eh:
                    # coloca item nesse espaço
                    b["itens"].append({"dimensoes": (w, h), "posicao": (ex, ey)})

                    # remove espaço usado e cria dois cortes (guillotine)
                    b["livres"].remove(espaco)

                    # corte vertical (à direita do item)
                    if ew - w > 0:
                        b["livres"].append({
                            "dimensoes": (ew - w, h),
                            "posicao": (ex + w, ey)
                        })
                    # corte horizontal (acima do item)
                    if eh - h > 0:
                        b["livres"].append({
                            "dimensoes": (ew, eh - h),
                            "posicao": (ex, ey + h)
                        })

                    colocado = True
                    break
            if colocado:
                break

        # se não couber em nenhum bin, cria um novo
        if not colocado:
            new_bin = {
                "itens": [{"dimensoes": (w, h), "posicao": (0, 0)}],
                "livres": []
            }

            # cortes iniciais do bin
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
