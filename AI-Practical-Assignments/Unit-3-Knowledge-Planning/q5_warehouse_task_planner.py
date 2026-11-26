def plan_deliveries(start: str, orders: list[tuple[str, str]], distances: dict[tuple[str, str], int]):
    # Each order: (package_id, destination_aisle)
    remaining = list(orders)
    current = start
    plan = []
    total_cost = 0

    while remaining:
        # Choose nearest next destination using simple nearest-neighbor heuristic
        best_idx = min(
            range(len(remaining)),
            key=lambda i: distances.get((current, remaining[i][1]), 999),
        )
        pkg_id, dest = remaining.pop(best_idx)
        step_cost = distances.get((current, dest), 1)
        total_cost += step_cost
        plan.append(f"MOVE({current} -> {dest}) [cost={step_cost}]")
        plan.append(f"DROP_PACKAGE({pkg_id} at {dest})")
        current = dest

    return plan, total_cost


if __name__ == "__main__":
    aisle_dists = {
        ("Staging", "Aisle_1"): 3, ("Staging", "Aisle_4"): 9,
        ("Aisle_1", "Aisle_2"): 2, ("Aisle_1", "Aisle_4"): 6,
        ("Aisle_2", "Aisle_4"): 4, ("Aisle_4", "Aisle_2"): 4,
    }
    pkg_orders = [("PKG_1", "Aisle_4"), ("PKG_2", "Aisle_1"), ("PKG_3", "Aisle_2")]
    actions, cost = plan_deliveries("Staging", pkg_orders, aisle_dists)
    for step in actions:
        print(" ", step)
    print("Total Travel Cost:", cost)