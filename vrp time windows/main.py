from vrptw_reading import vrptw_reading
from route_cost import route_cost

P = vrptw_reading("VRPTW-1.txt")
    
rota = [5,4,3,2,1]
capacidade = 20

dist, viavel, todas_rotas = route_cost(rota, P, capacidade, tempo_servico=0)

custo, viavel, rotas = route_cost(rota, P, capacidade)
print(f"Custo total: {custo}")
print(f"Rota viável: {viavel}")
print(f"Rotas dos veículos: {rotas}")   
print(f"Distância total: {dist:.2f}")
print(f"Rota viável: {viavel}")

    

