def max_min_composition(R: list[list[float]], S: list[list[float]]) -> list[list[float]]:
    # R is m x k, S is k x n -> result is m x n
    m = len(R)
    k = len(S)
    n = len(S[0])
    result = [[0.0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            result[i][j] = round(max(min(R[i][p], S[p][j]) for p in range(k)), 3)
    return result


if __name__ == "__main__":
    # Rows: Distance [Near, Medium, Far]; Cols: Speed [Slow, Moderate, Fast]
    R_dist_speed = [
        [0.8, 0.5, 0.2],
        [0.4, 0.7, 0.4],
        [0.1, 0.3, 0.9],
    ]
    # Rows: Speed [Slow, Moderate, Fast]; Cols: Braking [Light, Medium, Hard]
    S_speed_brake = [
        [0.9, 0.2, 0.0],
        [0.3, 0.8, 0.4],
        [0.0, 0.3, 0.95],
    ]
    T_dist_brake = max_min_composition(R_dist_speed, S_speed_brake)
    print("Distance -> Braking Fuzzy Composition Matrix:")
    for row in T_dist_brake:
        print(" ", row)