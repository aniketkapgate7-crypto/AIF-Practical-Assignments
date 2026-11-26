import math
import random


def route_distance(route: list[str], coords: dict[str, tuple[float, float]]) -> float:
    dist = 0.0
    for i in range(len(route)):
        x1, y1 = coords[route[i]]
        x2, y2 = coords[route[(i + 1) % len(route)]]
        dist += math.hypot(x2 - x1, y2 - y1)
    return dist


def ordered_crossover(p1: list[str], p2: list[str], rng: random.Random) -> list[str]:
    a, b = sorted(rng.sample(range(len(p1)), 2))
    child = [None] * len(p1)
    child[a:b] = p1[a:b]
    fill = [city for city in p2 if city not in child]
    idx = 0
    for i in range(len(child)):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child  # type: ignore


def optimize_delivery_route(stops: list[str], coords: dict[str, tuple[float, float]], generations: int = 120, seed: int = 9):
    rng = random.Random(seed)
    pop = [rng.sample(stops, len(stops)) for _ in range(30)]

    for _ in range(generations):
        pop.sort(key=lambda r: route_distance(r, coords))
        next_pop = pop[:4]
        while len(next_pop) < len(pop):
            p1, p2 = rng.sample(pop[:12], 2)
            child = ordered_crossover(p1, p2, rng)
            if rng.random() < 0.25:
                i, j = rng.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]
            next_pop.append(child)
        pop = next_pop

    best_route = min(pop, key=lambda r: route_distance(r, coords))
    return best_route, round(route_distance(best_route, coords), 2)


if __name__ == "__main__":
    hub_and_stops = {
        "Hub": (0.0, 0.0),
        "Stop_A": (2.0, 4.0),
        "Stop_B": (5.0, 1.0),
        "Stop_C": (6.0, 5.0),
        "Stop_D": (1.0, 6.0),
        "Stop_E": (4.0, 3.0),
    }
    route, total_dist = optimize_delivery_route(list(hub_and_stops.keys()), hub_and_stops)
    print("Optimized Delivery Loop:", " -> ".join(route + [route[0]]), "| Distance:", total_dist)