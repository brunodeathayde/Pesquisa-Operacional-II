import networkx as nx

def reading_cpp(nome_arquivo):
    # Criar grafo dirigido para suportar arcos direcionados
    G = nx.DiGraph()

    with open(nome_arquivo, "r") as f:
        linhas = f.readlines()

        # Pular a primeira linha (comentário)
        for linha in linhas[1:]:
            linha = linha.strip()
            if not linha:
                continue

            tipo, u, v, peso = linha.split(",")
            u, v, peso = int(u), int(v), int(peso)

            if tipo == "D":
                # Arco direcionado
                G.add_edge(u, v, weight=peso)
            elif tipo == "U":
                # Aresta não direcionada -> adicionar duas direções
                G.add_edge(u, v, weight=peso)
                G.add_edge(v, u, weight=peso)

    return G

