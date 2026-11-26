import random


def normalize_weights(weights: list[float]) -> list[float]:
    total = sum(weights)
    if total <= 0:
        return [1.0 / len(weights)] * len(weights)
    return [w / total for w in weights]


def portfolio_fitness(weights: list[float], returns: list[float], risks: list[float], risk_aversion: float = 1.5) -> float:
    w = normalize_weights(weights)
    exp_return = sum(wi * ri for wi, ri in zip(w, returns))
    # Simplified volatility proxy
    risk = (sum((wi * si) ** 2 for wi, si in zip(w, risks))) ** 0.5
    return exp_return - risk_aversion * risk


def run_portfolio_ga(returns: list[float], risks: list[float], generations: int = 80, pop_size: int = 40, seed: int = 21):
    rng = random.Random(seed)
    n = len(returns)
    pop = [[rng.random() for _ in range(n)] for _ in range(pop_size)]

    for _ in range(generations):
        pop.sort(key=lambda c: portfolio_fitness(c, returns, risks), reverse=True)
        elites = pop[:6]
        children = []
        while len(children) < pop_size - len(elites):
            p1, p2 = rng.sample(elites, 2)
            cut = rng.randint(1, n - 1)
            child = p1[:cut] + p2[cut:]
            child = [max(0.0, g + rng.gauss(0, 0.08)) for g in child]
            children.append(child)
        pop = elites + children

    best = normalize_weights(max(pop, key=lambda c: portfolio_fitness(c, returns, risks)))
    exp_ret = sum(wi * ri for wi, ri in zip(best, returns))
    exp_risk = (sum((wi * si) ** 2 for wi, si in zip(best, risks))) ** 0.5
    return [round(x, 4) for x in best], round(exp_ret * 100, 2), round(exp_risk * 100, 2)


if __name__ == "__main__":
    asset_returns = [0.14, 0.11, 0.06, 0.18]
    asset_risks = [0.16, 0.12, 0.04, 0.24]
    alloc, ret_pct, risk_pct = run_portfolio_ga(asset_returns, asset_risks)
    print(f"Weights: {alloc} | Expected Return: {ret_pct}% | Risk Proxy: {risk_pct}%")