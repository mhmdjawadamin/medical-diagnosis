import pandas as pd
from sklearn.ensemble import RandomForestClassifier

symptom_features = [
    "fever", "headache", "cough", "fatigue", "body pain", "sore throat",
    "chest pain", "shortness of breath", "vomiting", "diarrhea", "nausea",
    "dizziness", "runny nose", "sneezing", "abdominal pain", "rash",
    "itching", "joint pain", "back pain", "burning urination",
    "frequent urination", "ear pain", "eye redness", "blurred vision",
    "palpitations", "anxiety", "loss of appetite", "weight loss",
    "swelling", "dry mouth"
]

def make_row(disease, symptoms):
    row = {symptom: 0 for symptom in symptom_features}
    for symptom in symptoms:
        if symptom in row:
            row[symptom] = 1
    row["disease"] = disease
    return row

data = [
    # 1 Flu
    make_row("Flu", ["fever", "headache", "cough", "fatigue", "body pain"]),
    make_row("Flu", ["fever", "cough", "sore throat", "runny nose"]),
    make_row("Flu", ["fever", "body pain", "fatigue"]),
    make_row("Flu", ["fever", "headache", "body pain"]),
    make_row("Flu", ["fever", "cough", "fatigue", "sore throat"]),
    make_row("Flu", ["fever", "runny nose", "headache", "body pain"]),
    make_row("Flu", ["fever", "fatigue", "cough"]),
    make_row("Flu", ["fever", "body pain", "sore throat"]),
    make_row("Flu", ["fever", "headache", "fatigue"]),
    make_row("Flu", ["fever", "cough", "body pain", "runny nose"]),

    # 2 Common Cold
    make_row("Common Cold", ["runny nose", "sneezing", "sore throat"]),
    make_row("Common Cold", ["cough", "runny nose", "sore throat"]),
    make_row("Common Cold", ["sneezing", "runny nose", "headache"]),
    make_row("Common Cold", ["cough", "sneezing"]),
    make_row("Common Cold", ["runny nose", "sore throat"]),
    make_row("Common Cold", ["cough", "runny nose"]),
    make_row("Common Cold", ["sneezing", "sore throat"]),
    make_row("Common Cold", ["headache", "runny nose"]),
    make_row("Common Cold", ["cough", "sneezing", "sore throat"]),
    make_row("Common Cold", ["runny nose", "sneezing", "fatigue"]),

    # 3 COVID-19
    make_row("COVID-19", ["fever", "cough", "fatigue", "shortness of breath"]),
    make_row("COVID-19", ["fever", "body pain", "headache", "cough"]),
    make_row("COVID-19", ["fever", "chest pain", "shortness of breath"]),
    make_row("COVID-19", ["cough", "shortness of breath", "fatigue"]),
    make_row("COVID-19", ["fever", "sore throat", "cough", "fatigue"]),
    make_row("COVID-19", ["fever", "headache", "body pain", "fatigue"]),
    make_row("COVID-19", ["fever", "cough", "dizziness"]),
    make_row("COVID-19", ["shortness of breath", "cough", "chest pain"]),
    make_row("COVID-19", ["fever", "cough", "body pain"]),
    make_row("COVID-19", ["fever", "fatigue", "shortness of breath"]),

    # 4 Migraine
    make_row("Migraine", ["headache", "nausea", "blurred vision"]),
    make_row("Migraine", ["headache", "vomiting", "dizziness"]),
    make_row("Migraine", ["headache", "dizziness", "blurred vision"]),
    make_row("Migraine", ["headache", "nausea"]),
    make_row("Migraine", ["headache", "vomiting"]),
    make_row("Migraine", ["headache", "blurred vision"]),
    make_row("Migraine", ["headache", "dizziness"]),
    make_row("Migraine", ["headache", "nausea", "vomiting"]),
    make_row("Migraine", ["headache", "fatigue", "dizziness"]),
    make_row("Migraine", ["headache", "blurred vision", "nausea"]),

    # 5 Food Poisoning
    make_row("Food Poisoning", ["vomiting", "diarrhea", "abdominal pain"]),
    make_row("Food Poisoning", ["diarrhea", "nausea", "abdominal pain"]),
    make_row("Food Poisoning", ["vomiting", "nausea", "fatigue"]),
    make_row("Food Poisoning", ["fever", "vomiting", "diarrhea"]),
    make_row("Food Poisoning", ["vomiting", "diarrhea", "nausea"]),
    make_row("Food Poisoning", ["abdominal pain", "vomiting", "diarrhea"]),
    make_row("Food Poisoning", ["fever", "abdominal pain", "diarrhea"]),
    make_row("Food Poisoning", ["vomiting", "dry mouth", "fatigue"]),
    make_row("Food Poisoning", ["diarrhea", "dry mouth", "fatigue"]),
    make_row("Food Poisoning", ["vomiting", "nausea", "abdominal pain"]),

    # 6 Gastritis
    make_row("Gastritis", ["abdominal pain", "nausea", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "vomiting"]),
    make_row("Gastritis", ["nausea", "loss of appetite", "dry mouth"]),
    make_row("Gastritis", ["abdominal pain", "dry mouth"]),
    make_row("Gastritis", ["abdominal pain", "nausea"]),
    make_row("Gastritis", ["loss of appetite", "nausea"]),
    make_row("Gastritis", ["abdominal pain", "vomiting", "loss of appetite"]),
    make_row("Gastritis", ["nausea", "dry mouth"]),
    make_row("Gastritis", ["abdominal pain", "fatigue"]),
    make_row("Gastritis", ["abdominal pain", "nausea", "vomiting"]),

    # 7 Respiratory Issue
    make_row("Respiratory Issue", ["shortness of breath", "chest pain"]),
    make_row("Respiratory Issue", ["cough", "shortness of breath"]),
    make_row("Respiratory Issue", ["chest pain", "dizziness", "shortness of breath"]),
    make_row("Respiratory Issue", ["fatigue", "shortness of breath", "cough"]),
    make_row("Respiratory Issue", ["shortness of breath", "fatigue"]),
    make_row("Respiratory Issue", ["chest pain", "cough"]),
    make_row("Respiratory Issue", ["shortness of breath", "dizziness"]),
    make_row("Respiratory Issue", ["cough", "chest pain", "fatigue"]),
    make_row("Respiratory Issue", ["shortness of breath", "cough", "chest pain"]),
    make_row("Respiratory Issue", ["dizziness", "chest pain"]),

    # 8 Allergy
    make_row("Allergy", ["sneezing", "runny nose", "itching"]),
    make_row("Allergy", ["rash", "itching", "swelling"]),
    make_row("Allergy", ["eye redness", "runny nose", "sneezing"]),
    make_row("Allergy", ["itching", "eye redness"]),
    make_row("Allergy", ["rash", "itching"]),
    make_row("Allergy", ["sneezing", "eye redness"]),
    make_row("Allergy", ["runny nose", "itching"]),
    make_row("Allergy", ["swelling", "rash"]),
    make_row("Allergy", ["sneezing", "runny nose"]),
    make_row("Allergy", ["rash", "eye redness", "itching"]),

    # 9 Urinary Tract Infection
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination"]),
    make_row("Urinary Tract Infection", ["burning urination", "abdominal pain"]),
    make_row("Urinary Tract Infection", ["frequent urination", "back pain"]),
    make_row("Urinary Tract Infection", ["fever", "burning urination", "frequent urination"]),
    make_row("Urinary Tract Infection", ["burning urination", "fever"]),
    make_row("Urinary Tract Infection", ["frequent urination", "abdominal pain"]),
    make_row("Urinary Tract Infection", ["burning urination", "back pain"]),
    make_row("Urinary Tract Infection", ["fever", "abdominal pain", "burning urination"]),
    make_row("Urinary Tract Infection", ["frequent urination", "fever"]),
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination", "back pain"]),

    # 10 Joint Inflammation
    make_row("Joint Inflammation", ["joint pain", "swelling"]),
    make_row("Joint Inflammation", ["joint pain", "fatigue"]),
    make_row("Joint Inflammation", ["joint pain", "body pain", "swelling"]),
    make_row("Joint Inflammation", ["back pain", "joint pain"]),
    make_row("Joint Inflammation", ["joint pain", "swelling", "fatigue"]),
    make_row("Joint Inflammation", ["body pain", "joint pain"]),
    make_row("Joint Inflammation", ["joint pain", "back pain", "fatigue"]),
    make_row("Joint Inflammation", ["swelling", "body pain"]),
    make_row("Joint Inflammation", ["joint pain", "swelling", "body pain"]),
    make_row("Joint Inflammation", ["joint pain", "fatigue", "body pain"]),

    # 11 Asthma
    make_row("Asthma", ["shortness of breath", "cough"]),
    make_row("Asthma", ["shortness of breath", "chest pain"]),
    make_row("Asthma", ["cough", "anxiety", "shortness of breath"]),
    make_row("Asthma", ["fatigue", "shortness of breath"]),
    make_row("Asthma", ["shortness of breath", "cough", "chest pain"]),
    make_row("Asthma", ["shortness of breath", "anxiety"]),
    make_row("Asthma", ["cough", "chest pain"]),
    make_row("Asthma", ["shortness of breath", "fatigue", "anxiety"]),
    make_row("Asthma", ["cough", "fatigue"]),
    make_row("Asthma", ["shortness of breath", "dizziness"]),

    # 12 Bronchitis
    make_row("Bronchitis", ["cough", "chest pain", "sore throat"]),
    make_row("Bronchitis", ["cough", "fatigue", "fever"]),
    make_row("Bronchitis", ["cough", "shortness of breath", "fatigue"]),
    make_row("Bronchitis", ["cough", "body pain", "fever"]),
    make_row("Bronchitis", ["cough", "sore throat", "fatigue"]),
    make_row("Bronchitis", ["cough", "chest pain"]),
    make_row("Bronchitis", ["cough", "fever", "sore throat"]),
    make_row("Bronchitis", ["cough", "body pain", "fatigue"]),
    make_row("Bronchitis", ["cough", "shortness of breath"]),
    make_row("Bronchitis", ["cough", "fever", "chest pain"]),

    # 13 Pneumonia
    make_row("Pneumonia", ["fever", "cough", "shortness of breath"]),
    make_row("Pneumonia", ["fever", "chest pain", "fatigue"]),
    make_row("Pneumonia", ["cough", "chest pain", "shortness of breath"]),
    make_row("Pneumonia", ["fever", "body pain", "shortness of breath"]),
    make_row("Pneumonia", ["fever", "cough", "chest pain"]),
    make_row("Pneumonia", ["fever", "fatigue", "shortness of breath"]),
    make_row("Pneumonia", ["cough", "fatigue", "chest pain"]),
    make_row("Pneumonia", ["fever", "cough", "body pain"]),
    make_row("Pneumonia", ["shortness of breath", "chest pain", "fatigue"]),
    make_row("Pneumonia", ["fever", "cough", "shortness of breath", "chest pain"]),

    # 14 Eczema
    make_row("Eczema", ["rash", "itching"]),
    make_row("Eczema", ["itching", "dry mouth"]),
    make_row("Eczema", ["rash", "itching", "swelling"]),
    make_row("Eczema", ["rash", "dry mouth"]),
    make_row("Eczema", ["itching", "swelling"]),
    make_row("Eczema", ["rash", "itching", "eye redness"]),
    make_row("Eczema", ["itching"]),
    make_row("Eczema", ["rash"]),
    make_row("Eczema", ["itching", "rash"]),
    make_row("Eczema", ["rash", "swelling"]),

    # 15 Skin Infection
    make_row("Skin Infection", ["rash", "swelling", "fever"]),
    make_row("Skin Infection", ["rash", "body pain", "fever"]),
    make_row("Skin Infection", ["swelling", "rash"]),
    make_row("Skin Infection", ["rash", "itching", "swelling"]),
    make_row("Skin Infection", ["fever", "swelling"]),
    make_row("Skin Infection", ["rash", "fever"]),
    make_row("Skin Infection", ["body pain", "swelling"]),
    make_row("Skin Infection", ["rash", "swelling", "body pain"]),
    make_row("Skin Infection", ["itching", "swelling", "fever"]),
    make_row("Skin Infection", ["rash", "fever", "body pain"]),

    # 16 Vertigo
    make_row("Vertigo", ["dizziness", "nausea"]),
    make_row("Vertigo", ["dizziness", "blurred vision"]),
    make_row("Vertigo", ["dizziness", "vomiting"]),
    make_row("Vertigo", ["headache", "dizziness"]),
    make_row("Vertigo", ["dizziness", "nausea", "vomiting"]),
    make_row("Vertigo", ["dizziness", "blurred vision", "nausea"]),
    make_row("Vertigo", ["dizziness", "fatigue"]),
    make_row("Vertigo", ["dizziness", "headache", "blurred vision"]),
    make_row("Vertigo", ["dizziness"]),
    make_row("Vertigo", ["dizziness", "vomiting", "blurred vision"]),

    # 17 Possible Cardiac Issue
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations"]),
    make_row("Possible Cardiac Issue", ["chest pain", "shortness of breath", "dizziness"]),
    make_row("Possible Cardiac Issue", ["palpitations", "anxiety", "chest pain"]),
    make_row("Possible Cardiac Issue", ["chest pain", "blurred vision", "palpitations"]),
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations", "shortness of breath"]),
    make_row("Possible Cardiac Issue", ["palpitations", "dizziness"]),
    make_row("Possible Cardiac Issue", ["chest pain", "anxiety"]),
    make_row("Possible Cardiac Issue", ["chest pain", "dizziness"]),
    make_row("Possible Cardiac Issue", ["palpitations", "shortness of breath"]),
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations", "dizziness"]),

    # 18 Kidney Stone
    make_row("Kidney Stone", ["back pain", "abdominal pain"]),
    make_row("Kidney Stone", ["back pain", "nausea", "vomiting"]),
    make_row("Kidney Stone", ["back pain", "burning urination"]),
    make_row("Kidney Stone", ["abdominal pain", "frequent urination", "back pain"]),
    make_row("Kidney Stone", ["back pain", "abdominal pain", "nausea"]),
    make_row("Kidney Stone", ["back pain", "vomiting"]),
    make_row("Kidney Stone", ["abdominal pain", "burning urination"]),
    make_row("Kidney Stone", ["back pain", "frequent urination"]),
    make_row("Kidney Stone", ["back pain", "nausea"]),
    make_row("Kidney Stone", ["back pain", "abdominal pain", "vomiting"]),
]

