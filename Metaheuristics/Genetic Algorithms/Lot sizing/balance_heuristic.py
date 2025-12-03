def balance_heuristic(d, p, f, h):
    """
    Heurística de Balanço por Partes (BP) corrigida.
    Produz em um período para cobrir demandas futuras se o custo de estocagem for menor que o custo fixo de produção adicional.

    Parâmetros:
    - d: demanda por período
    - p: custo unitário de produção por período
    - f: custo fixo de produção por período
    - h: custo unitário de estocagem por período

    Retorna:
    - x: produção por período
    - s: estoque ao final de cada período
    - y: indicador binário de produção
    - custo_total: custo total da solução
    """
    n = len(d)
    x = [0] * n
    s = [0] * n
    y = [0] * n

    t = 1
    while t < n:
        total_demand = d[t]
        total_holding = 0
        t_final = t

        for j in range(t + 1, n):
            total_holding += h[j] * sum(d[k] for k in range(t, j))
            if total_holding < f[j]:
                total_demand += d[j]
                t_final = j
            else:
                break

        x[t] = total_demand
        y[t] = 1

        # Atualiza estoques
        estoque = total_demand
        for j in range(t, t_final + 1):
            estoque -= d[j]
            s[j] = max(estoque, 0)

        t = t_final + 1

    custo_total = sum(p[t] * x[t] + f[t] * y[t] + h[t] * s[t] for t in range(1, n))
    return x, s, y, custo_total
