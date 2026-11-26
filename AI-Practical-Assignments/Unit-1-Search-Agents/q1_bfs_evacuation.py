from collections import deque


def bfs_evacuation(road_network: dict[str, list[str]], start: str, evacuation_centers: set[str]):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()
        if current in evacuation_centers:
            return path
        for neighbor in road_network.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


if __name__ == "__main__":
    city_roads = {
        "Zone_A": ["Zone_B", "Zone_C"],
        "Zone_B": ["Zone_A", "Zone_D", "Shelter_North"],
        "Zone_C": ["Zone_A", "Zone_E"],
        "Zone_D": ["Zone_B", "Shelter_East"],
        "Zone_E": ["Zone_C", "Shelter_East"],
        "Shelter_North": [],
        "Shelter_East": [],
    }
    centers = {"Shelter_North", "Shelter_East"}
    route = bfs_evacuation(city_roads, "Zone_A", centers)
    print("Nearest Evacuation Route (BFS):", " -> ".join(route) if route else "No route found")