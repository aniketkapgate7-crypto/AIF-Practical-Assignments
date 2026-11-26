KB_RULES = [
    (["no_display", "fans_spin"], "check_monitor_cable"),
    (["check_monitor_cable", "cable_loose"], "reseat_hdmi_dp_cable"),
    (["no_power_led", "outlet_dead"], "switch_power_strip_or_outlet"),
    (["slow_boot", "high_disk_usage"], "disable_startup_apps_and_scan_disk"),
    (["reseat_hdmi_dp_cable"], "resolve_display_issue"),
    (["switch_power_strip_or_outlet"], "resolve_power_issue"),
    (["disable_startup_apps_and_scan_disk"], "resolve_performance_issue"),
]


def forward_chaining(initial_facts: set[str], rules=KB_RULES) -> set[str]:
    inferred = set(initial_facts)
    added = True
    while added:
        added = False
        for premises, conclusion in rules:
            if conclusion not in inferred and all(p in inferred for p in premises):
                inferred.add(conclusion)
                added = True
    return inferred


def backward_chaining(goal: str, known_facts: set[str], rules=KB_RULES, visited=None) -> bool:
    if visited is None:
        visited = set()
    if goal in known_facts:
        return True
    if goal in visited:
        return False
    visited.add(goal)

    for premises, conclusion in rules:
        if conclusion == goal:
            if all(backward_chaining(p, known_facts, rules, visited.copy()) for p in premises):
                return True
    return False


if __name__ == "__main__":
    ticket_facts = {"no_display", "fans_spin", "cable_loose"}
    derived = forward_chaining(ticket_facts)
    print("Forward Chaining Derived Facts:", sorted(derived))
    print("Backward Chaining Goal 'resolve_display_issue' achievable?:", backward_chaining("resolve_display_issue", ticket_facts))