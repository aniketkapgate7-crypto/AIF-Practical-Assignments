import random
import time


# Minimize beam deflection/cost proxy f(x) = (x - 3.7)^2 + 0.5 * sin(5*x) over discrete design steps
def engineering_objective(x: float) -> float:
    return (x - 3.7) ** 2 + 0.5 * (x * 0.3)


def grid_search_benchmark(candidates: list[float]):
    t0 = time.perf_counter()
    best_x = min(candidates, key=engineering_objective)
    ms = (time.perf_counter() - t0) * 1000
    return ms, best_x, round(engineering_objective(best_x), 4), len(candidates)


def ga_benchmark(candidates: list[float], generations: int = 35, pop_size: int = 20, seed: int = 12):
    rng = random.Random(seed)
    t0 = time.perf_counter()
    pop = [rng.choice(candidates) for _ in range(pop_size)]
    evals = len(pop)

    for _ in range(generations):
        pop.sort(key=engineering_objective)
        elites = pop[:4]
        children = []
        while len(children) < pop_size - len(elites):
            parent = rng.choice(elites)
            if rng.random() < 0.3:
                child = rng.choice(candidates)
            else:
                idx = candidates.index(parent)
                step = rng.choice([-2, -1, 1, 2])
                child = candidates[max(0, min(len(candidates) - 1, idx + step))]
            children.append(child)
        pop = elites + children
        evals += len(children)

    best_x = min(pop, key=engineering_objective)
    ms = (time.perf_counter() - t0) * 1000
    return ms, best_x, round(engineering_objective(best_x), 4), evals


if __name__ == "__main__":
    design_grid = [round(i * 0.05, 2) for i in range(0, 201)]  # 201 discrete cross-section sizes
    g_ms, g_x, g_obj, g_evals = grid_search_benchmark(design_grid)
    ga_ms, ga_x, ga_obj, ga_evals = ga_benchmark(design_grid)

    print(f"Exhaustive Grid | Time: {g_ms:.4f} ms | Evals: {g_evals:3d} | Best x: {g_x} | Obj: {g_obj}")
    print(f"Genetic Algo    | Time: {ga_ms:.4f} ms | Evals: {ga_evals:3d} | Best x: {ga_x} | Obj: {ga_obj}")