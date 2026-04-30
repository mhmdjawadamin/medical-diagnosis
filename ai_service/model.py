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
    make_row("Flu", ["fever", "headache", "cough", "fatigue", "body pain", "sore throat", "runny nose"]),
    make_row("Flu", ["fever", "cough", "body pain", "fatigue", "headache"]),

    # 2 Common Cold
    make_row("Common Cold", ["cough", "sore throat", "runny nose", "sneezing"]),
    make_row("Common Cold", ["headache", "runny nose", "sneezing", "cough"]),

    # 3 COVID-19
    make_row("COVID-19", ["fever", "cough", "fatigue", "body pain", "shortness of breath", "headache"]),
    make_row("COVID-19", ["fever", "sore throat", "cough", "chest pain", "shortness of breath"]),

    # 4 Migraine
    make_row("Migraine", ["headache", "nausea", "vomiting", "dizziness", "blurred vision"]),
    make_row("Migraine", ["headache", "dizziness", "nausea"]),

    # 5 Food Poisoning
    make_row("Food Poisoning", ["vomiting", "diarrhea", "nausea", "abdominal pain", "fever"]),
    make_row("Food Poisoning", ["vomiting", "diarrhea", "abdominal pain", "fatigue"]),

    # 6 Gastritis
    make_row("Gastritis", ["abdominal pain", "nausea", "vomiting", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "nausea", "dry mouth"]),

    # 7 Respiratory Issue
    make_row("Respiratory Issue", ["cough", "chest pain", "shortness of breath", "fatigue"]),
    make_row("Respiratory Issue", ["shortness of breath", "chest pain", "dizziness"]),

    # 8 Allergy
    make_row("Allergy", ["sneezing", "runny nose", "itching", "rash", "eye redness"]),
    make_row("Allergy", ["itching", "rash", "sneezing", "eye redness"]),

    # 9 Urinary Tract Infection
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination", "abdominal pain", "fever"]),
    make_row("Urinary Tract Infection", ["burning urination", "back pain", "frequent urination"]),

    # 10 Joint Inflammation
    make_row("Joint Inflammation", ["joint pain", "swelling", "fatigue", "body pain"]),
    make_row("Joint Inflammation", ["joint pain", "back pain", "swelling"]),

    # 11 Asthma
    make_row("Asthma", ["shortness of breath", "cough", "chest pain", "fatigue"]),
    make_row("Asthma", ["shortness of breath", "cough", "anxiety"]),

    # 12 Bronchitis
    make_row("Bronchitis", ["cough", "chest pain", "fatigue", "fever", "sore throat"]),
    make_row("Bronchitis", ["cough", "shortness of breath", "chest pain"]),

    # 13 Pneumonia
    make_row("Pneumonia", ["fever", "cough", "chest pain", "shortness of breath", "fatigue"]),
    make_row("Pneumonia", ["fever", "shortness of breath", "chest pain", "body pain"]),

    # 14 Eczema
    make_row("Eczema", ["rash", "itching", "dry mouth"]),
    make_row("Eczema", ["itching", "rash", "swelling"]),

    # 15 Skin Infection
    make_row("Skin Infection", ["rash", "swelling", "fever", "body pain"]),
    make_row("Skin Infection", ["rash", "itching", "swelling"]),

    # 16 Vertigo
    make_row("Vertigo", ["dizziness", "nausea", "vomiting", "blurred vision"]),
    make_row("Vertigo", ["dizziness", "headache", "nausea"]),

    # 17 Possible Cardiac Issue
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations", "shortness of breath", "dizziness", "anxiety"]),
    make_row("Possible Cardiac Issue", ["palpitations", "chest pain", "blurred vision"]),

    # 18 Kidney Stone
    make_row("Kidney Stone", ["back pain", "abdominal pain", "burning urination", "nausea", "vomiting"]),
    make_row("Kidney Stone", ["back pain", "frequent urination", "abdominal pain"]),
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

def predict_disease(symptoms):
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