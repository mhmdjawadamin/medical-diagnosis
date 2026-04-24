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
- Prediction history per logged-in user

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
