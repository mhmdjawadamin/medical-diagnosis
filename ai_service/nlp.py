import re
from textblob import TextBlob

# Symptom dictionary with variations
symptom_dict = {
    "fever": ["fever", "high temperature", "hot body"],
    "headache": ["headache", "head pain", "head hurts"],
    "cough": ["cough", "coughing"],
    "fatigue": ["fatigue", "tired", "weak", "exhausted"],
    "body pain": ["body pain", "muscle pain", "pain in body"],
    "chest pain": ["chest pain", "pain in chest"],
    "shortness of breath": ["shortness of breath", "breathing difficulty", "difficulty breathing"],
    "vomiting": ["vomiting", "throwing up"],
    "diarrhea": ["diarrhea", "loose stool"],
    "sore throat": ["sore throat", "throat pain"],
    "confusion": ["confusion", "confused"],
    "fainting": ["fainting", "passed out", "loss of consciousness"] 
}

high_severity_words = ["high", "severe", "strong", "extreme", "intense", "serious", "terrible", "worst"]
low_severity_words = ["mild", "slight", "little", "light"]

danger_symptoms = [
    "chest pain",
    "shortness of breath",
    "confusion",
    "fainting"
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
   text = "I have headache and fever for 2 days"

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