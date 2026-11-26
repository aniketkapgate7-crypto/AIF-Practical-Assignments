from collections import deque


class HospitalDeliveryAgent:
    def __init__(self, corridor_graph: dict[str, list[str]], blocked_edges: set[tuple[str, str]]):
        self.graph = corridor_graph
        self.blocked = set()
        for u, v in blocked_edges:
            self.blocked.add((u, v))
            self.blocked.add((v, u))

    def is_passable(self, u: str, v: str) -> bool:
        return (u, v) not in self.blocked

    def plan_route(self, start: str, goal: str) -> list[str] | None:
        if start == goal:
            return [start]
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            curr, path = queue.popleft()
            for nxt in self.graph.get(curr, []):
                if nxt not in visited and self.is_passable(curr, nxt):
                    if nxt == goal:
                        return path + [nxt]
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))
        return None

    def deliver_medicines(self, start_bay: str, deliveries: list[tuple[str, str]]):
        current_loc = start_bay
        for patient_id, dept in deliveries:
            route = self.plan_route(current_loc, dept)
            if route:
                print(f"[DELIVERED {patient_id}] Route {current_loc} -> {dept}: {' -> '.join(route)}")
                current_loc = dept
            else:
                print(f"[BLOCKED  {patient_id}] No clear path from {current_loc} to {dept}")


if __name__ == "__main__":
    hospital_map = {
        "Pharmacy": ["Central_Lobby", "East_Wing"],
        "Central_Lobby": ["Pharmacy", "ICU", "Cardiology", "Pediatrics"],
        "East_Wing": ["Pharmacy", "Cardiology", "Oncology"],
        "ICU": ["Central_Lobby"],
        "Cardiology": ["Central_Lobby", "East_Wing", "Oncology"],
        "Pediatrics": ["Central_Lobby"],
        "Oncology": ["East_Wing", "Cardiology"],
    }
    blocked = {("Central_Lobby", "ICU"), ("East_Wing", "Oncology")}
    agent = HospitalDeliveryAgent(hospital_map, blocked)
    agent.deliver_medicines("Pharmacy", [("P101", "ICU"), ("P102", "Oncology"), ("P103", "Pediatrics")])