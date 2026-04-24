CREATE DATABASE IF NOT EXISTS medical_ai;
USE medical_ai;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patient_health_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    age INT NULL,
    gender VARCHAR(20) NULL,
    blood_type VARCHAR(10) NULL,
    height DOUBLE NULL,
    weight DOUBLE NULL,
    allergies TEXT NULL,
    chronic_diseases TEXT NULL,
    medications TEXT NULL,
    past_surgeries TEXT NULL,
    smoking_status VARCHAR(50) NULL,
    family_history TEXT NULL,
    emergency_contact VARCHAR(150) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_patient_profile_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    input_text TEXT NOT NULL,
    detected_symptoms TEXT NULL,
    predicted_disease VARCHAR(150) NULL,
    confidence_score DECIMAL(5,2) DEFAULT 0,
    severity_level VARCHAR(20) NULL,
    severity_score INT DEFAULT 0,
    recommended_doctor VARCHAR(150) NULL,
    duration_days INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_predictions_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);
