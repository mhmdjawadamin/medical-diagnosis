from nlp import (
    preprocess,
    correct_spelling,
    extract_symptoms,
    extract_duration_days,
    detect_severity
)
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
        "Kidney Stone": "Urologist",
        "Flu-like Illness": "General Physician",
        "Insufficient Information": "General Physician"
    }

    return doctor_map.get(disease, "General Physician")


def merge_symptoms(symptoms_1, symptoms_2):
    merged = []

    for symptom in symptoms_1 + symptoms_2:
        if symptom not in merged:
            merged.append(symptom)

    return merged


def get_contributing_symptoms(symptoms):
    if not symptoms:
        return []

    return symptoms[:5]


def adjust_severity_from_score(score):
    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"


def personalize_risk(score, symptoms, disease, health_profile):
    personalized_notes = []

    if not health_profile:
        return score, personalized_notes

    age = health_profile.get("age")
    chronic = (health_profile.get("chronic_diseases") or "").lower()
    medications = (health_profile.get("medications") or "").lower()
    allergies = (health_profile.get("allergies") or "").lower()
    smoking = (health_profile.get("smoking_status") or "").lower()
    family_history = (health_profile.get("family_history") or "").lower()

    try:
        age = int(age)
    except:
        age = 0

    if age >= 60:
        score += 2
        personalized_notes.append("Risk increased because the patient is older than 60.")

    if "asthma" in chronic or "respiratory" in chronic or "lung" in chronic:
        if "shortness of breath" in symptoms or "chest pain" in symptoms or "cough" in symptoms:
            score += 3
            personalized_notes.append(
                "Risk increased because the patient has a respiratory condition and breathing-related symptoms."
            )

    if "diabetes" in chronic or "diabetic" in chronic:
        if "vomiting" in symptoms or "diarrhea" in symptoms or "fever" in symptoms:
            score += 2
            personalized_notes.append(
                "Risk increased because the patient has diabetes and symptoms may increase dehydration or infection risk."
            )

    if "heart" in chronic or "cardiac" in chronic or "blood pressure" in chronic or "hypertension" in chronic:
        if "chest pain" in symptoms or "palpitations" in symptoms or "shortness of breath" in symptoms:
            score += 4
            personalized_notes.append(
                "Risk increased because the patient has a heart-related condition and warning symptoms."
            )

    if allergies.strip() != "":
        if "rash" in symptoms or "itching" in symptoms or "swelling" in symptoms or "shortness of breath" in symptoms:
            score += 2
            personalized_notes.append(
                "Risk increased because the patient has allergies and possible allergic symptoms."
            )

    if "current" in smoking or "smoker" in smoking:
        if "cough" in symptoms or "chest pain" in symptoms or "shortness of breath" in symptoms:
            score += 2
            personalized_notes.append(
                "Risk increased because the patient smokes and has respiratory symptoms."
            )

    if "heart" in family_history or "diabetes" in family_history:
        score += 1
        personalized_notes.append("Family medical history may increase overall health risk.")

    if medications.strip() != "":
        personalized_notes.append(
            "Patient uses regular medication, so medical advice should be personalized by a doctor."
        )

    return score, personalized_notes


def get_urgent_action(disease, severity_level, personalized_notes=None):
    personalized_notes = personalized_notes or []

    profile_warning = ""
    if personalized_notes:
        profile_warning = " Profile-based risk factors were detected."

    if severity_level != "High":
        return (
            "Monitor your symptoms, rest well, drink fluids, and consult the recommended doctor if symptoms continue or become worse."
            + profile_warning
        )

    urgent_map = {
        "Flu": "High-risk flu symptoms detected. Please consult a General Physician, especially if fever lasts more than 3 days or symptoms become worse.",
        "Flu-like Illness": "Flu-like symptoms detected with higher risk. Please monitor fever and consult a General Physician if symptoms continue or worsen.",
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
        "Kidney Stone": "Possible kidney stone symptoms detected. Please visit a Urologist. If pain is severe or accompanied by fever, seek urgent medical care.",
        "Insufficient Information": "Not enough symptoms were provided. Please add more symptoms or consult a General Physician if you feel unwell."
    }

    return urgent_map.get(
        disease,
        "High-risk symptoms detected. Please seek medical attention as soon as possible."
    ) + profile_warning


