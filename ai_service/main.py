from nlp import preprocess, correct_spelling, extract_symptoms, extract_duration_days, detect_severity
from model import predict_disease

def recommend_doctor(disease):
    doctor_map = {
        "Flu": "General Physician",
        "Common Cold": "General Physician",
        "COVID-19": "Pulmonologist",
        "Migraine": "Neurologist",
        "Food Poisoning": "Gastroenterologist",
        "Respiratory Issue": "Pulmonologist"
    }

    return doctor_map.get(disease, "General Physician")


def analyze_text(user_text):
    clean_text = preprocess(user_text)
    corrected_text = correct_spelling(clean_text)
    symptoms = extract_symptoms(corrected_text)
    duration = extract_duration_days(corrected_text)
    severity, score = detect_severity(corrected_text, symptoms)

    if symptoms:
        disease, confidence = predict_disease(symptoms)
        doctor = recommend_doctor(disease)
    else:
        disease = "No clear prediction"
        confidence = 0
        doctor = "General Physician"

    result = {
        "original_text": user_text,
        "clean_text": clean_text,
        "corrected_text": corrected_text,
        "detected_symptoms": symptoms,
        "duration_days": duration,
        "severity_score": score,
        "severity_level": severity,
        "predicted_disease": disease,
        "confidence_score": confidence,
        "recommended_doctor": doctor
    }

    return result


if __name__ == "__main__":
    text = "I have high fever for 3 days and strong headache with body pain"

    result = analyze_text(text)

    print("Original Text:", result["original_text"])
    print("Clean Text:", result["clean_text"])
    print("Corrected Text:", result["corrected_text"])
    print("Detected Symptoms:", result["detected_symptoms"])
    print("Duration (days):", result["duration_days"])
    print("Severity Score:", result["severity_score"])
    print("Severity Level:", result["severity_level"])
    print("Predicted Disease:", result["predicted_disease"])
    print("Confidence Score:", result["confidence_score"])
    print("Recommended Doctor:", result["recommended_doctor"])