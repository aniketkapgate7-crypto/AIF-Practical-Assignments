import random

FEATURES = [
    "OLED_120Hz",
    "Periscope_Zoom",
    "5500mAh_SiC_Battery",
    "Titanium_Frame",
    "Satellite_SOS",
    "AI_ISP_Chip",
]


def score_design(chrom: list[int]) -> float:
    weights = [22.0, 20.0, 25.0, 15.0, 12.0, 18.0]
    penalty = 18.0 if sum(chrom) > 4 else 0.0  # BOM cost cap beyond 4 flagship modules
    return round(sum(g * w for g, w in zip(chrom, weights)) - penalty, 2)


def tournament_select(pop: list[list[int]], rng: random.Random) -> list[int]:
    a, b = rng.sample(pop, 2)
    return a[:] if score_design(a) >= score_design(b) else b[:]


def crossover(p1: list[int], p2: list[int], rng: random.Random) -> tuple[list[int], list[int]]:
    pt = rng.randint(1, len(p1) - 1)
    return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]


def mutate(chrom: list[int], rate: float, rng: random.Random) -> list[int]:
    return [1 - g if rng.random() < rate else g for g in chrom]


if __name__ == "__main__":
    rng = random.Random(101)
    pop = [[rng.randint(0, 1) for _ in FEATURES] for _ in range(8)]
    for gen in range(10):
        pop.sort(key=score_design, reverse=True)
        next_pop = pop[:2]  # elitism
        while len(next_pop) < len(pop):
            c1, c2 = crossover(tournament_select(pop, rng), tournament_select(pop, rng), rng)
            next_pop.append(mutate(c1, 0.1, rng))
            if len(next_pop) < len(pop):
                next_pop.append(mutate(c2, 0.1, rng))
        pop = next_pop

    best = max(pop, key=score_design)
    selected_specs = [feat for feat, bit in zip(FEATURES, best) if bit == 1]
    print("Evolved Smartphone Specs:", selected_specs, "| Score:", score_design(best))