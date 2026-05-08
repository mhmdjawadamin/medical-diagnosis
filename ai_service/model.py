import pandas as pd
from sklearn.ensemble import RandomForestClassifier


# =========================
# 1) SYMPTOM FEATURES
# =========================

symptom_features = [
    "fever", "headache", "cough", "fatigue", "body pain", "sore throat",
    "chest pain", "shortness of breath", "vomiting", "diarrhea", "nausea",
    "dizziness", "runny nose", "sneezing", "abdominal pain", "rash",
    "itching", "joint pain", "back pain", "burning urination",
    "frequent urination", "ear pain", "eye redness", "blurred vision",
    "palpitations", "anxiety", "loss of appetite", "weight loss",
    "swelling", "dry mouth"
]


# =========================
# 2) SPECIALIST MAP
# =========================

specialist_map = {
    "Flu": "General Doctor",
    "Common Cold": "General Doctor",
    "COVID-19": "General Doctor / Pulmonologist",
    "Migraine": "Neurologist",
    "Food Poisoning": "Gastroenterologist",
    "Gastritis": "Gastroenterologist",
    "Respiratory Issue": "Pulmonologist",
    "Allergy": "Allergist",
    "Urinary Tract Infection": "Urologist",
    "Joint Inflammation": "Rheumatologist",
    "Asthma": "Pulmonologist",
    "Bronchitis": "Pulmonologist",
    "Pneumonia": "Pulmonologist",
    "Eczema": "Dermatologist",
    "Skin Infection": "Dermatologist",
    "Vertigo": "ENT Specialist / Neurologist",
    "Possible Cardiac Issue": "Cardiologist",
    "Kidney Stone": "Urologist",
    "Flu-like Illness": "General Doctor",
    "Insufficient Information": "General Doctor"
}


# =========================
# 3) HELPER FUNCTION
# =========================

def make_row(disease, symptoms):
    row = {symptom: 0 for symptom in symptom_features}

    for symptom in symptoms:
        if symptom in row:
            row[symptom] = 1

    row["disease"] = disease
    return row


