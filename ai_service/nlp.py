import re
from textblob import TextBlob

# =========================
# 1) SYMPTOM DICTIONARY
# =========================

symptom_dict = {
    "fever": [
        "fever", "high fever", "temperature", "high temperature",
        "hot body", "body is hot", "feverish"
    ],

    "headache": [
        "headache", "head pain", "head hurts", "pain in my head",
        "migraine", "pressure in head"
    ],

    "cough": [
        "cough", "coughing", "dry cough", "wet cough", "strong cough",
        "bad cough", "continuous cough"
    ],

    "fatigue": [
        "fatigue", "tired", "very tired", "weak", "weakness",
        "exhausted", "low energy", "feeling weak", "no energy"
    ],

    "body pain": [
        "body pain", "body ache", "body aches", "muscle pain",
        "muscle ache", "muscle aches", "whole body hurts",
        "pain in body", "body hurts"
    ],

    "sore throat": [
        "sore throat", "throat pain", "painful throat",
        "throat hurts", "my throat hurts", "scratchy throat",
        "burning throat", "difficulty swallowing"
    ],

    "runny nose": [
        "runny nose", "blocked nose", "stuffy nose", "nasal congestion",
        "nose is blocked", "nose blocked", "running nose", "watery nose","running nose"
    ],

    "sneezing": [
        "sneezing", "sneeze", "sneezes", "i keep sneezing",
        "keep sneezing", "frequent sneezing"
    ],

    "chest pain": [
        "chest pain", "pain in chest", "pain in my chest",
        "my chest hurts", "chest hurts", "tight chest", "chest tightness"
    ],

    "shortness of breath": [
        "shortness of breath", "difficulty breathing", "breathing difficulty",
        "hard to breathe", "cannot breathe", "can't breathe",
        "cannot breathe well", "trouble breathing", "breathless"
    ],

    "palpitations": [
        "palpitations", "fast heartbeat", "fast heart beat",
        "heart racing", "racing heart", "rapid heartbeat",
        "rapid heart beat", "irregular heartbeat", "irregular heart beat",
        "my heart beats fast", "heart beats fast"
    ],

    "vomiting": [
        "vomiting", "vomit", "throwing up", "threw up",
        "puking", "puke", "i vomit", "i threw up"
    ],

    "diarrhea": [
        "diarrhea", "diarrhoea", "loose stool", "watery stool",
        "stomach running"
    ],

    "nausea": [
        "nausea", "nauseous", "feeling sick", "feel sick",
        "want to vomit", "feel like vomiting"
    ],

    "dizziness": [
        "dizziness", "dizzy", "lightheaded", "light headed",
        "feeling dizzy", "vertigo"
    ],

    "abdominal pain": [
        "abdominal pain", "stomach pain", "belly pain", "tummy pain",
        "pain in stomach", "my stomach hurts", "stomach hurts",
        "severe abdominal pain"
    ],

    "rash": [
        "rash", "skin rash", "red spots", "skin redness",
        "red skin"
    ],

    "itching": [
        "itching", "itchy", "itchy skin", "skin itching",
        "my skin is itchy"
    ],

    "joint pain": [
        "joint pain", "pain in joints", "joints hurt",
        "my joints hurt"
    ],

    "back pain": [
        "back pain", "lower back pain", "my back hurts",
        "back hurts"
    ],

    "burning urination": [
        "burning urination", "pain when urinating", "urine pain",
        "burning pee", "pain while peeing", "burning when peeing",
        "burning while urinating"
    ],

    "frequent urination": [
        "frequent urination", "urinating a lot", "pee a lot",
        "peeing a lot", "going to bathroom a lot"
    ],

    "ear pain": [
        "ear pain", "earache", "pain in ear", "my ear hurts",
        "ear hurts"
    ],

    "eye redness": [
        "eye redness", "red eyes", "red eye", "my eyes are red"
    ],

    "blurred vision": [
        "blurred vision", "blurry vision", "vision problem",
        "cannot see clearly", "can't see clearly"
    ],

    "anxiety": [
        "anxiety", "panic", "nervous", "panic attack",
        "feeling anxious"
    ],

    "loss of appetite": [
        "loss of appetite", "not hungry", "no appetite",
        "do not want to eat", "don't want to eat"
    ],

    "weight loss": [
        "weight loss", "losing weight", "getting thinner"
    ],

    "swelling": [
        "swelling", "swollen", "body swelling", "leg swelling",
        "face swelling"
    ],

    "dry mouth": [
        "dry mouth", "mouth dryness", "mouth feels dry"
    ]
}

high_severity_words = [
    "high", "severe", "strong", "extreme", "intense",
    "serious", "terrible", "worst", "bad", "very bad"
]

low_severity_words = [
    "mild", "slight", "little", "light", "minor"
]

danger_symptoms = [
    "chest pain",
    "shortness of breath",
    "blurred vision",
    "palpitations",
    "dizziness",
    "burning urination",
    "vomiting",
    "severe abdominal pain",
    "swelling"
]


