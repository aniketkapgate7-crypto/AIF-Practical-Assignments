import heapq
import time
from collections import deque


def benchmark_algorithms(coords: dict[str, tuple[int, int]], graph: dict[str, list[str]], start: str, goal: str):
    def h(n: str) -> float:
        x1, y1 = coords[n]
        x2, y2 = coords[goal]
        return abs(x1 - x2) + abs(y1 - y2)

    results = {}

    # BFS
    t0 = time.perf_counter()
    q = deque([(start, [start])])
    seen = {start}
    expanded = 0
    bfs_path = None
    while q:
        u, p = q.popleft()
        expanded += 1
        if u == goal:
            bfs_path = p
            break
        for v in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append((v, p + [v]))
    results["BFS"] = ((time.perf_counter() - t0) * 1000, expanded, len(bfs_path) - 1 if bfs_path else -1, bfs_path)

    # DFS
    t0 = time.perf_counter()
    stack = [(start, [start])]
    seen = set()
    expanded = 0
    dfs_path = None
    while stack:
        u, p = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        expanded += 1
        if u == goal:
            dfs_path = p
            break
        for v in reversed(graph.get(u, [])):
            if v not in seen:
                stack.append((v, p + [v]))
    results["DFS"] = ((time.perf_counter() - t0) * 1000, expanded, len(dfs_path) - 1 if dfs_path else -1, dfs_path)

    # A*
    t0 = time.perf_counter()
    pq = [(h(start), 0, start, [start])]
    best_g = {start: 0}
    expanded = 0
    astar_path = None
    while pq:
        _, g, u, p = heapq.heappop(pq)
        expanded += 1
        if u == goal:
            astar_path = p
            break
        for v in graph.get(u, []):
            ng = g + 1
            if ng < best_g.get(v, float("inf")):
                best_g[v] = ng
                heapq.heappush(pq, (ng + h(v), ng, v, p + [v]))
    results["A*"] = ((time.perf_counter() - t0) * 1000, expanded, len(astar_path) - 1 if astar_path else -1, astar_path)

    return results


if __name__ == "__main__":
    node_coords = {
        "J1": (0, 0), "J2": (1, 0), "J3": (2, 0),
        "J4": (0, 1), "J5": (1, 1), "J6": (2, 1),
        "J7": (0, 2), "J8": (1, 2), "J9": (2, 2),
    }
    road_graph = {
        "J1": ["J2", "J4"], "J2": ["J1", "J3", "J5"], "J3": ["J2", "J6"],
        "J4": ["J1", "J5", "J7"], "J5": ["J2", "J4", "J6", "J8"], "J6": ["J3", "J5", "J9"],
        "J7": ["J4", "J8"], "J8": ["J5", "J7", "J9"], "J9": ["J6", "J8"],
    }
    stats = benchmark_algorithms(node_coords, road_graph, "J1", "J9")
    for algo, (ms, nodes, hops, p) in stats.items():
        print(f"{algo:4s} | Time: {ms:.4f} ms | Nodes Popped: {nodes:2d} | Hops: {hops:2d} | Path: {' -> '.join(p)}")