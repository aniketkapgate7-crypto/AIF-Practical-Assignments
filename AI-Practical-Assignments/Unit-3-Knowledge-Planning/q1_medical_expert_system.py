RULES = [
    {"symptoms": {"fever", "cough", "body_ache"}, "disease": "Seasonal Influenza", "advice": "Hydrate, rest, and monitor temperature."},
    {"symptoms": {"sneezing", "itchy_eyes", "runny_nose"}, "disease": "Allergic Rhinitis", "advice": "Avoid triggers and consult an allergist."},
    {"symptoms": {"headache", "nausea", "light_sensitivity"}, "disease": "Migraine", "advice": "Rest in a dark room and seek medical care if severe."},
    {"symptoms": {"fever", "stiff_neck", "confusion"}, "disease": "Urgent Neurological Evaluation Needed", "advice": "Seek immediate emergency medical attention."},
]


def diagnose_patient(reported_symptoms: set[str]):
    matches = []
    for rule in RULES:
        matched = reported_symptoms & rule["symptoms"]
        if matched:
            confidence = len(matched) / len(rule["symptoms"])
            matches.append((round(confidence, 2), rule["disease"], sorted(matched), rule["advice"]))
    matches.sort(reverse=True)
    return matches


if __name__ == "__main__":
    patient_input = {"fever", "cough", "body_ache"}
    for conf, disease, hit, advice in diagnose_patient(patient_input):
        print(f"Candidate: {disease} | Match: {conf*100:.0f}% ({hit}) | Note: {advice}")