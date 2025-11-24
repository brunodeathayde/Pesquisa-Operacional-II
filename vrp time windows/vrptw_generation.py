from random import randint

n = 5    # número de clientes
K = 20   # capacidade máxima
m = 1    # número de instâncias a gerar

for k in range(m):
    file_name = f"VRPTW-{k+1}.txt"
    
    with open(file_name, "w") as file:
        for i in range(n):
            r1 = randint(-10*n, 10*n)      # coordenada x
            r2 = randint(-10*n, 10*n)      # coordenada y
            r3 = randint(1, K//2)          # demanda (inteiro)
            
            # janela de tempo (início e fim)
            start_tw = randint(0, 50)      # início da janela
            end_tw = start_tw + randint(10, 30)  # fim da janela
            
            file.write(f"{r1}  {r2}  {r3}  {start_tw}  {end_tw}\n")
