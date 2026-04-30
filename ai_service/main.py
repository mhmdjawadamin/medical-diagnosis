from nlp import preprocess, correct_spelling, extract_symptoms, extract_duration_days, detect_severity
from model import predict_disease


def recommend_doctor(disease):
    doctor_map = {
        "Flu": "General Physician",
        "Common Cold": "General Physician",
        "COVID-19": "Pulmonologist",
        "Migraine": "Neurologist",
        "Food Poisoning": "Gastroenterologist",
        "Gastritis": "Gastroenterologist",
        "Respiratory Issue": "Pulmonologist",
        "Allergy": "Allergist / Immunologist",
        "Urinary Tract Infection": "Urologist",
        "Joint Inflammation": "Rheumatologist / Orthopedic Doctor",
        "Asthma": "Pulmonologist",
        "Bronchitis": "Pulmonologist",
        "Pneumonia": "Pulmonologist",
        "Eczema": "Dermatologist",
        "Skin Infection": "Dermatologist",
        "Vertigo": "ENT Specialist / Neurologist",
        "Possible Cardiac Issue": "Cardiologist",
        "Kidney Stone": "Urologist"
    }

    return doctor_map.get(disease, "General Physician")


def get_urgent_action(disease, severity_level):
    if severity_level != "High":
        return "Monitor your symptoms, rest well, drink fluids, and consult the recommended doctor if symptoms continue or become worse."

    urgent_map = {
        "Flu": "High-risk flu symptoms detected. Please consult a General Physician, especially if fever lasts more than 3 days or symptoms become worse.",

        "Common Cold": "Symptoms appear stronger than a normal cold. Please consult a General Physician if symptoms persist or worsen.",

        "COVID-19": "High-risk respiratory symptoms detected. Please contact a Pulmonologist. If you have severe breathing difficulty or chest pain, seek emergency care immediately.",

        "Migraine": "Severe headache symptoms detected. Please visit a Neurologist. If headache is sudden, extreme, or comes with blurred vision, seek emergency care.",

        "Food Poisoning": "Serious digestive symptoms detected. Please visit a Gastroenterologist. If vomiting, diarrhea, or dehydration becomes severe, seek urgent medical care.",

        "Gastritis": "Severe stomach symptoms detected. Please consult a Gastroenterologist, especially if pain is strong or vomiting continues.",

        "Respiratory Issue": "High-risk breathing symptoms detected. Please visit a Pulmonologist urgently. If breathing becomes difficult, go to emergency care now.",

        "Allergy": "Possible severe allergic reaction detected. If you experience swelling, breathing difficulty, or dizziness, seek emergency care immediately.",

        "Urinary Tract Infection": "Possible urinary infection detected. Please visit a Urologist. If fever and back pain are severe, seek urgent medical care.",

        "Joint Inflammation": "Severe joint or swelling symptoms detected. Please consult a Rheumatologist or Orthopedic Doctor.",

        "Asthma": "Possible asthma-related breathing difficulty detected. Please contact a Pulmonologist. If breathing becomes severe, seek emergency care immediately.",

        "Bronchitis": "Possible bronchitis with high-risk symptoms. Please consult a Pulmonologist, especially if cough and chest pain worsen.",

        "Pneumonia": "Possible serious lung infection detected. Please visit a Pulmonologist urgently. If fever and breathing difficulty worsen, seek emergency care.",

        "Eczema": "Severe skin irritation detected. Please consult a Dermatologist if rash, itching, or swelling becomes worse.",

        "Skin Infection": "Possible skin infection detected. Please consult a Dermatologist. If fever or swelling increases, seek medical care quickly.",

        "Vertigo": "Severe dizziness or balance symptoms detected. Please consult an ENT Specialist or Neurologist. If dizziness is sudden or severe, seek urgent care.",

        "Possible Cardiac Issue": "Possible heart-related warning signs detected. Please seek urgent medical care or visit a Cardiologist immediately. If chest pain is severe, call emergency services.",

        "Kidney Stone": "Possible kidney stone symptoms detected. Please visit a Urologist. If pain is severe or accompanied by fever, seek urgent medical care."
    }

    return urgent_map.get(
        disease,
        "High-risk symptoms detected. Please seek medical attention as soon as possible."
    )


def analyze_text(user_text):
    clean_text = preprocess(user_text)
    corrected_text = correct_spelling(clean_text)
    symptoms = extract_symptoms(corrected_text)
    duration = extract_duration_days(corrected_text)
    severity, score = detect_severity(corrected_text, symptoms)

    if symptoms:
        disease, confidence, top_predictions = predict_disease(symptoms)
        doctor = recommend_doctor(disease)
        urgent_action = get_urgent_action(disease, severity)
    else:
        disease = "No clear prediction"
        confidence = 0
        top_predictions = []
        doctor = "General Physician"
        urgent_action = "Please describe your symptoms more clearly so the system can provide better guidance."

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
        "top_predictions": top_predictions,
        "recommended_doctor": doctor,
        "urgent_action": urgent_action
    }

    return result


if __name__ == "__main__":
    text = "I have chest pain, rapid heartbeat, dizziness and hard to breathe"

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
    print("Top Predictions:", result["top_predictions"])
    print("Recommended Doctor:", result["recommended_doctor"])
    print("Urgent Action:", result["urgent_action"])