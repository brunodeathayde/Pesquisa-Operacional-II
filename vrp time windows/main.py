from vrptw_reading import vrptw_reading
from route_cost import route_cost
from route_cost_open import route_cost_open

P = vrptw_reading("VRPTW-1.txt")

rota = [5,4,3,2,1]
capacidade = 20

dist, viavel, todas_rotas = route_cost(rota, P, capacidade, tempo_servico=0)

print(f"Rota viável: {viavel}")
print(f"Rotas dos veículos: {todas_rotas}")   
print(f"Distância total: {dist:.2f}")
print(f"Rota viável: {viavel}")


rota = [5,4,3,2,1]
capacidade = 20
deposito = (3,5)
destino_final = (-10,-12)
custo, viavel, todas_rotas =   route_cost_open(rota, P, capacidade, deposito, destino_final, tempo_servico=0)

print(f"Rota viável: {viavel}")
print(f"Rotas dos veículos: {todas_rotas}")   
print(f"Distância total: {custo:.2f}")
print(f"Rota viável: {viavel}")

    