def analyze_text(user_text, health_profile=None):
    clean_text = preprocess(user_text)
    corrected_text = correct_spelling(clean_text)

    # Important fix:
    # Extract from BOTH clean_text and corrected_text.
    # This prevents TextBlob from removing/changing symptoms.
    symptoms_from_clean = extract_symptoms(clean_text)
    symptoms_from_corrected = extract_symptoms(corrected_text)

    symptoms = merge_symptoms(symptoms_from_clean, symptoms_from_corrected)

    duration_clean = extract_duration_days(clean_text)
    duration_corrected = extract_duration_days(corrected_text)
    duration = max(duration_clean, duration_corrected)

    severity, score = detect_severity(clean_text, symptoms)

    contributing_symptoms = get_contributing_symptoms(symptoms)

    if symptoms:
        model_result = predict_disease(
            symptoms,
            severity_level=severity
        )

        disease = model_result["disease"]
        confidence = model_result["confidence"]
        top_predictions = model_result["top_predictions"]

        score, personalized_notes = personalize_risk(
            score,
            symptoms,
            disease,
            health_profile
        )

        severity = adjust_severity_from_score(score)

        doctor = model_result.get(
            "specialist",
            recommend_doctor(disease)
        )

        urgent_action = get_urgent_action(
            disease,
            severity,
            personalized_notes
        )

    else:
        disease = "No clear prediction"
        confidence = 0
        top_predictions = []
        doctor = "General Physician"
        personalized_notes = []
        urgent_action = "Please describe your symptoms more clearly so the system can provide better guidance."

    result = {
        "original_text": user_text,
        "clean_text": clean_text,
        "corrected_text": corrected_text,
        "detected_symptoms": symptoms,
        "contributing_symptoms": contributing_symptoms,
        "duration_days": duration,
        "severity_score": score,
        "severity_level": severity,
        "predicted_disease": disease,
        "confidence_score": confidence,
        "top_predictions": top_predictions,
        "recommended_doctor": doctor,
        "urgent_action": urgent_action,
        "personalized_notes": personalized_notes
    }

    return result


if __name__ == "__main__":
    sample_profile = {
        "age": 65,
        "chronic_diseases": "asthma, diabetes",
        "medications": "insulin",
        "allergies": "penicillin",
        "smoking_status": "current smoker",
        "family_history": "heart disease"
    }

    test_sentences = [
        "I keep sneezing and I have sore throat and runny nose",
        "I have high fever for 3 days and strong headache with body pain",
        "my heart beats fast and i have pain in my chest and hard to breathe",
        "I have burning when peeing and I pee a lot",
        "I have vomiting and diarrhea with stomach pain",
        "I have headache with blurry vision and nausea",
        "I have chest pain, cough, dizziness and hard to breathe for 3 days"
    ]

    for text in test_sentences:
        result = analyze_text(text, sample_profile)

        print("\n==============================")
        print("Original Text:", result["original_text"])
        print("Clean Text:", result["clean_text"])
        print("Corrected Text:", result["corrected_text"])
        print("Detected Symptoms:", result["detected_symptoms"])
        print("Contributing Symptoms:", result["contributing_symptoms"])
        print("Duration Days:", result["duration_days"])
        print("Predicted Disease:", result["predicted_disease"])
        print("Confidence Score:", result["confidence_score"])
        print("Top Predictions:", result["top_predictions"])
        print("Severity Score:", result["severity_score"])
        print("Severity Level:", result["severity_level"])
        print("Recommended Doctor:", result["recommended_doctor"])
        print("Urgent Action:", result["urgent_action"])
        print("Personalized Notes:", result["personalized_notes"])