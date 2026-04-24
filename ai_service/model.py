import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Small training dataset
data = [
    {"fever": 1, "headache": 1, "cough": 1, "fatigue": 1, "body pain": 1, "sore throat": 1, "chest pain": 0, "shortness of breath": 0, "vomiting": 0, "diarrhea": 0, "disease": "Flu"},
    {"fever": 1, "headache": 1, "cough": 1, "fatigue": 1, "body pain": 0, "sore throat": 1, "chest pain": 0, "shortness of breath": 1, "vomiting": 0, "diarrhea": 0, "disease": "COVID-19"},
    {"fever": 0, "headache": 1, "cough": 0, "fatigue": 0, "body pain": 0, "sore throat": 0, "chest pain": 0, "shortness of breath": 0, "vomiting": 1, "diarrhea": 0, "disease": "Migraine"},
    {"fever": 0, "headache": 0, "cough": 0, "fatigue": 1, "body pain": 1, "sore throat": 0, "chest pain": 0, "shortness of breath": 0, "vomiting": 1, "diarrhea": 1, "disease": "Food Poisoning"},
    {"fever": 1, "headache": 0, "cough": 1, "fatigue": 0, "body pain": 0, "sore throat": 1, "chest pain": 0, "shortness of breath": 0, "vomiting": 0, "diarrhea": 0, "disease": "Common Cold"},
    {"fever": 0, "headache": 0, "cough": 0, "fatigue": 1, "body pain": 0, "sore throat": 0, "chest pain": 1, "shortness of breath": 1, "vomiting": 0, "diarrhea": 0, "disease": "Respiratory Issue"}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Features and labels
X = df.drop("disease", axis=1)
y = df["disease"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Feature order must stay fixed
feature_columns = list(X.columns)

def predict_disease(symptoms):
    input_data = {feature: 0 for feature in feature_columns}

    for symptom in symptoms:
        if symptom in input_data:
            input_data[symptom] = 1

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Get confidence of predicted class
    confidence = max(probabilities)

    return prediction, round(confidence, 2)

# Test
if __name__ == "__main__":
    test_symptoms = ["fever", "headache", "cough", "fatigue"]
    predicted_disease, confidence = predict_disease(test_symptoms)

    print("Symptoms:", test_symptoms)
    print("Predicted Disease:", predicted_disease)
    print("Confidence Score:", confidence)