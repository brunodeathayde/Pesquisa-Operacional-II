import matplotlib.pyplot as plt
from next_fit import next_fit  
from first_fit import first_fit  
from first_fit_decreasing import first_fit_decreasing
from best_fit import best_fit  
from best_fit_decreasing import best_fit_decreasing

itens = l = [1.5, 2.8, 2.4, 3.3, 3.5, 1.25, 0.85, 2.45, 4.1, 3.6, 2.7, 1.3, 3.8, 1.75, 3.8, 0.75, 1.85, 2.1]
capacidade = 12


resultado = next_fit(itens, capacidade)

print(f"Número de bins usados: {len(resultado)}")
print("Alocação dos itens por bin:")
for i, bin in enumerate(resultado, start=1):
    print(f"Bin {i}: {bin}")

# Visualização gráfica
fig, ax = plt.subplots(figsize=(6, len(resultado) * 0.6))  # largura menor, altura proporcional

for i, bin in enumerate(resultado):
    inicio = 0
    for item in bin:
        ax.barh(i, item, left=inicio, height=0.5, edgecolor='black')
        ax.text(inicio + item / 2, i, str(item), va='center', ha='center', color='white', fontsize=8)
        inicio += item

# Ajustes visuais
ax.set_yticks(range(len(resultado)))
ax.set_yticklabels([f"Bin {i+1}" for i in range(len(resultado))])
ax.set_xlabel("Capacidade ocupada")
ax.set_title("Alocação de Itens nos Bins (FFD)")
ax.set_xlim(0, capacidade)
plt.tight_layout()
plt.show()

