def lot_for_lot_heuristic(d, p, f):
    """
    Heurística lote-por-lote: produz exatamente o que é demandado em cada período.
    
    Parâmetros:
    - d: lista de demandas por período
    - p: lista de custos unitários de produção por período
    - f: lista de custos fixos de produção por período
    
    Retorna:
    - x: lista de quantidades produzidas
    - s: lista de estoques (sempre zero)
    - y: lista de indicadores binários de produção
    - custo_total: custo total da solução
    """
    n = len(d)
    x = [0] * n
    s = [0] * n
    y = [0] * n

    for t in range(1, n):
        if d[t] > 0:
            x[t] = d[t]
            y[t] = 1
            s[t] = 0

    custo_total = sum(p[t] * x[t] + f[t] * y[t] for t in range(1, n))

    return x, s, y, custo_total