# =========================
# 4) DATASET
# 18 diseases x 20 rows = 360 rows
# =========================

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
    make_row("Flu", ["fever", "cough", "body pain"]),
    make_row("Flu", ["fever", "fatigue", "body pain", "headache"]),
    make_row("Flu", ["fever", "sore throat", "headache"]),
    make_row("Flu", ["fever", "cough", "headache"]),
    make_row("Flu", ["fever", "body pain", "cough", "fatigue"]),
    make_row("Flu", ["fever", "runny nose", "sore throat", "fatigue"]),
    make_row("Flu", ["fever", "body pain", "headache", "sore throat"]),
    make_row("Flu", ["fever", "cough", "fatigue", "body pain"]),
    make_row("Flu", ["fever", "headache", "runny nose"]),
    make_row("Flu", ["fever", "body pain", "fatigue", "sore throat"]),

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
    make_row("Common Cold", ["sneezing", "runny nose"]),
    make_row("Common Cold", ["sore throat", "runny nose", "fatigue"]),
    make_row("Common Cold", ["cough", "sore throat", "runny nose"]),
    make_row("Common Cold", ["sneezing", "eye redness", "runny nose"]),
    make_row("Common Cold", ["runny nose", "sneezing", "headache"]),
    make_row("Common Cold", ["sore throat", "cough"]),
    make_row("Common Cold", ["runny nose", "sneezing", "cough"]),
    make_row("Common Cold", ["sore throat", "headache", "runny nose"]),
    make_row("Common Cold", ["sneezing", "runny nose", "fatigue"]),
    make_row("Common Cold", ["runny nose", "cough", "sneezing"]),

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
    make_row("COVID-19", ["fever", "dry mouth", "fatigue"]),
    make_row("COVID-19", ["fever", "cough", "sore throat"]),
    make_row("COVID-19", ["body pain", "fatigue", "cough"]),
    make_row("COVID-19", ["fever", "shortness of breath", "body pain"]),
    make_row("COVID-19", ["fever", "headache", "cough"]),
    make_row("COVID-19", ["cough", "fatigue", "sore throat"]),
    make_row("COVID-19", ["fever", "dizziness", "fatigue"]),
    make_row("COVID-19", ["fever", "cough", "shortness of breath"]),
    make_row("COVID-19", ["headache", "body pain", "fatigue"]),
    make_row("COVID-19", ["fever", "chest pain", "cough"]),

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
    make_row("Migraine", ["headache", "eye redness", "blurred vision"]),
    make_row("Migraine", ["headache", "dizziness", "nausea"]),
    make_row("Migraine", ["headache", "vomiting", "blurred vision"]),
    make_row("Migraine", ["headache", "fatigue", "nausea"]),
    make_row("Migraine", ["headache", "blurred vision", "dizziness"]),
    make_row("Migraine", ["headache", "nausea", "fatigue"]),
    make_row("Migraine", ["headache", "vomiting", "fatigue"]),
    make_row("Migraine", ["headache", "blurred vision", "vomiting"]),
    make_row("Migraine", ["headache", "dizziness", "vomiting"]),
    make_row("Migraine", ["headache", "nausea", "dizziness"]),

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
    make_row("Food Poisoning", ["vomiting", "diarrhea", "dry mouth"]),
    make_row("Food Poisoning", ["nausea", "diarrhea", "fatigue"]),
    make_row("Food Poisoning", ["vomiting", "abdominal pain", "dry mouth"]),
    make_row("Food Poisoning", ["diarrhea", "abdominal pain", "fatigue"]),
    make_row("Food Poisoning", ["fever", "vomiting", "abdominal pain"]),
    make_row("Food Poisoning", ["vomiting", "diarrhea", "fatigue"]),
    make_row("Food Poisoning", ["nausea", "vomiting", "dry mouth"]),
    make_row("Food Poisoning", ["diarrhea", "nausea", "dry mouth"]),
    make_row("Food Poisoning", ["fever", "diarrhea", "fatigue"]),
    make_row("Food Poisoning", ["vomiting", "diarrhea", "abdominal pain", "dry mouth"]),

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
    make_row("Gastritis", ["abdominal pain", "loss of appetite"]),
    make_row("Gastritis", ["nausea", "vomiting", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "nausea", "fatigue"]),
    make_row("Gastritis", ["dry mouth", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "nausea", "dry mouth"]),
    make_row("Gastritis", ["abdominal pain", "vomiting", "dry mouth"]),
    make_row("Gastritis", ["nausea", "fatigue", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "loss of appetite", "fatigue"]),
    make_row("Gastritis", ["vomiting", "loss of appetite"]),
    make_row("Gastritis", ["abdominal pain", "nausea", "loss of appetite", "dry mouth"]),

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
    make_row("Respiratory Issue", ["shortness of breath", "cough", "fatigue"]),
    make_row("Respiratory Issue", ["chest pain", "shortness of breath", "fatigue"]),
    make_row("Respiratory Issue", ["shortness of breath", "body pain"]),
    make_row("Respiratory Issue", ["cough", "chest pain", "shortness of breath"]),
    make_row("Respiratory Issue", ["dizziness", "shortness of breath", "fatigue"]),
    make_row("Respiratory Issue", ["chest pain", "fatigue"]),
    make_row("Respiratory Issue", ["shortness of breath", "anxiety"]),
    make_row("Respiratory Issue", ["cough", "shortness of breath", "sore throat"]),
    make_row("Respiratory Issue", ["chest pain", "shortness of breath", "dizziness"]),
    make_row("Respiratory Issue", ["shortness of breath", "cough", "body pain"]),

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
    make_row("Allergy", ["sneezing", "runny nose", "eye redness"]),
    make_row("Allergy", ["itching", "swelling"]),
    make_row("Allergy", ["rash", "itching", "eye redness"]),
    make_row("Allergy", ["runny nose", "sneezing", "itching"]),
    make_row("Allergy", ["eye redness", "itching", "runny nose"]),
    make_row("Allergy", ["swelling", "itching", "rash"]),
    make_row("Allergy", ["sneezing", "itching"]),
    make_row("Allergy", ["runny nose", "eye redness"]),
    make_row("Allergy", ["rash", "swelling", "itching"]),
    make_row("Allergy", ["sneezing", "runny nose", "rash"]),

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
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination", "abdominal pain"]),
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination", "fever"]),
    make_row("Urinary Tract Infection", ["burning urination", "back pain", "fever"]),
    make_row("Urinary Tract Infection", ["frequent urination", "abdominal pain", "fever"]),
    make_row("Urinary Tract Infection", ["burning urination", "dry mouth"]),
    make_row("Urinary Tract Infection", ["frequent urination", "dry mouth"]),
    make_row("Urinary Tract Infection", ["burning urination", "nausea"]),
    make_row("Urinary Tract Infection", ["frequent urination", "back pain", "abdominal pain"]),
    make_row("Urinary Tract Infection", ["burning urination", "frequent urination", "fatigue"]),
    make_row("Urinary Tract Infection", ["burning urination", "fever", "back pain"]),

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
    make_row("Joint Inflammation", ["joint pain", "swelling", "back pain"]),
    make_row("Joint Inflammation", ["joint pain", "body pain", "fatigue"]),
    make_row("Joint Inflammation", ["swelling", "joint pain", "fatigue"]),
    make_row("Joint Inflammation", ["back pain", "body pain", "joint pain"]),
    make_row("Joint Inflammation", ["joint pain"]),
    make_row("Joint Inflammation", ["joint pain", "body pain"]),
    make_row("Joint Inflammation", ["joint pain", "swelling"]),
    make_row("Joint Inflammation", ["joint pain", "fatigue", "swelling"]),
    make_row("Joint Inflammation", ["joint pain", "back pain"]),
    make_row("Joint Inflammation", ["joint pain", "swelling", "body pain", "fatigue"]),

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
    make_row("Asthma", ["shortness of breath", "cough", "anxiety"]),
    make_row("Asthma", ["shortness of breath", "chest pain", "anxiety"]),
    make_row("Asthma", ["cough", "shortness of breath", "fatigue"]),
    make_row("Asthma", ["shortness of breath", "cough", "dizziness"]),
    make_row("Asthma", ["shortness of breath", "fatigue"]),
    make_row("Asthma", ["cough", "anxiety"]),
    make_row("Asthma", ["shortness of breath", "chest pain", "fatigue"]),
    make_row("Asthma", ["shortness of breath", "cough"]),
    make_row("Asthma", ["shortness of breath", "anxiety", "dizziness"]),
    make_row("Asthma", ["cough", "shortness of breath", "chest pain"]),

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
    make_row("Bronchitis", ["cough", "sore throat", "chest pain"]),
    make_row("Bronchitis", ["cough", "fatigue", "chest pain"]),
    make_row("Bronchitis", ["cough", "fever", "fatigue"]),
    make_row("Bronchitis", ["cough", "shortness of breath", "chest pain"]),
    make_row("Bronchitis", ["cough", "body pain", "sore throat"]),
    make_row("Bronchitis", ["cough", "fever", "body pain"]),
    make_row("Bronchitis", ["cough", "fatigue", "sore throat"]),
    make_row("Bronchitis", ["cough", "shortness of breath", "body pain"]),
    make_row("Bronchitis", ["cough", "chest pain", "fatigue"]),
    make_row("Bronchitis", ["cough", "fever", "shortness of breath"]),

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
    make_row("Pneumonia", ["fever", "cough", "fatigue"]),
    make_row("Pneumonia", ["fever", "shortness of breath", "fatigue"]),
    make_row("Pneumonia", ["fever", "chest pain", "shortness of breath"]),
    make_row("Pneumonia", ["cough", "shortness of breath", "body pain"]),
    make_row("Pneumonia", ["fever", "cough", "dizziness"]),
    make_row("Pneumonia", ["fever", "chest pain", "body pain"]),
    make_row("Pneumonia", ["cough", "chest pain", "fatigue", "shortness of breath"]),
    make_row("Pneumonia", ["fever", "body pain", "fatigue"]),
    make_row("Pneumonia", ["fever", "cough", "sore throat", "shortness of breath"]),
    make_row("Pneumonia", ["fever", "cough", "chest pain", "fatigue"]),

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
    make_row("Eczema", ["rash", "itching", "dry mouth"]),
    make_row("Eczema", ["itching", "eye redness"]),
    make_row("Eczema", ["rash", "itching", "fatigue"]),
    make_row("Eczema", ["rash", "swelling", "itching"]),
    make_row("Eczema", ["itching", "dry mouth", "rash"]),
    make_row("Eczema", ["rash", "eye redness"]),
    make_row("Eczema", ["itching", "swelling", "dry mouth"]),
    make_row("Eczema", ["rash", "itching"]),
    make_row("Eczema", ["itching", "swelling"]),
    make_row("Eczema", ["rash", "itching", "swelling", "dry mouth"]),

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
    make_row("Skin Infection", ["rash", "swelling", "fatigue"]),
    make_row("Skin Infection", ["fever", "rash", "itching"]),
    make_row("Skin Infection", ["swelling", "body pain", "fever"]),
    make_row("Skin Infection", ["rash", "swelling", "fever", "body pain"]),
    make_row("Skin Infection", ["rash", "fatigue", "fever"]),
    make_row("Skin Infection", ["swelling", "fever", "fatigue"]),
    make_row("Skin Infection", ["rash", "body pain", "swelling"]),
    make_row("Skin Infection", ["itching", "rash", "fever"]),
    make_row("Skin Infection", ["rash", "swelling"]),
    make_row("Skin Infection", ["rash", "swelling", "fever", "fatigue"]),

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
    make_row("Vertigo", ["dizziness", "nausea", "fatigue"]),
    make_row("Vertigo", ["dizziness", "blurred vision", "fatigue"]),
    make_row("Vertigo", ["dizziness", "headache", "nausea"]),
    make_row("Vertigo", ["dizziness", "vomiting", "nausea"]),
    make_row("Vertigo", ["dizziness", "eye redness"]),
    make_row("Vertigo", ["dizziness", "blurred vision", "headache"]),
    make_row("Vertigo", ["dizziness", "fatigue", "nausea"]),
    make_row("Vertigo", ["dizziness", "vomiting", "fatigue"]),
    make_row("Vertigo", ["dizziness", "headache", "fatigue"]),
    make_row("Vertigo", ["dizziness", "blurred vision", "vomiting"]),

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
    make_row("Possible Cardiac Issue", ["chest pain", "shortness of breath"]),
    make_row("Possible Cardiac Issue", ["palpitations", "chest pain", "fatigue"]),
    make_row("Possible Cardiac Issue", ["chest pain", "dizziness", "blurred vision"]),
    make_row("Possible Cardiac Issue", ["palpitations", "shortness of breath", "anxiety"]),
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations", "anxiety"]),
    make_row("Possible Cardiac Issue", ["chest pain", "shortness of breath", "fatigue"]),
    make_row("Possible Cardiac Issue", ["palpitations", "dizziness", "blurred vision"]),
    make_row("Possible Cardiac Issue", ["chest pain", "palpitations", "shortness of breath", "dizziness"]),
    make_row("Possible Cardiac Issue", ["chest pain", "anxiety", "palpitations"]),
    make_row("Possible Cardiac Issue", ["palpitations", "shortness of breath", "dizziness"]),

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
    make_row("Kidney Stone", ["back pain", "abdominal pain", "burning urination"]),
    make_row("Kidney Stone", ["back pain", "nausea", "frequent urination"]),
    make_row("Kidney Stone", ["back pain", "vomiting", "abdominal pain"]),
    make_row("Kidney Stone", ["abdominal pain", "frequent urination", "nausea"]),
    make_row("Kidney Stone", ["back pain", "burning urination", "frequent urination"]),
    make_row("Kidney Stone", ["back pain", "abdominal pain", "fever"]),
    make_row("Kidney Stone", ["back pain", "vomiting", "nausea"]),
    make_row("Kidney Stone", ["abdominal pain", "burning urination", "back pain"]),
    make_row("Kidney Stone", ["back pain", "frequent urination", "vomiting"]),
    make_row("Kidney Stone", ["back pain", "abdominal pain", "nausea", "vomiting"]),
]


