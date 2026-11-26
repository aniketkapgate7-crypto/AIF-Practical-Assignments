def allocate_shifts(engineers: dict[str, dict], shifts: list[dict]):
    # engineers: {name: {"skill": str, "max_shifts": int}}
    # shifts: [{"id": str, "required_skill": str, "machine_available": bool}]
    shift_count = {e: 0 for e in engineers}
    assignment: dict[str, str] = {}

    def valid(shift: dict, eng_name: str) -> bool:
        eng = engineers[eng_name]
        return (
            shift["machine_available"]
            and eng["skill"] == shift["required_skill"]
            and shift_count[eng_name] < eng["max_shifts"]
        )

    def backtrack(idx: int):
        if idx == len(shifts):
            return dict(assignment)
        shift = shifts[idx]
        for eng_name in engineers:
            if valid(shift, eng_name):
                assignment[shift["id"]] = eng_name
                shift_count[eng_name] += 1
                res = backtrack(idx + 1)
                if res:
                    return res
                shift_count[eng_name] -= 1
                del assignment[shift["id"]]
        return None

    return backtrack(0)


if __name__ == "__main__":
    eng_pool = {
        "Eng_A": {"skill": "CNC_Robotics", "max_shifts": 2},
        "Eng_B": {"skill": "Quality_Vision", "max_shifts": 2},
        "Eng_C": {"skill": "CNC_Robotics", "max_shifts": 1},
        "Eng_D": {"skill": "Quality_Vision", "max_shifts": 1},
    }
    line_shifts = [
        {"id": "Line1_Shift1", "required_skill": "CNC_Robotics", "machine_available": True},
        {"id": "Line1_Shift2", "required_skill": "CNC_Robotics", "machine_available": True},
        {"id": "Line2_Shift1", "required_skill": "Quality_Vision", "machine_available": True},
        {"id": "Line2_Shift2", "required_skill": "Quality_Vision", "machine_available": True},
    ]
    plan = allocate_shifts(eng_pool, line_shifts)
    print("Shift Allocation:", plan)