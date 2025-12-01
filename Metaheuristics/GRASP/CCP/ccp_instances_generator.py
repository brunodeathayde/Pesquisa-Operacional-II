
from random import randint

n = 50   # número de clientes
m = 1    # número de instâncias a gerar
p = 10   # número de clusters

# Folga percentual sobre a soma das demandas (ajuste conforme necessário)
SLACK_PCT = 0.20  # 20% de folga para reduzir inviabilidades na construção

for k in range(m):
    str_file_name = "ccp-"
    file_name = str_file_name + str(k+1) + ".txt"

    # === Gerar clientes ===
    demandas = []
    clientes = []
    for i in range(n):
        x = randint(-10*n, 10*n)
        y = randint(-10*n, 10*n)
        demanda = randint(1, 20)
        demandas.append(demanda)
        clientes.append((x, y, demanda))

    soma_demandas = sum(demandas)
    max_demanda = max(demandas)

    # === Gerar clusters com base em max_demanda ===
    capacidades = []
    clusters = []
    for j in range(p):
        x = randint(-10*n, 10*n)
        y = randint(-10*n, 10*n)
        # Base: pelo menos max_demanda por cluster
        base_min = max_demanda
        base_extra = randint(0, max(10, max_demanda))  # alguma variação
        capacidade = base_min + base_extra
        capacidades.append(capacidade)
        clusters.append([x, y, capacidade])

    # Atualiza agregados
    soma_capacidades = sum(capacidades)
    max_capacidade = max(capacidades)

    # === Garantir soma das capacidades com folga ===
    target_sum = int(soma_demandas * (1 + SLACK_PCT))
    if soma_capacidades < target_sum:
        deficit = target_sum - soma_capacidades
        # distribui de forma uniforme o déficit
        incr = deficit // p
        rem = deficit % p
        for j in range(p):
            clusters[j][2] += incr + (1 if j < rem else 0)
        capacidades = [c[2] for c in clusters]
        soma_capacidades = sum(capacidades)
        max_capacidade = max(capacidades)

    # === Verificação cumulativa (prefixos) ===
    # Ordena demandas e capacidades em ordem decrescente
    demandas_sorted = sorted(demandas, reverse=True)
    caps_sorted_idx = sorted(range(p), key=lambda j: clusters[j][2], reverse=True)

    # Enquanto houver violação, adiciona capacidade aos maiores clusters
    # Isso garante: para todo k, sum(demandas[:k]) <= sum(capacidades[:k])
    k_ptr = 1
    while k_ptr <= min(n, p):
        sum_dem_k = sum(demandas_sorted[:k_ptr])
        sum_cap_k = sum(clusters[j][2] for j in caps_sorted_idx[:k_ptr])
        if sum_cap_k < sum_dem_k:
            # déficit para o prefixo k
            deficit_k = sum_dem_k - sum_cap_k
            # distribui o déficit entre os k maiores clusters
            add_each = max(1, deficit_k // k_ptr)
            rem = deficit_k % k_ptr
            for idx_pos in range(k_ptr):
                j = caps_sorted_idx[idx_pos]
                clusters[j][2] += add_each + (1 if idx_pos < rem else 0)
            # reordena índices de capacidades após incremento
            caps_sorted_idx = sorted(range(p), key=lambda j: clusters[j][2], reverse=True)
            # não avança k_ptr até ficar viável para este k
            continue
        k_ptr += 1

    # Atualiza métricas finais
    capacidades = [c[2] for c in clusters]
    soma_capacidades = sum(capacidades)
    max_capacidade = max(capacidades)

    # === Salvar no arquivo ===
    with open(file_name, "w") as file:
        # primeira linha: número de clusters e número de clientes
        file.write("%i %i\n" % (p, n))

        # clientes
        file.write("# Clientes: x y demanda\n")
        for (x, y, d) in clientes:
            file.write("%i %i %i\n" % (x, y, d))

        # clusters
        file.write("# Clusters: x y capacidade\n")
        for (x, y, cap) in clusters:
            file.write("%i %i %i\n" % (x, y, cap))

    print(f"Instância {file_name} gerada com soma_demandas={soma_demandas}, soma_capacidades={soma_capacidades}, max_demanda={max_demanda}, max_capacidade={max_capacidade}")
