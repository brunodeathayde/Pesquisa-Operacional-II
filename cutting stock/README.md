Corte de Estoque com Python MIP

Este repositório apresenta a modelagem e resolução do clássico Problema de Corte de Estoque, utilizando o pacote Python MIP para otimização linear inteira.

Descrição do Problema

O problema de corte de estoque consiste em determinar a melhor forma de cortar rolos de material padrão (com largura fixa) para atender à demanda de diferentes itens, minimizando o número total de rolos utilizados.
Objetivo:

    Minimizar o número de rolos padrão utilizados.

    Atender à demanda de cada item com os padrões de corte disponíveis.

Restrições:

    Cada padrão de corte define como um rolo pode ser dividido.

    A soma dos cortes deve atender ou exceder a demanda de cada item.

Uma instância para o problema

    Largura do rolo padrão: L = 12.0

    Comprimentos dos itens: l = [3.0, 4.5, 4.2, 5.0]

    Demandas dos itens: d = [10, 4, 5, 3]

    Custos unitários por padrão: c = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    Padrões de corte: matriz a com combinações viáveis de cortes
