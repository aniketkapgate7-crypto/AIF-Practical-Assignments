VEHICLE_RULES = [
    (
        lambda s: s.get("engine_temp_c", 0) > 105 and s.get("coolant_low", False),
        "Engine Overheating (Coolant Loss / Leak)",
        "Stop safely, let engine cool, and inspect radiator/hoses.",
    ),
    (
        lambda s: s.get("clicking_on_start", False) and s.get("battery_voltage", 12.6) < 11.8,
        "Discharged or Failing 12V Battery",
        "Test battery state-of-charge and alternator output.",
    ),
    (
        lambda s: s.get("grinding_noise", False) and s.get("brake_pad_mm", 10) < 3,
        "Worn Brake Pads",
        "Schedule immediate brake pad and rotor inspection.",
    ),
    (
        lambda s: s.get("knocking_noise", False) and s.get("low_octane_fuel", False),
        "Engine Knock / Detonation",
        "Refuel with recommended octane rating and inspect ignition timing.",
    ),
]


def diagnose_vehicle(telemetry: dict):
    findings = []
    for condition, fault, action in VEHICLE_RULES:
        if condition(telemetry):
            findings.append((fault, action))
    return findings or [("No Critical Fault Detected", "Continue routine maintenance schedule.")]


if __name__ == "__main__":
    car_state = {
        "engine_temp_c": 112,
        "coolant_low": True,
        "clicking_on_start": False,
        "battery_voltage": 12.5,
        "grinding_noise": False,
        "brake_pad_mm": 7,
        "knocking_noise": False,
        "low_octane_fuel": False,
    }
    for fault, action in diagnose_vehicle(car_state):
        print(f"Fault: {fault}\nRecommended Action: {action}")