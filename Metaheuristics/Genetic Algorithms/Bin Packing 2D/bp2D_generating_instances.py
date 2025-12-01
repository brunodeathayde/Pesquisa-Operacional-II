
from random import randint, seed

# Parâmetros principais
m = 1           # número de instâncias a gerar
n_itens = 14    # quantidade de itens
largura_bin = 10
altura_bin = 6

# Controle de dificuldade: alvo de densidade de área (0.6 a 1.2 é razoável)
densidade_alvo = 0.85  # área total dos itens / área do bin

# Geração reprodutível (opcional)
seed(42)

for k in range(m):
    str_file_name = "bin2d-"
    file_name = str_file_name + str(k+1) + ".txt"

    itens = []

    # Área alvo total dos itens
    area_bin = largura_bin * altura_bin
    area_alvo = int(area_bin * densidade_alvo)

    # Limites dos itens (cada item deve caber no bin individualmente)
    w_max_item = largura_bin
    h_max_item = altura_bin
    w_min_item = max(1, largura_bin // 10)  # evita itens degenerados
    h_min_item = max(1, altura_bin // 10)

    # Gera itens até atingir n_itens, ajustando para aproximar a área alvo
    # Estratégia: primeiro distribui itens com tamanhos variados, depois ajusta se necessário
    area_acumulada = 0
    for i in range(n_itens):
        # Heurística simples para variar tamanhos e aproximar a área alvo
        # Em fases iniciais, itens maiores; depois menores, para refinar a área total
        peso_fase = 1.0 - (i / max(1, n_itens - 1)) * 0.5  # decresce de 1.0 para 0.5
        w = randint(w_min_item, max(w_min_item, int(w_max_item * peso_fase)))
        h = randint(h_min_item, max(h_min_item, int(h_max_item * peso_fase)))

        # Garante que o item cabe no bin
        w = min(w, largura_bin)
        h = min(h, altura_bin)

        itens.append((w, h))
        area_acumulada += w * h

    # Ajuste fino: se área ficou muito longe do alvo, ajusta itens pequenos
    # Aumenta área se necessário (sem ultrapassar dimensões do bin por item)
    i = 0
    while area_acumulada < area_alvo and i < n_itens:
        w, h = itens[i]
        if w < largura_bin or h < altura_bin:
            novo_w = min(largura_bin, w + randint(0, max(1, largura_bin // 5)))
            novo_h = min(altura_bin, h + randint(0, max(1, altura_bin // 5)))
            area_acumulada += novo_w * novo_h - w * h
            itens[i] = (novo_w, novo_h)
        i += 1

    # Se exceder demais o alvo, reduz alguns itens
    i = 0
    while area_acumulada > int(area_alvo * 1.15) and i < n_itens:
        w, h = itens[i]
        if w > w_min_item or h > h_min_item:
            novo_w = max(w_min_item, w - randint(0, max(1, largura_bin // 5)))
            novo_h = max(h_min_item, h - randint(0, max(1, altura_bin // 5)))
            area_acumulada += novo_w * novo_h - w * h
            itens[i] = (novo_w, novo_h)
        i += 1

    # Salva no formato solicitado
    with open(file_name, "w") as f:
        f.write(f"itens = {itens}\n")
        f.write(f"largura_bin = {largura_bin}\n")
        f.write(f"altura_bin = {altura_bin}\n")

    print(f"Instância {file_name} gerada: {len(itens)} itens, área_itens={area_acumulada}, área_bin={area_bin}, densidade={area_acumulada/area_bin:.2f}")
