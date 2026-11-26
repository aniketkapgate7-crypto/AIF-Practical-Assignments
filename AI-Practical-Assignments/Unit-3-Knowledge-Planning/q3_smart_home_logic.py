def evaluate_smart_home(facts: dict[str, bool]) -> dict[str, bool]:
    # Propositional rules expressed as boolean implications
    motion = facts.get("motion_detected", False)
    dark = facts.get("ambient_dark", False)
    temp_high = facts.get("temp_above_28c", False)
    occupied = facts.get("room_occupied", False)
    door_open_away = facts.get("door_opened", False) and facts.get("away_mode", False)
    smoke = facts.get("smoke_detected", False)

    actuators = {
        "lights_on": motion and dark,
        "fan_on": temp_high and occupied,
        "security_alarm_on": door_open_away or smoke,
    }
    return actuators


if __name__ == "__main__":
    sensor_facts = {
        "motion_detected": True,
        "ambient_dark": True,
        "temp_above_28c": True,
        "room_occupied": True,
        "door_opened": False,
        "away_mode": False,
        "smoke_detected": False,
    }
    print("Actuator States:", evaluate_smart_home(sensor_facts))