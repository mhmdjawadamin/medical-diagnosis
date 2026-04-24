<?php
session_start();
header("Content-Type: application/json");
require_once "db.php";

// Read JSON sent from frontend
$data = json_decode(file_get_contents("php://input"), true);

// Check if text exists
if (!isset($data["symptoms"])) {
    echo json_encode(["error" => "Missing symptoms field"]);
    exit;
}

$text = $data["symptoms"];

// Flask API URL
$url = "http://127.0.0.1:5000/analyze";

// Prepare request options
$options = [
    "http" => [
        "header"  => "Content-Type: application/json\r\n",
        "method"  => "POST",
        "content" => json_encode(["text" => $text]),
        "ignore_errors" => true
    ]
];

// Send request to Flask
$context = stream_context_create($options);
$result = @file_get_contents($url, false, $context);

// Return error if Flask fails
if ($result === FALSE) {
    $error = error_get_last();
    echo json_encode([
        "error" => "Failed to connect to Flask API",
        "details" => $error ? $error["message"] : "Unknown error"
    ]);
    exit;
}

// Decode Flask result
$predictionData = json_decode($result, true);

if (!$predictionData) {
    echo json_encode([
        "error" => "Invalid response from Flask API"
    ]);
    exit;
}

// Save prediction if user is logged in
if (isset($_SESSION["user_id"])) {
    $user_id = $_SESSION["user_id"];

    $input_text = $text;
    $detected_symptoms = isset($predictionData["detected_symptoms"]) ? implode(", ", $predictionData["detected_symptoms"]) : "";
    $predicted_disease = $predictionData["predicted_disease"] ?? "";
    $confidence_score = isset($predictionData["confidence_score"]) ? (float)$predictionData["confidence_score"] : 0;
    $severity_level = $predictionData["severity_level"] ?? "";
    $severity_score = isset($predictionData["severity_score"]) ? (int)$predictionData["severity_score"] : 0;
    $recommended_doctor = $predictionData["recommended_doctor"] ?? "";
    $duration_days = isset($predictionData["duration_days"]) ? (int)$predictionData["duration_days"] : 0;

    $sql = "INSERT INTO predictions 
    (user_id, input_text, detected_symptoms, predicted_disease, confidence_score, severity_level, severity_score, recommended_doctor, duration_days)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";

    $stmt = $conn->prepare($sql);

    if ($stmt) {
        $stmt->bind_param(
            "isssdsisi",
            $user_id,
            $input_text,
            $detected_symptoms,
            $predicted_disease,
            $confidence_score,
            $severity_level,
            $severity_score,
            $recommended_doctor,
            $duration_days
        );
        $stmt->execute();
        $stmt->close();
    }
}

$conn->close();

// Return Flask result to frontend
echo json_encode($predictionData);
