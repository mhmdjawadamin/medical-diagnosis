def get_chatbot_response(message, latest_result=None):
    message = message.lower().strip()

    disclaimer = " This system does not replace a real doctor."

    general_symptom_advice = {
        "fever": "Fever may happen when the body is fighting an infection. Drink fluids, rest, and monitor your temperature. If it lasts more than 3 days or is very high, contact a doctor.",
        "headache": "Headache may be caused by stress, dehydration, migraine, infection, or lack of sleep. If it is sudden, severe, or with blurred vision, seek medical care.",
        "cough": "Cough may be caused by cold, flu, allergy, bronchitis, asthma, or infection. If it comes with chest pain or breathing difficulty, seek medical attention.",
        "chest pain": "Chest pain can be serious. If it is strong, sudden, or with shortness of breath, dizziness, or fast heartbeat, seek urgent medical care immediately.",
        "shortness of breath": "Shortness of breath is a warning symptom. If it is severe, sudden, or with chest pain, seek emergency care.",
        "vomiting": "Vomiting may happen due to food poisoning, infection, migraine, or stomach problems. Drink small amounts of water. If it continues, contact a doctor.",
        "diarrhea": "Diarrhea may be caused by infection, food poisoning, or digestive issues. Drink fluids to avoid dehydration. If it lasts more than 2 days, see a doctor.",
        "rash": "A rash may be caused by allergy, irritation, infection, or skin disease. If it spreads quickly or comes with fever/swelling, see a doctor.",
        "burning urination": "Burning urination may indicate urinary infection. Drink water and consult a doctor, especially if you also have fever or back pain.",
        "dizziness": "Dizziness may happen due to dehydration, low blood pressure, migraine, vertigo, or other causes. If severe or with chest pain, seek medical care."
    }

    emergency_keywords = [
        "chest pain",
        "can't breathe",
        "cannot breathe",
        "difficulty breathing",
        "shortness of breath",
        "fainting",
        "severe bleeding",
        "heart attack",
        "stroke",
        "loss of consciousness"
    ]

    for keyword in emergency_keywords:
        if keyword in message:
            return (
                "This may be an emergency warning sign. Please seek urgent medical care immediately, "
                "especially if symptoms are severe, sudden, or getting worse."
                + disclaimer
            )

    for symptom, advice in general_symptom_advice.items():
        if symptom in message:
            return advice + disclaimer

    if latest_result is None:
        if "hello" in message or "hi" in message:
            return (
                "Hello! I can answer general questions about symptoms, risk levels, confidence scores, "
                "and doctor recommendations. Run an analysis first if you want me to explain your personal result."
                + disclaimer
            )

        if "symptom" in message:
            return (
                "You can enter symptoms like fever, headache, cough, chest pain, shortness of breath, "
                "vomiting, diarrhea, rash, dizziness, burning urination, or body pain."
                + disclaimer
            )

        return (
            "I can help with general symptom explanations. For personalized guidance, please run a symptom analysis first."
            + disclaimer
        )

    disease = latest_result.get("predicted_disease", "unknown condition")
    severity = latest_result.get("severity_level", "unknown")
    confidence = latest_result.get("confidence_score", 0)
    doctor = latest_result.get("recommended_doctor", "General Physician")
    symptoms = latest_result.get("detected_symptoms", [])
    duration = latest_result.get("duration_days", 0)
    urgent_action = latest_result.get("urgent_action", "Please consult a doctor if symptoms continue.")
    top_predictions = latest_result.get("top_predictions", [])

    if "what do i have" in message or "disease" in message or "prediction" in message:
        return (
            f"The AI prediction suggests possible {disease} with {round(confidence * 100)}% confidence. "
            f"Detected symptoms include: {', '.join(symptoms) if symptoms else 'none detected'}."
            + disclaimer
        )

    if "top" in message or "other disease" in message or "possible diseases" in message:
        if top_predictions:
            formatted = ", ".join(
                [f"{item.get('disease')} ({round(item.get('confidence', 0) * 100)}%)" for item in top_predictions]
            )
            return f"The top possible diseases are: {formatted}." + disclaimer

        return "No top prediction list is available yet. Please run the analysis first." + disclaimer

    if "risk" in message or "danger" in message or "serious" in message or "severity" in message:
        return (
            f"Your risk level is {severity}. {urgent_action}"
            + disclaimer
        )

    if "doctor" in message or "specialist" in message or "who should i visit" in message:
        return (
            f"Based on the AI result, the recommended specialist is: {doctor}."
            + disclaimer
        )

    if "confidence" in message or "percentage" in message:
        return (
            f"The confidence score is {round(confidence * 100)}%. "
            "It means how strongly the model matched your symptoms to the predicted disease. "
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
            f"The system detected symptom duration as {duration} day(s). Longer duration can increase risk level."
            + disclaimer
        )

    if "what should i do" in message or "next step" in message or "help me" in message or "advice" in message:
        return urgent_action + disclaimer

    if "hello" in message or "hi" in message:
        return (
            "Hello! I can explain your AI result, risk level, confidence score, detected symptoms, "
            "top possible diseases, recommended doctor, and next steps."
            + disclaimer
        )

    return (
        f"I can help explain your current result: predicted disease is {disease}, risk level is {severity}, "
        f"and recommended doctor is {doctor}. You can ask: 'Is it dangerous?', 'What doctor should I visit?', "
        f"'What do I have?', or 'What should I do next?'."
        + disclaimer
    )