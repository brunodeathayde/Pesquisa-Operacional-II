from random import randint

n = 20    # número de clientes
K = 20   # capacidade máxima do veículo
m = 1    # número de instâncias a gerar

for k in range(m):
    file_name = f"VRPPD-{k+1}.txt"
    
    with open(file_name, "w") as file:
        for i in range(n):
            x = randint(-10 * n, 10 * n)       # coordenada x
            y = randint(-10 * n, 10 * n)       # coordenada y
            delivery = randint(0, K // 2)      # demanda de entrega
            pickup = randint(0, K // 2)        # demanda de coleta
            
            file.write(f"{x} {y} {delivery} {pickup}\n")

