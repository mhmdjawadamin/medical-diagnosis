def get_chatbot_response(message, latest_result=None):
    message = message.lower().strip()

    disclaimer = " This system does not replace a real doctor."

    # -------------------------------
    # If user has not analyzed yet
    # -------------------------------
    if latest_result is None:
        symptom_keywords = [
            "fever", "headache", "cough", "fatigue", "body pain", "sore throat",
            "chest pain", "shortness of breath", "vomiting", "diarrhea", "nausea",
            "dizziness", "runny nose", "sneezing", "stomach pain", "rash",
            "itching", "joint pain", "back pain", "burning urination",
            "fast heartbeat", "palpitations", "hard to breathe"
        ]

        detected_symptoms = [symptom for symptom in symptom_keywords if symptom in message]

        if len(detected_symptoms) >= 2:
            return (
                "You mentioned multiple symptoms. For a more accurate result, please use the AI Symptom Analyzer first. "
                "It can detect symptoms, predict possible diseases, calculate risk level, and recommend a doctor."
                + disclaimer
            )

        if "fever" in message:
            return (
                "Fever may happen because of infection, flu, cold, or other causes. "
                "Drink fluids, rest, and monitor your temperature. For personalized prediction, use the AI Symptom Analyzer."
                + disclaimer
            )

        if "headache" in message:
            return (
                "Headache can be caused by dehydration, stress, migraine, infection, or lack of sleep. "
                "If it is sudden, severe, or with vision problems, seek medical care."
                + disclaimer
            )

        if "chest pain" in message or "hard to breathe" in message or "shortness of breath" in message:
            return (
                "Chest pain or breathing difficulty can be serious. If symptoms are severe or sudden, seek urgent medical care immediately."
                + disclaimer
            )

        if "hi" in message or "hello" in message:
            return (
                "Hello! I can explain your AI result after you run the Symptom Analyzer. "
                "You can ask me: why this disease, why this risk level, what doctor to visit, or what to do next."
                + disclaimer
            )

        return (
            "I can give general guidance, but for personalized medical analysis, please use the AI Symptom Analyzer first."
            + disclaimer
        )

    # -------------------------------
    # Extract latest result fields
    # -------------------------------
    disease = latest_result.get("predicted_disease", "unknown condition")
    confidence = latest_result.get("confidence_score", 0)
    severity = latest_result.get("severity_level", "unknown")
    severity_score = latest_result.get("severity_score", "unknown")
    symptoms = latest_result.get("detected_symptoms", [])
    contributing_symptoms = latest_result.get("contributing_symptoms", symptoms[:5])
    duration = latest_result.get("duration_days", 0)
    doctor = latest_result.get("recommended_doctor", "General Physician")
    urgent_action = latest_result.get("urgent_action", "Please consult a doctor if symptoms continue.")
    top_predictions = latest_result.get("top_predictions", [])
    personalized_notes = latest_result.get("personalized_notes", [])

    symptoms_text = ", ".join(symptoms) if symptoms else "no symptoms detected"
    contributing_text = ", ".join(contributing_symptoms) if contributing_symptoms else symptoms_text

    profile_text = ""
    if personalized_notes:
        profile_text = " Also, your health profile affected the risk because: " + " ".join(personalized_notes)

    # -------------------------------
    # Explain disease prediction
    # -------------------------------
    if (
        "why this disease" in message
        or "why did you predict" in message
        or "why predicted" in message
        or "why this prediction" in message
        or "explain disease" in message
    ):
        return (
            f"The system predicted {disease} because your detected symptoms include {contributing_text}. "
            f"These symptoms matched patterns learned by the model for {disease}. "
            f"The confidence score is {round(confidence * 100)}%, which means how strongly the detected symptoms matched that pattern."
            + disclaimer
        )

    # -------------------------------
    # Explain risk level
    # -------------------------------
    if (
        "why risk" in message
        or "why high" in message
        or "why medium" in message
        or "why low" in message
        or "explain risk" in message
        or "risk level" in message
        or "severity" in message
    ):
        return (
            f"Your risk level is {severity}. The severity score is {severity_score}. "
            f"The risk is affected by detected symptoms, duration of {duration} day(s), warning symptoms, and health profile factors."
            + profile_text
            + disclaimer
        )

    # -------------------------------
    # Explain confidence
    # -------------------------------
    if "confidence" in message or "percentage" in message or "score mean" in message:
        return (
            f"The confidence score is {round(confidence * 100)}%. "
            "It means how strongly the model matched your symptoms with the predicted disease pattern. "
            "A high confidence score does not mean a confirmed diagnosis."
            + disclaimer
        )

    # -------------------------------
    # Explain health profile effect
    # -------------------------------
    if (
        "health profile" in message
        or "my profile" in message
        or "profile affect" in message
        or "personalized" in message
    ):
        if personalized_notes:
            return (
                "Your health profile affected the analysis in these ways: "
                + " ".join(personalized_notes)
                + disclaimer
            )

        return (
            "No special health-profile risk factors were detected in this analysis."
            + disclaimer
        )

    # -------------------------------
    # Explain top predictions
    # -------------------------------
    if "top" in message or "possible diseases" in message or "other diseases" in message:
        if top_predictions:
            formatted = ", ".join(
                [
                    f"{item.get('disease')} ({round(item.get('confidence', 0) * 100)}%)"
                    for item in top_predictions
                ]
            )
            return (
                f"The top possible diseases are: {formatted}. "
                "The first one is the strongest match, but the others are shown because symptoms can overlap between diseases."
                + disclaimer
            )

        return "No top predictions are available yet. Please run the analyzer first." + disclaimer

    # -------------------------------
    # Doctor recommendation
    # -------------------------------
    if "doctor" in message or "specialist" in message or "who should i visit" in message:
        return (
            f"Based on the AI result, the recommended specialist is: {doctor}. "
            f"This recommendation is linked to the predicted disease: {disease}."
            + disclaimer
        )

    # -------------------------------
    # What should I do?
    # -------------------------------
    if (
        "what should i do" in message
        or "next step" in message
        or "help me" in message
        or "advice" in message
    ):
        return urgent_action + profile_text + disclaimer

    # -------------------------------
    # What do I have?
    # -------------------------------
    if "what do i have" in message or "what is my disease" in message or "result" in message:
        return (
            f"The AI result suggests possible {disease} with {round(confidence * 100)}% confidence. "
            f"Detected symptoms: {symptoms_text}. Recommended doctor: {doctor}."
            + disclaimer
        )

    # -------------------------------
    # Detected symptoms
    # -------------------------------
    if "symptom" in message or "detected" in message:
        return (
            f"The detected symptoms are: {symptoms_text}. "
            f"The main contributing symptoms are: {contributing_text}."
            + disclaimer
        )

    # -------------------------------
    # Greeting
    # -------------------------------
    if "hello" in message or "hi" in message:
        return (
            "Hello! I can explain your AI result. You can ask: "
            "'Why this disease?', 'Why is my risk high?', 'What does confidence mean?', "
            "'How did my health profile affect this?', or 'What should I do next?'."
            + disclaimer
        )

    # -------------------------------
    # Default response
    # -------------------------------
    return (
        f"I can explain your current result. Predicted disease: {disease}, "
        f"risk level: {severity}, confidence: {round(confidence * 100)}%, recommended doctor: {doctor}. "
        "Try asking: 'Why this disease?' or 'Why is my risk level high?'."
        + disclaimer
    )