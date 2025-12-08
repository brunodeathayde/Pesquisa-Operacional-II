from itertools import combinations
import numpy as np

# --- Leitura do arquivo timetable.txt ---
# Formato por linha: id,hora_inicio,min_inicio,hora_fim,min_fim
def ler_viagens(arquivo="timetable.txt"):
    viagens = []
    with open(arquivo, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 5:
                continue
            id_, h_ini, m_ini, h_fim, m_fim = map(int, parts)
            viagens.append([id_, h_ini, m_ini, h_fim, m_fim])
    # ordena por id para consistência da matriz
    viagens.sort(key=lambda v: v[0])
    return viagens

# --- Utilidades ---
def to_minutes(h, m):
    return h * 60 + m

def inicio_fim_servico(combo):
    inicio = min(to_minutes(v[1], v[2]) for v in combo)
    fim = max(to_minutes(v[3], v[4]) for v in combo)
    return inicio, fim

# --- Parâmetros ---
janela_ini = to_minutes(6, 20)  # 06h20
janela_fim = to_minutes(9, 20)  # 09h20
limite_duracao = 440            # 7h20 = 440 min

# --- Execução ---
viagens = ler_viagens("timetable.txt")
n_viagens = len(viagens)
print(f"Número de viagens lidas: {n_viagens}")

# Gera todos os serviços dentro da janela
servicos = []
for r in range(1, n_viagens + 1):
    for combo in combinations(viagens, r):
        inicio, fim = inicio_fim_servico(combo)
        # Serviço totalmente dentro da janela [06:20, 09:20]
        if inicio >= janela_ini and fim <= janela_fim:
            duracao_total = fim - inicio
            custo = max(0, duracao_total - limite_duracao)
            servicos.append({
                "viagens": [v[0] for v in combo],
                "duracao_total": duracao_total,
                "custo": custo
            })

print(f"Número total de serviços gerados na janela: {len(servicos)}")

# Matriz binária: linhas = viagens (ordenadas por id), colunas = serviços
ids = [v[0] for v in viagens]
id_to_row = {id_: idx for idx, id_ in enumerate(ids)}

matriz = np.zeros((n_viagens, len(servicos)), dtype=int)
for j, s in enumerate(servicos):
    for id_v in s["viagens"]:
        i = id_to_row[id_v]
        matriz[i, j] = 1

# --- Salvar resultados ---
tempos = np.array([s["duracao_total"] for s in servicos], dtype=int)

# Empilha primeira linha (tempos) + matriz binária
saida = np.vstack([tempos.reshape(1, -1), matriz])

np.savetxt("matrix_services.csv", saida, fmt="%d", delimiter=",")

with open("services_list.txt", "w") as f:
    for s in servicos:
        f.write(f"{';'.join(map(str, s['viagens']))};{s['duracao_total']};{s['custo']}\n")

print("\nArquivos salvos: matrix_services.csv e services_list.txt")
