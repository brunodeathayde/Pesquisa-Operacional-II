# PSO Scheduling Toolkit

Este repositório contém uma implementação de **Particle Swarm Optimization (PSO)** aplicada a problemas de sequenciamento, utilizando a biblioteca [scheptk](https://github.com/framinan/scheptk).

## 📂 Estrutura do Repositório

- `main.py` → Script principal para executar o PSO.
- `pso_operators.py` → Funções auxiliares para geração de população, atualização de velocidades/posições e aplicação de elitismo.
- `instance.txt` → Instância de problema de máquinas paralelas idênticas (tempos de processamento, jobs e máquinas).
- `Makespan.png` → Gráfico da Gantt.

---

## ⚙️ Funções em `pso_operators.py`

| Função                  | Descrição                                                                 |
|--------------------------|---------------------------------------------------------------------------|
| `gen_velocities`         | Gera velocidades iniciais contínuas entre limites definidos.              |
| `gen_population`         | Cria população inicial contínua dentro de um intervalo.                   |
| `to_permutations`        | Converte população contínua em permutações de jobs.                       |
| `position_to_permutation`| Converte uma única solução contínua em permutação.                        |
| `fitness_population`     | Calcula o makespan para todos os indivíduos da população.                 |
| `update_best`            | Atualiza os melhores locais (`p_best`) e o melhor global (`g_best`).      |
| `update_velocities`      | Atualiza as velocidades de acordo com PSO (componentes cognitivo e social).|
| `update_positions`       | Atualiza as posições e aplica limites.                                    |
| `apply_elitism`          | Garante elitismo, mantendo sempre a melhor solução na população.          |

---
