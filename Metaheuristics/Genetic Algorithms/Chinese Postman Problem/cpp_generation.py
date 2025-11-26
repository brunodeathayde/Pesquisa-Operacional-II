import random

n = 10   # número de nós
m = 1   # número de instâncias

for k in range(m):
    file_name = f"CPP-{k+1}.txt"
    with open(file_name, "w") as f:
        # Primeira linha como comentário
        f.write("# tipo,u,v,peso\n")

        nodes = list(range(n))  # nós apenas como números

        # Arcos direcionados
        for _ in range(random.randint(n, 2*n)):
            u, v = random.sample(nodes, 2)
            w = random.randint(1, 20)
            f.write(f"D,{u},{v},{w}\n")

        # Arestas não direcionadas
        for _ in range(random.randint(n, 2*n)):
            u, v = random.sample(nodes, 2)
            w = random.randint(1, 20)
            f.write(f"U,{u},{v},{w}\n")