# =========================
# 5) TRAIN MODEL
# =========================

df = pd.DataFrame(data)

X = df.drop("disease", axis=1)
y = df["disease"]

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight="balanced",
    random_state=42
)

model.fit(X, y)

feature_columns = list(X.columns)


# =========================
# 6) OUTPUT HELPER
# =========================

def build_result(disease, confidence, top_predictions, specialist=None, risk_level="Low"):
    return {
        "disease": disease,
        "confidence": round(float(confidence), 2),
        "top_predictions": top_predictions,
        "specialist": specialist or specialist_map.get(disease, "General Doctor"),
        "risk_level": risk_level
    }


# =========================
# 7) MEDICAL RULES
# Rules should cover dangerous/clear cases only.
# The Random Forest model handles the full symptom list.
# =========================

def apply_medical_rules(symptoms):
    symptoms = set(symptoms)

    if len(symptoms) == 0:
        return build_result(
            "Insufficient Information",
            0.0,
            [],
            "General Doctor",
            "Unknown"
        )

    if len(symptoms) == 1:
        only_symptom = list(symptoms)[0]

        if only_symptom == "fever":
            return build_result(
                "Flu-like Illness",
                0.45,
                [
                    {"disease": "Flu", "confidence": 0.45},
                    {"disease": "COVID-19", "confidence": 0.35},
                    {"disease": "Common Cold", "confidence": 0.20}
                ],
                "General Doctor",
                "Medium"
            )

        return build_result(
            "Insufficient Information",
            0.30,
            [],
            "General Doctor",
            "Unknown"
        )

    # Cardiac danger patterns
    if "chest pain" in symptoms and "palpitations" in symptoms:
        return build_result(
            "Possible Cardiac Issue",
            0.95,
            [
                {"disease": "Possible Cardiac Issue", "confidence": 0.95},
                {"disease": "Anxiety", "confidence": 0.03},
                {"disease": "Respiratory Issue", "confidence": 0.02}
            ],
            "Cardiologist",
            "High"
        )

    if "chest pain" in symptoms and "shortness of breath" in symptoms:
        return build_result(
            "Possible Cardiac Issue",
            0.90,
            [
                {"disease": "Possible Cardiac Issue", "confidence": 0.90},
                {"disease": "Pneumonia", "confidence": 0.06},
                {"disease": "Respiratory Issue", "confidence": 0.04}
            ],
            "Cardiologist",
            "High"
        )

    # Urinary patterns
    if "burning urination" in symptoms and "frequent urination" in symptoms:
        return build_result(
            "Urinary Tract Infection",
            0.92,
            [
                {"disease": "Urinary Tract Infection", "confidence": 0.92},
                {"disease": "Kidney Stone", "confidence": 0.06},
                {"disease": "Gastritis", "confidence": 0.02}
            ],
            "Urologist",
            "Medium"
        )

    if "back pain" in symptoms and "abdominal pain" in symptoms and (
        "vomiting" in symptoms or "burning urination" in symptoms
    ):
        return build_result(
            "Kidney Stone",
            0.88,
            [
                {"disease": "Kidney Stone", "confidence": 0.88},
                {"disease": "Urinary Tract Infection", "confidence": 0.08},
                {"disease": "Gastritis", "confidence": 0.04}
            ],
            "Urologist",
            "High"
        )

    # Digestive patterns
    if "vomiting" in symptoms and "diarrhea" in symptoms:
        return build_result(
            "Food Poisoning",
            0.90,
            [
                {"disease": "Food Poisoning", "confidence": 0.90},
                {"disease": "Gastritis", "confidence": 0.07},
                {"disease": "Flu", "confidence": 0.03}
            ],
            "Gastroenterologist",
            "Medium"
        )

    if "abdominal pain" in symptoms and "nausea" in symptoms and "loss of appetite" in symptoms:
        return build_result(
            "Gastritis",
            0.87,
            [
                {"disease": "Gastritis", "confidence": 0.87},
                {"disease": "Food Poisoning", "confidence": 0.08},
                {"disease": "Kidney Stone", "confidence": 0.05}
            ],
            "Gastroenterologist",
            "Medium"
        )

    # Cold / flu / allergy patterns
    if "sneezing" in symptoms and "runny nose" in symptoms and "sore throat" in symptoms:
        return build_result(
            "Common Cold",
            0.90,
            [
                {"disease": "Common Cold", "confidence": 0.90},
                {"disease": "Allergy", "confidence": 0.07},
                {"disease": "Flu", "confidence": 0.03}
            ],
            "General Doctor",
            "Low"
        )

    if "sneezing" in symptoms and "runny nose" in symptoms and "itching" in symptoms:
        return build_result(
            "Allergy",
            0.88,
            [
                {"disease": "Allergy", "confidence": 0.88},
                {"disease": "Common Cold", "confidence": 0.09},
                {"disease": "Eczema", "confidence": 0.03}
            ],
            "Allergist",
            "Low"
        )

    if "fever" in symptoms and "cough" in symptoms and "body pain" in symptoms:
        return build_result(
            "Flu",
            0.88,
            [
                {"disease": "Flu", "confidence": 0.88},
                {"disease": "COVID-19", "confidence": 0.08},
                {"disease": "Bronchitis", "confidence": 0.04}
            ],
            "General Doctor",
            "Medium"
        )

    # Respiratory patterns
    if "fever" in symptoms and "cough" in symptoms and "shortness of breath" in symptoms:
        return build_result(
            "Pneumonia",
            0.86,
            [
                {"disease": "Pneumonia", "confidence": 0.86},
                {"disease": "COVID-19", "confidence": 0.10},
                {"disease": "Bronchitis", "confidence": 0.04}
            ],
            "Pulmonologist",
            "High"
        )

    if "cough" in symptoms and "shortness of breath" in symptoms and "fever" not in symptoms:
        return build_result(
            "Asthma",
            0.82,
            [
                {"disease": "Asthma", "confidence": 0.82},
                {"disease": "Respiratory Issue", "confidence": 0.12},
                {"disease": "Bronchitis", "confidence": 0.06}
            ],
            "Pulmonologist",
            "Medium"
        )

    if "cough" in symptoms and "chest pain" in symptoms and "sore throat" in symptoms:
        return build_result(
            "Bronchitis",
            0.84,
            [
                {"disease": "Bronchitis", "confidence": 0.84},
                {"disease": "Respiratory Issue", "confidence": 0.10},
                {"disease": "Pneumonia", "confidence": 0.06}
            ],
            "Pulmonologist",
            "Medium"
        )

    # Neurology / ENT patterns
    if "headache" in symptoms and "blurred vision" in symptoms and (
        "nausea" in symptoms or "vomiting" in symptoms
    ):
        return build_result(
            "Migraine",
            0.88,
            [
                {"disease": "Migraine", "confidence": 0.88},
                {"disease": "Vertigo", "confidence": 0.08},
                {"disease": "Possible Cardiac Issue", "confidence": 0.04}
            ],
            "Neurologist",
            "Medium"
        )

    if "dizziness" in symptoms and "nausea" in symptoms and "chest pain" not in symptoms:
        return build_result(
            "Vertigo",
            0.82,
            [
                {"disease": "Vertigo", "confidence": 0.82},
                {"disease": "Migraine", "confidence": 0.12},
                {"disease": "Food Poisoning", "confidence": 0.06}
            ],
            "ENT Specialist / Neurologist",
            "Medium"
        )

    # Skin patterns
    if "rash" in symptoms and "itching" in symptoms and "fever" not in symptoms:
        return build_result(
            "Eczema",
            0.84,
            [
                {"disease": "Eczema", "confidence": 0.84},
                {"disease": "Allergy", "confidence": 0.12},
                {"disease": "Skin Infection", "confidence": 0.04}
            ],
            "Dermatologist",
            "Low"
        )

    if "rash" in symptoms and "swelling" in symptoms and "fever" in symptoms:
        return build_result(
            "Skin Infection",
            0.88,
            [
                {"disease": "Skin Infection", "confidence": 0.88},
                {"disease": "Allergy", "confidence": 0.08},
                {"disease": "Eczema", "confidence": 0.04}
            ],
            "Dermatologist",
            "Medium"
        )

    return None


