def solve_frequency_csp(towers: list[str], adjacent_pairs: list[tuple[str, str]], frequencies: list[str]):
    neighbors = {t: set() for t in towers}
    for u, v in adjacent_pairs:
        neighbors[u].add(v)
        neighbors[v].add(u)

    domains = {t: list(frequencies) for t in towers}

    def is_consistent(tower: str, freq: str, assignment: dict[str, str]) -> bool:
        return all(assignment.get(nb) != freq for nb in neighbors[tower])

    def backtrack(assignment: dict[str, str]):
        if len(assignment) == len(towers):
            return assignment

        unassigned = [t for t in towers if t not in assignment]
        # MRV heuristic: fewest remaining legal values
        tower = min(unassigned, key=lambda t: sum(1 for f in domains[t] if is_consistent(t, f, assignment)))

        for freq in domains[tower]:
            if is_consistent(tower, freq, assignment):
                assignment[tower] = freq
                result = backtrack(assignment)
                if result:
                    return result
                del assignment[tower]
        return None

    return backtrack({})


if __name__ == "__main__":
    cell_towers = ["T1", "T2", "T3", "T4", "T5"]
    interference_links = [("T1", "T2"), ("T1", "T3"), ("T2", "T3"), ("T2", "T4"), ("T3", "T5"), ("T4", "T5")]
    channels = ["F1_900MHz", "F2_1800MHz", "F3_2100MHz"]
    plan = solve_frequency_csp(cell_towers, interference_links, channels)
    print("Frequency Assignment:", plan)