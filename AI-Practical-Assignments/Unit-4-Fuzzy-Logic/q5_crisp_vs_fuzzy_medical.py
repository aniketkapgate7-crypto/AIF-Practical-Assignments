def crisp_risk(bp_systolic: float, glucose_mg_dl: float) -> str:
    # Rigid threshold boundary
    if bp_systolic >= 140 or glucose_mg_dl >= 126:
        return "HIGH_RISK"
    if bp_systolic >= 120 or glucose_mg_dl >= 100:
        return "MODERATE_RISK"
    return "LOW_RISK"


def fuzzy_risk(bp_systolic: float, glucose_mg_dl: float) -> dict[str, float]:
    # Graded membership around borderline values (e.g., BP 138, Glucose 124)
    bp_elev = max(0.0, min(1.0, (bp_systolic - 115.0) / 30.0))
    gluc_elev = max(0.0, min(1.0, (glucose_mg_dl - 95.0) / 40.0))

    high_mu = round(min(bp_elev, gluc_elev), 3)
    mod_mu = round(max(bp_elev, gluc_elev) * (1.0 - high_mu * 0.5), 3)
    low_mu = round(max(0.0, 1.0 - max(high_mu, mod_mu)), 3)
    return {"low_mu": low_mu, "moderate_mu": mod_mu, "high_mu": high_mu}


if __name__ == "__main__":
    # Patient right near clinical cutoff thresholds
    bp, glu = 139.0, 125.0
    print("Crisp Classification:", crisp_risk(bp, glu))
    print("Fuzzy Memberships:   ", fuzzy_risk(bp, glu))