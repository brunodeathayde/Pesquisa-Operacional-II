import random
import numpy as np

# Função job_exchange:
# Gera uma vizinhança trocando dois elementos de posição na sequência (pi).
def job_exchange(pi):
    # escolhe duas posições distintas
    p1 = random.sample(range(len(pi)), 2)
    # troca os elementos
    pi[p1[0]], pi[p1[1]] = pi[p1[1]], pi[p1[0]]

    return pi


# Função job_insertion:
# Move um elemento escolhido aleatoriamente para o início da sequência.
def job_insertion(pi):
    n = len(pi)
    k = random.randint(1, n-1)  
    
    # inserir o elemento pi[k] na primeira posição
    pi.insert(0, pi[k])

    # remover o elemento original (que agora está deslocado para k+1)
    del pi[k+1]

    return pi


# Função job_series_exchange:
# Divide a sequência em duas partes e troca a ordem delas, mantendo a ordem interna.
def job_series_exchange(pi):
    n = len(pi)
    k = random.randint(1, n-2)  

    # pi_1 recebe os primeiros k elementos
    pi_1 = pi[:k+1]   

    # pi_2 = elementos que não estão em pi_1 (ordem preservada)
    pi_2 = [x for x in pi if x not in pi_1]

    # concatena: primeiro a parte "restante", depois a inicial
    pi_new = pi_2 + pi_1

    return pi_new


# Função job_series_move_one:
# Seleciona um bloco de 4 elementos consecutivos e move-o para o início da sequência.
def job_series_move_one(pi):
    n = len(pi)
    k = random.randint(1, n-5)

    # copiar 4 elementos começando de pi[k+1 : k+5]
    pi_1 = pi[k+1 : k+5]

    # elementos restantes, preservando ordem
    pi_2 = [x for x in pi if x not in pi_1]

    # concatena como vcat(pi_1, pi_2)
    pi_new = pi_1 + pi_2

    return pi_new

# Função job_series_move_two:
# Seleciona um bloco de 4 elementos consecutivos e move-o para o final da sequência.
def job_series_move_two(pi):
    n = len(pi)

    # Em Python (0-based): 1 .. n-5
    k = random.randint(1, n-5)

    # pi[i+k] para i=1..4 -> elementos pi[k+1] até pi[k+4]
    pi_1 = pi[k+1 : k+5]

    # elementos restantes na ordem original
    pi_2 = [x for x in pi if x not in pi_1]

    # concatena: primeiro os elementos restantes, depois o bloco selecionado
    pi_new = pi_2 + pi_1

    return pi_new
