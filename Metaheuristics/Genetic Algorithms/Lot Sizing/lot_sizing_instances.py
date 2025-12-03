from random import randint, seed

def generate_lot_sizing_instances(N=5, T=12, m=2, max_demand=20, seed_value=None, prefix="LotSizing"):
    if seed_value is not None:
        seed(seed_value)
    
    for k in range(m):
        file_name = f"{prefix}-{k+1}.txt"
        with open(file_name, "w") as file:
            # N e T
            file.write(f"{N}\n")
            file.write(f"{T}\n\n")
            
            # Demanda
            file.write("# demanda\n")
            for i in range(N):
                row = [str(randint(0, max_demand)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo de produção
            file.write("# custo de produção\n")
            for i in range(N):
                row = [str(randint(1, 20)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo de estoque
            file.write("# custo de estoque\n")
            for i in range(N):
                row = [str(randint(1, 10)) for t in range(T)]
                file.write(" ".join(row) + "\n")
            file.write("\n")
            
            # Custo fixo (setup)
            file.write("# custo fixo (setup)\n")
            for i in range(N):
                row = [str(randint(5, 30)) for t in range(T)]
                file.write(" ".join(row) + "\n")
