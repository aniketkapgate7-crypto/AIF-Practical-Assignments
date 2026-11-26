def schedule_exams(courses: list[str], slots: list[str], shared_student_pairs: list[tuple[str, str]]):
    conflicts = {c: set() for c in courses}
    for c1, c2 in shared_student_pairs:
        conflicts[c1].add(c2)
        conflicts[c2].add(c1)

    def backtrack(index: int, timetable: dict[str, str]):
        if index == len(courses):
            return dict(timetable)
        course = courses[index]
        for slot in slots:
            if all(timetable.get(other) != slot for other in conflicts[course]):
                timetable[course] = slot
                ans = backtrack(index + 1, timetable)
                if ans:
                    return ans
                del timetable[course]
        return None

    return backtrack(0, {})


if __name__ == "__main__":
    exam_courses = ["AI101", "ML102", "DS103", "DBMS104", "OS105"]
    time_slots = ["Slot_1_Mon_AM", "Slot_2_Mon_PM", "Slot_3_Tue_AM"]
    overlaps = [("AI101", "ML102"), ("AI101", "DS103"), ("ML102", "DBMS104"), ("DS103", "OS105"), ("DBMS104", "OS105")]

    schedule = schedule_exams(exam_courses, time_slots, overlaps)
    for course, slot in (schedule or {}).items():
        print(f"{course:8s} -> {slot}")