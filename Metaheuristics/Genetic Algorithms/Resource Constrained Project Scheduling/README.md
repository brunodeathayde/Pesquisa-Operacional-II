
# RCPSP Instance
n_activities = 10
n_resources = 2
resource_capacities = [4, 2]

# Atividades (id duration r1 r2 ... predecessors)
1 0 0 0 -
2 1 4 1 1
3 1 4 1 2,1
4 3 4 2 1
5 4 2 2 3
6 4 4 1 5,4
7 1 0 0 5,1
8 3 2 1 1,4,3
9 5 3 2 3,2,7
10 0 0 0 9