# =========================
# 2) PREPROCESSING
# =========================

def preprocess(text):
    text = text.lower()
    text = text.replace("can't", "cannot")
    text = text.replace("dont", "do not")
    text = text.replace("don't", "do not")
    text = text.replace("im", "i am")
    text = text.replace("i'm", "i am")
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# 3) SPELL CORRECTION
# =========================

def correct_spelling(text):
    """
    We do NOT correct all text blindly because medical words may be changed wrongly.
    So we only use TextBlob carefully.
    """
    try:
        corrected = str(TextBlob(text).correct())
        return corrected
    except:
        return text


# =========================
# 4) SAFE PHRASE MATCHING
# =========================

def phrase_exists(text, phrase):
    """
    Better than: if word in text
    This avoids wrong matches inside other words.
    """
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None


# =========================
# 5) SYMPTOM EXTRACTION
# =========================

def extract_symptoms(text):
    detected = []

    clean_text = preprocess(text)

    # First try without spelling correction
    for symptom, keywords in symptom_dict.items():
        for keyword in keywords:
            if phrase_exists(clean_text, keyword):
                detected.append(symptom)
                break

    # If few symptoms found, try spelling correction too
    if len(detected) < 2:
        corrected_text = correct_spelling(clean_text)

        for symptom, keywords in symptom_dict.items():
            if symptom in detected:
                continue

            for keyword in keywords:
                if phrase_exists(corrected_text, keyword):
                    detected.append(symptom)
                    break

    return list(set(detected))


# =========================
# 6) DURATION EXTRACTION
# =========================

def extract_duration_days(text):
    text = preprocess(text)

    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    for word, number in number_words.items():
        text = re.sub(rf"\b{word}\b", str(number), text)

    day_match = re.search(r"(\d+)\s*(day|days)", text)
    week_match = re.search(r"(\d+)\s*(week|weeks)", text)
    month_match = re.search(r"(\d+)\s*(month|months)", text)

    if day_match:
        return int(day_match.group(1))

    if week_match:
        return int(week_match.group(1)) * 7

    if month_match:
        return int(month_match.group(1)) * 30

    if "yesterday" in text:
        return 1

    if "today" in text:
        return 0

    return 0


# =========================
# 7) SEVERITY DETECTION
# =========================

def detect_severity(text, symptoms):
    text = preprocess(text)
    score = 0

    for word in high_severity_words:
        if phrase_exists(text, word):
            score += 2

    for word in low_severity_words:
        if phrase_exists(text, word):
            score -= 1

    for symptom in symptoms:
        if symptom in danger_symptoms:
            score += 4

    duration_days = extract_duration_days(text)

    if duration_days >= 7:
        score += 3
    elif duration_days >= 3:
        score += 2
    elif duration_days >= 1:
        score += 1

    if len(symptoms) >= 4:
        score += 3
    elif len(symptoms) >= 2:
        score += 2
    elif len(symptoms) == 1:
        score += 1

    # Emergency combination rules
    if "chest pain" in symptoms and "shortness of breath" in symptoms:
        score += 5

    if "palpitations" in symptoms and "chest pain" in symptoms:
        score += 4

    if "fever" in symptoms and duration_days >= 3:
        score += 2

    if score >= 7:
        return "High", score
    elif score >= 3:
        return "Medium", score
    else:
        return "Low", max(score, 0)


# =========================
# 8) FULL NLP PIPELINE
# =========================

def analyze_text(text):
    clean_text = preprocess(text)
    corrected_text = correct_spelling(clean_text)

    symptoms = extract_symptoms(clean_text)

    # Try corrected text only if original text found nothing or very little
    if len(symptoms) < 2:
        symptoms = extract_symptoms(corrected_text)

    duration_days = extract_duration_days(clean_text)
    severity_level, severity_score = detect_severity(clean_text, symptoms)

    return {
        "original_text": text,
        "clean_text": clean_text,
        "corrected_text": corrected_text,
        "detected_symptoms": symptoms,
        "duration_days": duration_days,
        "severity_level": severity_level,
        "severity_score": severity_score
    }


# =========================
# 9) TESTING
# =========================

if __name__ == "__main__":
    test_sentences = [
        "I have high fever for 3 days and strong headache with body pain",
        "I keep sneezing and I have sore throat and runny nose",
        "my heart beats fast and i have pain in my chest and hard to breathe",
        "I have burning when peeing and I pee a lot",
        "I feel dizzy and I have blurry vision",
        "I have cough, sore throat, fever and body aches for three days"
    ]

    for sentence in test_sentences:
        result = analyze_text(sentence)
        print("\nSentence:", sentence)
        print("Detected Symptoms:", result["detected_symptoms"])
        print("Duration:", result["duration_days"])
        print("Severity:", result["severity_level"])
        print("Score:", result["severity_score"])