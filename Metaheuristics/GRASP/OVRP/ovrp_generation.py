from random import randint 

# Parâmetros
n = 25    # número de clientes
K = 20   # capacidade máxima
m = 1    # número de instâncias a gerar

for k in range(m):
    file_name = f"OVRP-{k+1}.txt"
    
    with open(file_name, "w") as file:
        # (i) depósito (origem dos veículos)
        depot_x = randint(-10*n, 10*n)
        depot_y = randint(-10*n, 10*n)
        file.write(f"{depot_x}  {depot_y}  0\n")  # demanda = 0
        
        # (ii) ponto de entrega final
        delivery_x = randint(-10*n, 10*n)
        delivery_y = randint(-10*n, 10*n)
        file.write(f"{delivery_x}  {delivery_y}  0\n")  # demanda = 0
        
        # (iii) clientes
        for i in range(n):
            r1 = randint(-10*n, 10*n)      # coordenada x
            r2 = randint(-10*n, 10*n)      # coordenada y
            r3 = randint(1, K//2)          # demanda (inteiro)
            
            file.write(f"{r1}  {r2}  {r3}\n")
