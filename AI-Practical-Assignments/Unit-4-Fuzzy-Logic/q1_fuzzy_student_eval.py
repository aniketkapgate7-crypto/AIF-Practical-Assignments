def fuzzy_union(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    keys = a.keys() | b.keys()
    return {k: round(max(a.get(k, 0.0), b.get(k, 0.0)), 3) for k in keys}


def fuzzy_intersection(a: dict[str, float], b: dict[str, float]) -> dict[str, float]:
    keys = a.keys() | b.keys()
    return {k: round(min(a.get(k, 0.0), b.get(k, 0.0)), 3) for k in keys}


def fuzzy_complement(a: dict[str, float]) -> dict[str, float]:
    return {k: round(1.0 - v, 3) for k, v in a.items()}


if __name__ == "__main__":
    high_attendance = {"Stu_01": 0.92, "Stu_02": 0.65, "Stu_03": 0.80, "Stu_04": 0.45}
    strong_exams = {"Stu_01": 0.85, "Stu_02": 0.90, "Stu_03": 0.70, "Stu_04": 0.50}

    print("High Attendance AND Strong Exams (Intersection):", fuzzy_intersection(high_attendance, strong_exams))
    print("High Attendance OR Strong Exams (Union):       ", fuzzy_union(high_attendance, strong_exams))
    print("Not High Attendance (Complement):              ", fuzzy_complement(high_attendance))