df = pd.DataFrame(data)

X = df.drop("disease", axis=1)
y = df["disease"]

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

feature_columns = list(X.columns)

def apply_medical_rules(symptoms):
    symptoms = set(symptoms)

    # 🔴 1. Too few symptoms → don't force prediction
    if len(symptoms) <= 1:
        if "fever" in symptoms:
            return "Flu-like Illness", 0.4, [
                {"disease": "Flu", "confidence": 0.4},
                {"disease": "Common Cold", "confidence": 0.3},
                {"disease": "COVID-19", "confidence": 0.3}
            ]

        return "Insufficient Information", 0.3, []

    # 🔴 2. UTI must have urinary symptoms
    if "burning urination" in symptoms or "frequent urination" in symptoms:
        return None  # allow ML

    # Prevent UTI if no urinary symptoms
    if "fever" in symptoms and not any(s in symptoms for s in ["burning urination", "frequent urination"]):
        if len(symptoms) <= 2:
            return "Flu-like Illness", 0.5, [
                {"disease": "Flu", "confidence": 0.5},
                {"disease": "Common Cold", "confidence": 0.3},
                {"disease": "COVID-19", "confidence": 0.2}
            ]

    # 🔴 3. Cardiac rule
    if "chest pain" in symptoms and ("palpitations" in symptoms or "shortness of breath" in symptoms):
        return "Possible Cardiac Issue", 0.85, [
            {"disease": "Possible Cardiac Issue", "confidence": 0.85},
            {"disease": "Respiratory Issue", "confidence": 0.1},
            {"disease": "Anxiety", "confidence": 0.05}
        ]

    # 🔴 4. Respiratory rule
    if "cough" in symptoms and "shortness of breath" in symptoms:
        return "Respiratory Issue", 0.8, [
            {"disease": "Respiratory Issue", "confidence": 0.8},
            {"disease": "Bronchitis", "confidence": 0.1},
            {"disease": "Pneumonia", "confidence": 0.1}
        ]

    # 🔴 5. Digestive rule
    if "vomiting" in symptoms and "diarrhea" in symptoms:
        return "Food Poisoning", 0.85, [
            {"disease": "Food Poisoning", "confidence": 0.85},
            {"disease": "Gastritis", "confidence": 0.1},
            {"disease": "Flu", "confidence": 0.05}
        ]

    return None


def predict_disease(symptoms):
    # 🔥 APPLY RULES FIRST
    rule_result = apply_medical_rules(symptoms)

    if rule_result is not None:
        return rule_result

    # 🔵 NORMAL ML (your original code)
    input_data = {feature: 0 for feature in feature_columns}

    for symptom in symptoms:
        if symptom in input_data:
            input_data[symptom] = 1

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    confidence = max(probabilities)

    classes = model.classes_
    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []
    for index in top_indices:
        top_predictions.append({
            "disease": classes[index],
            "confidence": round(probabilities[index], 2)
        })

    return prediction, round(confidence, 2), top_predictions


if __name__ == "__main__":
    test_symptoms = ["chest pain", "palpitations", "shortness of breath", "dizziness"]

    disease, confidence, top_predictions = predict_disease(test_symptoms)

    print("Symptoms:", test_symptoms)
    print("Predicted Disease:", disease)
    print("Confidence Score:", confidence)
    print("Top Predictions:", top_predictions)