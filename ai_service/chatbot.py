def get_chatbot_response(message, latest_result=None):
    message = message.lower().strip()

    disclaimer = " This system does not replace a real doctor."

    # Detect if user is describing multiple symptoms directly to chatbot
    symptom_keywords = [
        "fever", "headache", "cough", "fatigue", "body pain", "sore throat",
        "chest pain", "shortness of breath", "vomiting", "diarrhea", "nausea",
        "dizziness", "runny nose", "sneezing", "stomach pain", "rash",
        "itching", "joint pain", "back pain", "burning urination",
        "fast heartbeat", "palpitations", "hard to breathe"
    ]

    detected_in_message = [s for s in symptom_keywords if s in message]

    if len(detected_in_message) >= 2 and latest_result is None:
        return (
            "You mentioned multiple symptoms. For a more accurate result including disease prediction, "
            "risk level, confidence score, and doctor recommendation, please use the AI Symptom Analyzer first."
            + disclaimer
        )

    # Emergency direct warning
    emergency_keywords = [
        "chest pain",
        "cannot breathe",
        "can't breathe",
        "difficulty breathing",
        "shortness of breath",
        "fainting",
        "loss of consciousness",
        "heart attack",
        "stroke"
    ]

    for keyword in emergency_keywords:
        if keyword in message:
            return (
                "This may be an emergency warning sign. Please seek urgent medical care immediately, "
                "especially if symptoms are severe, sudden, or getting worse."
                + disclaimer
            )

    # General symptom advice before analysis
    general_advice = {
        "fever": "Fever may happen when the body is fighting an infection. Drink fluids, rest, and monitor your temperature. If it lasts more than 3 days or is very high, contact a doctor.",
        "headache": "Headache may be caused by stress, dehydration, migraine, infection, or lack of sleep. If it is sudden, severe, or with blurred vision, seek medical care.",
        "cough": "Cough may be caused by cold, flu, allergy, bronchitis, asthma, or infection. If it comes with chest pain or breathing difficulty, seek medical attention.",
        "vomiting": "Vomiting may happen due to food poisoning, infection, migraine, or stomach problems. Drink small amounts of water. If it continues, contact a doctor.",
        "diarrhea": "Diarrhea may be caused by infection, food poisoning, or digestive issues. Drink fluids to avoid dehydration. If it lasts more than 2 days, see a doctor.",
        "rash": "A rash may be caused by allergy, irritation, infection, or skin disease. If it spreads quickly or comes with fever or swelling, see a doctor.",
        "burning urination": "Burning urination may indicate urinary infection. Drink water and consult a doctor, especially if you also have fever or back pain.",
        "dizziness": "Dizziness may happen due to dehydration, low blood pressure, migraine, vertigo, or other causes. If severe or with chest pain, seek medical care."
    }

    # If no analysis result yet
    if latest_result is None:
        for symptom, advice in general_advice.items():
            if symptom in message:
                return (
                    advice
                    + " For a personalized prediction, please use the AI Symptom Analyzer."
                    + disclaimer
                )

        if "hello" in message or "hi" in message:
            return (
                "Hello! I can answer general symptom questions, but for personalized prediction "
                "please use the AI Symptom Analyzer first."
                + disclaimer
            )

        if "symptom" in message:
            return (
                "You can enter symptoms such as fever, cough, headache, chest pain, shortness of breath, "
                "vomiting, diarrhea, rash, dizziness, burning urination, or body pain in the analyzer."
                + disclaimer
            )

        return (
            "I can give general health guidance, but for accurate personalized analysis, "
            "please run the AI Symptom Analyzer first."
            + disclaimer
        )

    # Use latest analyzer result
    disease = latest_result.get("predicted_disease", "unknown condition")
    severity = latest_result.get("severity_level", "unknown")
    confidence = latest_result.get("confidence_score", 0)
    doctor = latest_result.get("recommended_doctor", "General Physician")
    symptoms = latest_result.get("detected_symptoms", [])
    duration = latest_result.get("duration_days", 0)
    urgent_action = latest_result.get("urgent_action", "Please consult a doctor if symptoms continue.")
    top_predictions = latest_result.get("top_predictions", [])
    personalized_notes = latest_result.get("personalized_notes", [])

    profile_text = ""
    if personalized_notes:
        profile_text = " Health profile notes: " + " ".join(personalized_notes)

    if "what do i have" in message or "disease" in message or "prediction" in message:
        return (
            f"The AI prediction suggests possible {disease} with {round(confidence * 100)}% confidence. "
            f"Detected symptoms include: {', '.join(symptoms) if symptoms else 'none detected'}."
            + profile_text
            + disclaimer
        )

    if "top" in message or "other disease" in message or "possible diseases" in message:
        if top_predictions:
            formatted = ", ".join(
                [
                    f"{item.get('disease')} ({round(item.get('confidence', 0) * 100)}%)"
                    for item in top_predictions
                ]
            )
            return f"The top possible diseases are: {formatted}." + disclaimer

        return "No top prediction list is available yet. Please run the analysis first." + disclaimer

    if "risk" in message or "danger" in message or "serious" in message or "severity" in message:
        return (
            f"Your risk level is {severity}. {urgent_action}"
            + profile_text
            + disclaimer
        )

    if "doctor" in message or "specialist" in message or "who should i visit" in message:
        return (
            f"Based on your result, the recommended specialist is: {doctor}."
            + profile_text
            + disclaimer
        )

    if "confidence" in message or "percentage" in message:
        return (
            f"The confidence score is {round(confidence * 100)}%. "
            "It shows how strongly the model matched your symptoms to the predicted disease. "
            "It is not a confirmed diagnosis."
            + disclaimer
        )

    if "symptom" in message or "detected" in message:
        return (
            f"The detected symptoms are: {', '.join(symptoms) if symptoms else 'no symptoms detected'}."
            + disclaimer
        )

    if "duration" in message or "days" in message or "how long" in message:
        return (
            f"The system detected symptom duration as {duration} day(s). "
            "Longer duration can increase risk level."
            + disclaimer
        )

    if "profile" in message or "health profile" in message or "my health" in message:
        if personalized_notes:
            return (
                "Your health profile affected the analysis. "
                + " ".join(personalized_notes)
                + disclaimer
            )

        return (
            "No special health-profile risk factors were detected in this analysis."
            + disclaimer
        )

    if "what should i do" in message or "next step" in message or "help me" in message or "advice" in message:
        return urgent_action + profile_text + disclaimer

    if "hello" in message or "hi" in message:
        return (
            "Hello! I can explain your AI result, risk level, confidence score, detected symptoms, "
            "top possible diseases, health profile notes, recommended doctor, and next steps."
            + disclaimer
        )

    return (
        f"I can help explain your current result. Predicted disease: {disease}, "
        f"risk level: {severity}, recommended doctor: {doctor}. "
        "You can ask: 'Is it dangerous?', 'What doctor should I visit?', "
        "'What do I have?', 'How did my health profile affect this?', or 'What should I do next?'."
        + disclaimer
    )