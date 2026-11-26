import random
import time


def evaluate_allocation(allocation: list[int], values: list[int], costs: list[int], budget: int):
    total_val = sum(v for x, v in zip(allocation, values) if x == 1)
    total_cost = sum(c for x, c in zip(allocation, costs) if x == 1)
    # Penalize budget overruns heavily
    penalty = max(0, total_cost - budget) * 10
    return total_val - penalty, total_val, total_cost


def hill_climb_allocation(values: list[int], costs: list[int], budget: int, restarts: int = 10, seed: int = 7):
    rng = random.Random(seed)
    n = len(values)
    t0 = time.perf_counter()
    best_overall = None

    for _ in range(restarts):
        curr = [rng.choice([0, 1]) for _ in range(n)]
        curr_score, curr_val, curr_cost = evaluate_allocation(curr, values, costs, budget)

        improved = True
        while improved:
            improved = False
            for i in range(n):
                nxt = curr.copy()
                nxt[i] = 1 - nxt[i]
                score, val, cost = evaluate_allocation(nxt, values, costs, budget)
                if score > curr_score:
                    curr, curr_score, curr_val, curr_cost = nxt, score, val, cost
                    improved = True

        if best_overall is None or curr_score > best_overall[0]:
            best_overall = (curr_score, curr_val, curr_cost, curr)

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return elapsed_ms, best_overall


def backtracking_allocation(values: list[int], costs: list[int], budget: int):
    n = len(values)
    t0 = time.perf_counter()
    best = {"val": 0, "cost": 0, "alloc": [0] * n}

    def dfs(idx: int, curr_val: int, curr_cost: int, chosen: list[int]):
        if curr_cost > budget:
            return
        if idx == n:
            if curr_val > best["val"]:
                best.update({"val": curr_val, "cost": curr_cost, "alloc": chosen.copy()})
            return
        # Include item idx
        chosen.append(1)
        dfs(idx + 1, curr_val + values[idx], curr_cost + costs[idx], chosen)
        chosen.pop()
        # Exclude item idx
        chosen.append(0)
        dfs(idx + 1, curr_val, curr_cost, chosen)
        chosen.pop()

    dfs(0, 0, 0, [])
    elapsed_ms = (time.perf_counter() - t0) * 1000
    return elapsed_ms, (best["val"], best["val"], best["cost"], best["alloc"])


if __name__ == "__main__":
    item_values = [45, 70, 30, 85, 50, 60, 40, 95, 55, 35, 75, 65]
    item_costs = [15, 28, 12, 35, 20, 24, 16, 40, 22, 14, 30, 26]
    max_budget = 110

    hc_ms, (_, hc_val, hc_cost, hc_alloc) = hill_climb_allocation(item_values, item_costs, max_budget)
    bt_ms, (_, bt_val, bt_cost, bt_alloc) = backtracking_allocation(item_values, item_costs, max_budget)

    print(f"Hill Climbing | Time: {hc_ms:.4f} ms | Value: {hc_val} | Cost: {hc_cost}/{max_budget} | Alloc: {hc_alloc}")
    print(f"Backtracking  | Time: {bt_ms:.4f} ms | Value: {bt_val} | Cost: {bt_cost}/{max_budget} | Alloc: {bt_alloc}")