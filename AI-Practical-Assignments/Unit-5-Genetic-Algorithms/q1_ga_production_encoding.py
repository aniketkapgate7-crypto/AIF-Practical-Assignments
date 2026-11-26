import random


def generate_population(pop_size: int, num_lines: int, seed: int = 42) -> list[list[int]]:
    rng = random.Random(seed)
    # Each gene represents active batches scheduled on a production line (0..5)
    return [[rng.randint(0, 5) for _ in range(num_lines)] for _ in range(pop_size)]


def fitness_function(chromosome: list[int], unit_profit: list[float], setup_cost: list[float]) -> float:
    revenue = sum(batches * profit for batches, profit in zip(chromosome, unit_profit))
    cost = sum(setup for batches, setup in zip(chromosome, setup_cost) if batches > 0)
    return round(revenue - cost, 2)


if __name__ == "__main__":
    profits = [120.0, 150.0, 95.0, 180.0]
    costs = [200.0, 260.0, 140.0, 300.0]
    pop = generate_population(pop_size=6, num_lines=4)
    for idx, chrom in enumerate(pop, start=1):
        print(f"Chromosome {idx}: {chrom} -> Fitness: {fitness_function(chrom, profits, costs)}")