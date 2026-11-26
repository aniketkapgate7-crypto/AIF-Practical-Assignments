import heapq


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar_warehouse(grid: list[list[int]], start: tuple[int, int], goal: tuple[int, int]):
    rows, cols = len(grid), len(grid[0])
    open_heap = [(manhattan_distance(start, goal), 0, start, [start])]
    best_g = {start: 0}

    while open_heap:
        _, g, current, path = heapq.heappop(open_heap)
        if current == goal:
            return path, g

        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                new_g = g + 1
                if new_g < best_g.get(nxt, float("inf")):
                    best_g[nxt] = new_g
                    f = new_g + manhattan_distance(nxt, goal)
                    heapq.heappush(open_heap, (f, new_g, nxt, path + [nxt]))
    return None, -1


if __name__ == "__main__":
    # 0 = free aisle, 1 = storage rack/obstacle
    warehouse_grid = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0],
    ]
    path, cost = astar_warehouse(warehouse_grid, (0, 0), (4, 4))
    print("Optimal Path:", path)
    print("Total Steps/Cost:", cost)