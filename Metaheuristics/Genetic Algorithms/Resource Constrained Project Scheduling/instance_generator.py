from random import randint, sample

def gerar_instancias_rcpsp(num_instancias=3, n=10, m=2):
    """
    Gera instâncias RCPSP em arquivos .txt
    :param num_instancias: número de instâncias a serem geradas
    :param n: número de atividades (inclui dummy start e end)
    :param m: número de recursos
    """
    for k in range(num_instancias):
        file_name = f"RCPSP-{k+1}.txt"
        with open(file_name, "w") as file:
            # Cabeçalho
            file.write("# RCPSP Instance\n")
            file.write(f"n_activities = {n}\n")
            file.write(f"n_resources = {m}\n")

            # Capacidades dos recursos
            resource_capacities = [randint(2, 5) for _ in range(m)]
            file.write("resource_capacities = " + str(resource_capacities) + "\n\n")

            file.write("# Atividades (id duration r1 r2 ... predecessors)\n")

            # Atividade inicial dummy
            file.write("1 0 " + " ".join(["0"]*m) + " -\n")

            # Atividades intermediárias
            for i in range(2, n):
                duration = randint(1, 5)
                resources = [randint(0, resource_capacities[j]) for j in range(m)]
                preds = sample(range(1, i), randint(1, min(3, i-1)))
                preds_str = ",".join(map(str, preds))
                file.write(f"{i} {duration} " + " ".join(map(str, resources)) + f" {preds_str}\n")

            # Atividade final dummy
            file.write(f"{n} 0 " + " ".join(["0"]*m) + f" {n-1}\n")

        print(f"Instância gerada: {file_name}")


# Exemplo de uso:
gerar_instancias_rcpsp(num_instancias=5, n=12, m=3)
