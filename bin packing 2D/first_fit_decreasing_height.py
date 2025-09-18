def first_fit_decreasing_height(itens, largura_bin, altura_bin, allow_rotation=True):
    itens_rotacionados = []
    for w, h in itens:
        if w <= largura_bin and h <= altura_bin:
            itens_rotacionados.append((w, h))
        elif allow_rotation and h <= largura_bin and w <= altura_bin:
            itens_rotacionados.append((h, w))  # rota o item
        else:
            raise ValueError(f"Item {(w,h)} não cabe no bin ({largura_bin}x{altura_bin}), mesmo com rotação.")
    
    # ordenar por altura decrescente
    itens_ordenados = sorted(itens_rotacionados, key=lambda x: x[1], reverse=True)

    bins = []
    for w, h in itens_ordenados:
        colocado = False
        for b in bins:
            # tenta colocar em shelves existentes
            for shelf in b["shelves"]:
                if h <= shelf["altura"] and shelf["ocupado"] + w <= largura_bin:
                    x = shelf["ocupado"]
                    y = shelf["y"]
                    b["itens"].append({"dimensoes": (w, h), "posicao": (x, y)})
                    shelf["ocupado"] += w
                    colocado = True
                    break
            if colocado:
                break

            # tenta abrir nova shelf
            used_height = sum(s["altura"] for s in b["shelves"])
            if used_height + h <= altura_bin:
                y_new = used_height
                b["shelves"].append({"y": y_new, "altura": h, "ocupado": w})
                b["itens"].append({"dimensoes": (w, h), "posicao": (0, y_new)})
                colocado = True
                break

        # se não couber em nenhum bin, cria um novo
        if not colocado:
            new_bin = {
                "itens": [{"dimensoes": (w, h), "posicao": (0, 0)}],
                "shelves": [{"y": 0, "altura": h, "ocupado": w}]
            }
            bins.append(new_bin)

    return bins