# =========================
# 8) ML PREDICTION
# =========================

def predict_disease(symptoms, severity_level="Low"):
    rule_result = apply_medical_rules(symptoms)

    if rule_result is not None:
        return rule_result

    input_data = {feature: 0 for feature in feature_columns}

    for symptom in symptoms:
        if symptom in input_data:
            input_data[symptom] = 1

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_

    top_indices = probabilities.argsort()[-3:][::-1]

    top_predictions = []
    for index in top_indices:
        top_predictions.append({
            "disease": classes[index],
            "confidence": round(float(probabilities[index]), 2)
        })

    confidence = round(float(max(probabilities)), 2)
    specialist = specialist_map.get(prediction, "General Doctor")

    if severity_level == "High":
        risk_level = "High"
    elif severity_level == "Medium":
        risk_level = "Medium"
    else:
        if confidence < 0.45:
            risk_level = "Unknown"
        else:
            risk_level = "Low"

    return build_result(
        prediction,
        confidence,
        top_predictions,
        specialist,
        risk_level
    )


# =========================
# 9) TESTING
# =========================

if __name__ == "__main__":
    test_cases = [
        ["sneezing", "sore throat", "runny nose"],
        ["fever", "cough", "body pain"],
        ["chest pain", "palpitations", "shortness of breath", "dizziness"],
        ["burning urination", "frequent urination"],
        ["vomiting", "diarrhea", "abdominal pain"],
        ["headache", "blurred vision", "nausea"],
        ["rash", "itching"],
        ["fever"],
        []
    ]

    for symptoms in test_cases:
        result = predict_disease(symptoms, severity_level="Medium")
        print("\nSymptoms:", symptoms)
        print("Disease:", result["disease"])
        print("Confidence:", result["confidence"])
        print("Top Predictions:", result["top_predictions"])
        print("Specialist:", result["specialist"])
        print("Risk Level:", result["risk_level"])
