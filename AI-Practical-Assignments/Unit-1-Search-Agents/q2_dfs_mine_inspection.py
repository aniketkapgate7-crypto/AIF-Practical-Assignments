def dfs_mine_tunnel(tunnels: dict[str, list[str]], start: str, target_shaft: str):
    visited = set()
    traversal_order = []

    def _dfs(node: str, path: list[str]):
        visited.add(node)
        traversal_order.append(node)
        if node == target_shaft:
            return path
        for next_segment in tunnels.get(node, []):
            if next_segment not in visited:
                found = _dfs(next_segment, path + [next_segment])
                if found:
                    return found
        return None

    route = _dfs(start, [start])
    return traversal_order, route


if __name__ == "__main__":
    mine_map = {
        "Entry_Shaft": ["Tunnel_1A", "Tunnel_2A"],
        "Tunnel_1A": ["Tunnel_1B", "Tunnel_1C"],
        "Tunnel_1B": ["Sensor_Bay_1"],
        "Tunnel_1C": [],
        "Sensor_Bay_1": [],
        "Tunnel_2A": ["Tunnel_2B"],
        "Tunnel_2B": ["Deep_Vault"],
        "Deep_Vault": [],
    }
    order, path = dfs_mine_tunnel(mine_map, "Entry_Shaft", "Deep_Vault")
    print("Inspection Order (DFS):", " -> ".join(order))
    print("Path to Target:", " -> ".join(path) if path else "Unreachable")