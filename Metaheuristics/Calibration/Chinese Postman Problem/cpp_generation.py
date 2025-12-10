import random
import os

# Cria a pasta "instances" se não existir
os.makedirs("instances", exist_ok=True)

# Lista de tamanhos de nós que você quer gerar
node_sizes = [10, 20, 30]   # exemplo: instâncias com 10, 20 e 30 nós
instances_per_size = 10     # número de instâncias para cada tamanho

counter = 1  # contador global para nomear os arquivos

for n in node_sizes:
    for k in range(instances_per_size):
        # Nome do arquivo dentro da pasta "instances"
        file_name = os.path.join("instances", f"CPP-{counter}.txt")
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

        counter += 1  # incrementa contador global

print("Instâncias geradas com sucesso na pasta 'instances'!")
