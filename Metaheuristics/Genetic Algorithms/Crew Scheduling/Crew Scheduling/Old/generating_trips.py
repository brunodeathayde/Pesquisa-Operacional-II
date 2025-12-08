import os
import random

def gerar_timetable(arquivo="timetable.txt", num_viagens=20, modo="w"):
    """
    arquivo: caminho do arquivo (pode ser absoluto)
    num_viagens: quantidade desejada de viagens (None = até 23:00)
    modo: 'w' sobrescreve, 'a' acrescenta
    """
    # Intervalo do dia
    inicio_dia = 5 * 60   # 05:00
    fim_dia = 23 * 60     # 23:00

    # Períodos de pico: headway menor
    def headway(minuto):
        if 6*60 <= minuto < 9*60:      # manhã
            return random.randint(7, 12)
        if 12*60 <= minuto < 14*60:    # almoço
            return random.randint(10, 15)
        if 17*60 <= minuto < 19*60:    # início da noite
            return random.randint(7, 12)
        return random.randint(20, 30)  # fora de pico

    # Duração da viagem
    def duracao():
        return random.randint(80, 110)

    viagens = []
    trip_id = 1
    t = inicio_dia

    while t < fim_dia:
        if num_viagens is not None and trip_id > num_viagens:
            break

        d = duracao()
        fim = t + d
        if fim > fim_dia:
            break

        h_ini, m_ini = divmod(t, 60)
        h_fim, m_fim = divmod(fim, 60)
        viagens.append([trip_id, h_ini, m_ini, h_fim, m_fim])

        t += headway(t)
        trip_id += 1

    # Salvar arquivo com tratamento de erros
    try:
        # Garante que diretório existe
        dir_arquivo = os.path.dirname(os.path.abspath(arquivo))
        if dir_arquivo and not os.path.exists(dir_arquivo):
            os.makedirs(dir_arquivo, exist_ok=True)

        with open(arquivo, modo, encoding="utf-8") as f:
            for v in viagens:
                f.write(f"{v[0]},{v[1]:02d},{v[2]:02d},{v[3]:02d},{v[4]:02d}\n")

        print(f"Geradas {len(viagens)} viagens entre 05:00 e 23:00 e salvas em {os.path.abspath(arquivo)}")
    except Exception as e:
        print(f"Falha ao salvar em '{arquivo}': {e}")

    return viagens

# Execute APENAS UMA VEZ
viagens = gerar_timetable("timetable.txt", num_viagens=15, modo="w")
