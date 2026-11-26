def trap_mf(x: float, a: float, b: float, c: float, d: float) -> float:
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (d - x) / (d - c)


def ac_fan_speed(temp_c: float, humidity_pct: float) -> float:
    # Fuzzify temperature (C) and humidity (%)
    warm_temp = trap_mf(temp_c, 22.0, 26.0, 34.0, 38.0)
    cool_temp = trap_mf(temp_c, 15.0, 18.0, 22.0, 25.0)
    humid = trap_mf(humidity_pct, 45.0, 65.0, 95.0, 100.0)

    # Rule strengths (Mamdani min) -> mapped fan speed (%) on 0..100
    rules = [
        (min(warm_temp, humid), 90.0),      # Hot & humid -> High fan
        (min(warm_temp, 1.0 - humid), 65.0), # Warm & dry -> Medium-High fan
        (min(cool_temp, humid), 45.0),       # Cool & humid -> Medium fan
        (min(cool_temp, 1.0 - humid), 20.0), # Cool & dry -> Low fan
    ]

    num = sum(w * speed for w, speed in rules)
    den = sum(w for w, _ in rules)
    return round(num / den, 2) if den > 0 else 25.0


if __name__ == "__main__":
    print("Recommended Fan Speed (%):", ac_fan_speed(temp_c=29.5, humidity_pct=75.0))