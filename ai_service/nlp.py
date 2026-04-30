import re
from textblob import TextBlob

# Symptom dictionary with variations
symptom_dict = {
    "fever": ["fever", "high temperature", "hot body", "body is hot", "temperature", "high fever"],
    "headache": ["headache", "head pain", "head hurts", "pain in my head", "my head hurts badly"],
    "cough": ["cough", "coughing", "dry cough", "strong cough", "bad cough"],
    "fatigue": ["fatigue", "tired", "very tired", "weak", "exhausted", "low energy", "feeling weak"],
    "body pain": ["body pain", "muscle pain", "body ache", "muscle ache", "pain in body", "whole body hurts"],
    "sore throat": ["sore throat", "throat pain", "painful throat", "my throat hurts"],
    "chest pain": ["chest pain", "pain in chest", "my chest hurts", "pain in my chest"],
    "shortness of breath": ["shortness of breath", "difficulty breathing", "breathing difficulty", "hard to breathe", "cannot breathe well", "trouble breathing"],
    "vomiting": ["vomiting", "throwing up", "puking", "i vomit", "i threw up"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool", "stomach running"],
    "nausea": ["nausea", "feeling sick", "feel sick", "want to vomit"],
    "dizziness": ["dizziness", "dizzy", "lightheaded", "feeling dizzy"],
    "runny nose": ["runny nose", "blocked nose", "stuffy nose", "nasal congestion", "nose is blocked"],
    "sneezing": ["sneezing", "sneeze", "i keep sneezing"],
    "abdominal pain": ["abdominal pain", "stomach pain", "belly pain", "tummy pain", "pain in stomach", "my stomach hurts"],
    "rash": ["rash", "skin rash", "red spots", "skin redness"],
    "itching": ["itching", "itchy skin", "skin itching", "my skin is itchy"],
    "joint pain": ["joint pain", "pain in joints", "my joints hurt"],
    "back pain": ["back pain", "lower back pain", "my back hurts"],
    "burning urination": ["burning urination", "pain when urinating", "urine pain", "burning pee", "pain while peeing"],
    "frequent urination": ["frequent urination", "urinating a lot", "pee a lot", "going to bathroom a lot"],
    "ear pain": ["ear pain", "earache", "pain in ear", "my ear hurts"],
    "eye redness": ["eye redness", "red eyes", "red eye", "my eyes are red"],
    "blurred vision": ["blurred vision", "blurry vision", "vision problem", "cannot see clearly"],
    "palpitations": ["palpitations", "fast heartbeat", "fast heart beat", "heart racing", "racing heart", "rapid heartbeat", "rapid heart beat", "irregular heartbeat", "irregular heart beat", "my heart beats fast"],
    "anxiety": ["anxiety", "panic", "nervous", "panic attack"],
    "loss of appetite": ["loss of appetite", "not hungry", "no appetite", "do not want to eat"],
    "weight loss": ["weight loss", "losing weight", "getting thinner"],
    "swelling": ["swelling", "swollen", "body swelling"],
    "dry mouth": ["dry mouth", "mouth dryness", "mouth feels dry"]
}


high_severity_words = ["high", "severe", "strong", "extreme", "intense", "serious", "terrible", "worst"]
low_severity_words = ["mild", "slight", "little", "light"]

danger_symptoms = [
    "chest pain",
    "shortness of breath",
    "blurred vision",
    "palpitations",
    "dizziness",
    "burning urination",
    "high fever",
    "vomiting",
    "severe abdominal pain",
    "loss of consciousness",
    "swelling",
    "back pain"
]

# Step 1: Clean text
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Step 2: Spell correction
def correct_spelling(text):
    return str(TextBlob(text).correct())

# Step 3: Symptom extraction
def extract_symptoms(text):
    detected = []

    for symptom, keywords in symptom_dict.items():
        for word in keywords:
            if word in text:
                detected.append(symptom)
                break

    return detected

# Step 4: Extract duration
def extract_duration_days(text):
    """
    Returns duration in days if found, otherwise 0.
    Examples:
    'for 3 days' -> 3
    'for 1 week' -> 7
    '2 weeks' -> 14
    """
    day_match = re.search(r'(\d+)\s+day', text)
    week_match = re.search(r'(\d+)\s+week', text)

    if day_match:
        return int(day_match.group(1))
    elif week_match:
        return int(week_match.group(1)) * 7

    return 0

# Step 5: Better severity detection
def detect_severity(text, symptoms):
    score = 0

    # A) severity words
    for word in high_severity_words:
        if word in text:
            score += 2

    for word in low_severity_words:
        if word in text:
            score -= 1

    # B) danger symptoms
    for symptom in symptoms:
        if symptom in danger_symptoms:
            score += 4

    # C) duration
    duration_days = extract_duration_days(text)
    if duration_days >= 7:
        score += 3
    elif duration_days >= 3:
        score += 2
    elif duration_days >= 1:
        score += 1

    # D) number of symptoms
    if len(symptoms) >= 4:
        score += 3
    elif len(symptoms) >= 2:
        score += 2
    elif len(symptoms) == 1:
        score += 1

    # Final level
    if score >= 6:
        return "High", score
    elif score >= 3:
        return "Medium", score
    else:
        return "Low", score


# Test
if __name__ == "__main__":
   text = "my heart beats fast and i have pain in my chest and hard to breathe"

   clean = preprocess(text)
   corrected = correct_spelling(clean)
   symptoms = extract_symptoms(corrected)
   severity, score = detect_severity(corrected, symptoms)
   duration = extract_duration_days(corrected)

   print("Original:", text)
   print("Clean:", clean)
   print("Corrected:", corrected)
   print("Detected Symptoms:", symptoms)
   print("Duration (days):", duration)
   print("Severity Score:", score)
   print("Severity Level:", severity)