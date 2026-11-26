import math
import random


def solar_yield(tilt_deg: float, azimuth_deg: float) -> float:
    # Smooth synthetic irradiance surface peaking near tilt=28 deg, azimuth=180 deg (South)
    tilt_term = math.exp(-((tilt_deg - 28.0) ** 2) / (2 * 18.0**2))
    az_term = math.exp(-((azimuth_deg - 180.0) ** 2) / (2 * 35.0**2))
    return round(1000.0 * tilt_term * az_term, 3)


def hill_climb_solar(steps: int = 200, step_size: float = 1.5, seed: int = 42):
    rng = random.Random(seed)
    tilt = rng.uniform(0, 60)
    azimuth = rng.uniform(90, 270)
    best_power = solar_yield(tilt, azimuth)

    for _ in range(steps):
        neighbors = [
            (max(0.0, min(60.0, tilt + dt)), max(90.0, min(270.0, azimuth + da)))
            for dt, da in [
                (step_size, 0.0), (-step_size, 0.0),
                (0.0, step_size), (0.0, -step_size),
                (step_size, step_size), (-step_size, -step_size),
            ]
        ]
        candidate_tilt, candidate_az = max(neighbors, key=lambda pos: solar_yield(pos[0], pos[1]))
        candidate_power = solar_yield(candidate_tilt, candidate_az)
        if candidate_power > best_power:
            tilt, azimuth, best_power = candidate_tilt, candidate_az, candidate_power
        else:
            break

    return round(tilt, 2), round(azimuth, 2), best_power


if __name__ == "__main__":
    opt_tilt, opt_az, max_w = hill_climb_solar()
    print(f"Optimal Orientation -> Tilt: {opt_tilt}°, Azimuth: {opt_az}° | Estimated Output: {max_w} W/m²")