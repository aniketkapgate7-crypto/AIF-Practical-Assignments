def triangular_mf(x: float, a: float, b: float, c: float) -> float:
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if x < b:
        return round((x - a) / (b - a), 3)
    return round((c - x) / (c - b), 3)


def assess_employee(productivity: float, teamwork: float, punctuality: float):
    # Inputs on 0-100 scale
    prod_high = triangular_mf(productivity, 65.0, 85.0, 100.0)
    team_high = triangular_mf(teamwork, 60.0, 85.0, 100.0)
    punc_high = triangular_mf(punctuality, 70.0, 90.0, 100.0)

    overall_high_score = round((0.45 * prod_high + 0.30 * team_high + 0.25 * punc_high), 3)
    return {
        "productivity_high_mu": prod_high,
        "teamwork_high_mu": team_high,
        "punctuality_high_mu": punc_high,
        "overall_high_performer_mu": overall_high_score,
    }


if __name__ == "__main__":
    print("Employee Assessment:", assess_employee(productivity=88.0, teamwork=82.0, punctuality=92.0))