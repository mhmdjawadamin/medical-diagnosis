# Senior Project - AI Medical Assistant

This project is a small full-stack medical assistant prototype built with:

- A static HTML/CSS/Bootstrap frontend
- A PHP backend running under XAMPP
- A Flask-based Python AI service for symptom analysis
- A MySQL database for users, health profiles, and prediction history

## Project Structure

```text
senior_project/
|-- ai_service/   # Flask API + NLP/model logic
|-- backend/      # PHP endpoints and MySQL connection
|-- database/     # Database schema
`-- frontend/     # HTML pages
```

## Features

- User registration and login
- Health profile creation
- AI symptom analysis through a local Flask API
- Floating medical chatbot on the analyzer page
- Prediction history per logged-in user

## Chatbot

The chatbot is available from the floating chat button on:

```text
frontend/index.html
```

It is implemented across three layers:

- `frontend/index.html` displays the chat widget, stores the most recent analyzer result in `lastResult`, and sends each chat message to the PHP backend.
- `backend/chatbot.php` acts as a PHP proxy. It receives JSON from the frontend and forwards it to the Flask AI service.
- `ai_service/app.py` exposes the `/chatbot` Flask endpoint.
- `ai_service/chatbot.py` contains the rule-based chatbot response logic.

### Chatbot Request Flow

```text
Browser chatbot widget
-> /senior_project/backend/chatbot.php
-> http://127.0.0.1:5000/chatbot
-> get_chatbot_response()
-> JSON reply returned to the browser
```

The frontend sends this JSON shape:

```json
{
  "message": "What doctor should I visit?",
  "latest_result": {
    "predicted_disease": "Flu",
    "confidence_score": 0.86,
    "severity_level": "Medium",
    "recommended_doctor": "General Physician",
    "detected_symptoms": ["fever", "cough"],
    "duration_days": 3,
    "urgent_action": "Please consult a doctor if symptoms continue.",
    "top_predictions": [],
    "personalized_notes": []
  }
}
```

The Flask service returns:

```json
{
  "reply": "Based on your result, the recommended specialist is: General Physician. This system does not replace a real doctor."
}
```

### Chatbot Behavior

Before the user runs the AI Symptom Analyzer, the chatbot gives general guidance for common symptoms such as fever, headache, cough, vomiting, diarrhea, rash, burning urination, and dizziness. If the user describes multiple symptoms directly in chat, it asks them to use the analyzer for a more accurate result.

The chatbot checks for emergency keywords such as chest pain, breathing difficulty, fainting, heart attack, and stroke. When these appear, it tells the user to seek urgent medical care immediately.

After the analyzer has returned a result, the chatbot can explain:

- Predicted disease
- Confidence score
- Severity or risk level
- Detected symptoms
- Symptom duration
- Top possible diseases
- Recommended doctor or specialist
- Health profile notes
- Suggested next steps or urgent guidance

Every chatbot response includes a medical disclaimer that the system does not replace a real doctor.

## Requirements

- XAMPP with Apache and MySQL
- Python 3.10+ recommended
- `pip` for Python packages

## Setup

### 1. Place the project in XAMPP

Keep the project inside:

```text
htdocs/senior_project
```

### 2. Create the database

Create a MySQL database named `medical_ai`, then import:

```text
database/schema.sql
```

Default PHP connection settings are in `backend/db.php`:

- Host: `localhost`
- Database: `medical_ai`
- User: `root`
- Password: empty

If your local setup is different, update `backend/db.php`.

### 3. Install Python dependencies

From the project root:

```bash
pip install -r ai_service/requirements.txt
python -m textblob.download_corpora
```

### 4. Start the Flask AI service

From `ai_service/`:

```bash
python app.py
```

The PHP backend expects the Flask API at:

```text
http://127.0.0.1:5000/analyze
http://127.0.0.1:5000/chatbot
```

### 5. Start Apache and MySQL in XAMPP

Then open the frontend in your browser through Apache, for example:

```text
http://localhost/senior_project/frontend/home.html
```

## Important Notes

- The analyzer page checks whether the logged-in user has completed a health profile before allowing analysis.
- Session-based features require using the app through the PHP/XAMPP server, not by opening HTML files directly from disk.
- The AI model is a simple in-project decision tree trained on a very small sample dataset, so this should be treated as a student prototype and not a production medical tool.

## GitHub Push Checklist

This repository is now prepared with:

- A `.gitignore` for editor files, Python cache files, virtual environments, logs, and common local artifacts
- A `README.md` with setup instructions
- A starter database schema in `database/schema.sql`
- Python dependencies listed in `ai_service/requirements.txt`

Suggested first push commands:

```bash
git add .
git commit -m "Initial project import"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Disclaimer

This project is for educational use and does not replace professional medical advice.
