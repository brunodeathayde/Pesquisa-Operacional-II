import math
def distance_matrix(n, P):
    D = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = P[i][0] - P[j][0]
            dy = P[i][1] - P[j][1]
            D[i][j] = math.sqrt(dx*dx + dy*dy)
    return D
