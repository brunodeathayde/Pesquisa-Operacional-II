import os
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from reading_cpp import reading_cpp
from full_genetic_algorithm import full_genetic_algorithm

# 1. Selecionar 30% dos arquivos da pasta Instances
all_files = [f for f in os.listdir("Instances") if f.endswith(".txt")]
sample_size = max(1, int(len(all_files) * 0.3))  # garante pelo menos 1
selected_files = random.sample(all_files, sample_size)

# 2. Definir combinações de parâmetros
pop_sizes = [20, 50, 100]
prob_muts = [1, 2]
num_gens = [100, 500, 1000]
param_combinations = [(p, m, g) for p in pop_sizes for m in prob_muts for g in num_gens]

# 3. Estruturas para armazenar resultados
# Guardamos todas as execuções para cada instância e combinação
all_runs = {}  # chave: (instancia, pop, mut, gen) -> lista de fitness
instances_best = {}  # melhor fitness observado por instância

# 4. Loop sobre instâncias e parâmetros (apenas coletando fitness)
for arquivo in selected_files:
    graph = reading_cpp(os.path.join("Instances", arquivo))
    instances_best[arquivo] = float("inf")

    for (pop_size, prob_mut, num_gen) in param_combinations:
        print(f">>> Iniciando testes para instância {arquivo} com parâmetros: "
              f"pop_size={pop_size}, prob_mut={prob_mut}, num_gen={num_gen}")

        key = (arquivo, pop_size, prob_mut, num_gen)
        all_runs[key] = []

        # Rodar 5 vezes e armazenar fitness
        for _ in range(5):
            best_fitness = full_genetic_algorithm(graph, pop_size=pop_size, prob_mut=prob_mut, num_gen=num_gen)
            all_runs[key].append(best_fitness)
            # Atualiza melhor fitness global da instância
            if best_fitness < instances_best[arquivo]:
                instances_best[arquivo] = best_fitness

# 5. Calcular desvios percentuais relativos e salvar em CSV
records = []
for (arquivo, pop_size, prob_mut, num_gen), fitness_values in all_runs.items():
    mean_fitness = float(np.mean(fitness_values))
    best_overall = instances_best[arquivo]

    # Garantia de desvio não-negativo sem mascarar erros:
    # Como best_overall é o melhor observado na instância, não há motivo para mean < best_overall.
    # Se ocorrer (por algum erro ou corrida), ajustamos best_overall para min(mean, best_overall) ANTES da divisão,
    # preservando a definição "melhor solução obtida para a instância" como o menor valor observado até então.
    # Isso evita valores negativos sem usar abs().
    if mean_fitness < best_overall:
        best_overall = mean_fitness

    if best_overall > 0 and np.isfinite(best_overall):
        deviation = ((mean_fitness - best_overall) / best_overall) * 100.0
    else:
        deviation = 0.0  # se best_overall == 0 (improvável), definimos desvio como 0

    records.append({
        "instancia": arquivo,
        "pop_size": pop_size,
        "prob_mut": prob_mut,
        "num_gen": num_gen,
        "mean_fitness": mean_fitness,
        "best_instance_fitness": instances_best[arquivo],
        "deviation_percent": deviation
    })

df = pd.DataFrame(records)
df.to_csv("results_genetic_algorithm.csv", index=False)
print("\nResultados salvos em 'results_genetic_algorithm.csv'")

# 6. Identificar melhor combinação de parâmetros (menor desvio médio)
grouped = df.groupby(["pop_size", "prob_mut", "num_gen"])["deviation_percent"].mean()
best_params = grouped.idxmin()
best_value = grouped.min()

print("\n==============================")
print("Melhor combinação de parâmetros:")
print(f"pop_size={best_params[0]}, prob_mut={best_params[1]}, num_gen={best_params[2]}")
print(f"Desvio percentual relativo médio: {best_value:.2f}%")
print("==============================\n")

# 7. Plotar boxplots
fig, ax = plt.subplots(figsize=(12, 6))
labels = [f"pop={p}, mut={m}, gen={g}" for (p, m, g) in param_combinations]
data = [df[(df["pop_size"]==p) & (df["prob_mut"]==m) & (df["num_gen"]==g)]["deviation_percent"].values
        for (p, m, g) in param_combinations]

ax.boxplot(data, labels=labels, showmeans=True)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Desvio percentual relativo (%)")
plt.title("Comparação de parâmetros do algoritmo genético")

# Destacar melhor combinação
best_idx = param_combinations.index(best_params)
ax.plot([best_idx+1], [best_value], marker="o", markersize=10, color="red", label="Melhor combinação")
ax.legend()

plt.tight_layout()
plt.show()
