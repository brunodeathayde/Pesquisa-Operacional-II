import matplotlib.pyplot as plt

def plotting_route(n, s, P):
    # s: permutação de índices de 0..n-1
    # P: lista/array de coordenadas [(x,y), ...] de tamanho n
    assert len(s) == n, "Permutação s deve ter tamanho n"
    assert set(s) == set(range(n)), "s deve ser uma permutação de 0..n-1"

    # plota os pontos
    for i in range(n):
        plt.scatter(P[i][0], P[i][1], color='red', s=30)

    # plota as arestas na ordem de s
    for i in range(n - 1):
        x = [P[s[i]][0], P[s[i+1]][0]]
        y = [P[s[i]][1], P[s[i+1]][1]]
        plt.plot(x, y, color='blue')

    # fecha o ciclo ligando o último ao primeiro
    x_close = [P[s[-1]][0], P[s[0]][0]]
    y_close = [P[s[-1]][1], P[s[0]][1]]
    plt.plot(x_close, y_close, color='blue')

    plt.title("Rota")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')   # mantém a escala dos eixos
    plt.grid(True)
    plt.show()

