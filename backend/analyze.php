<?php
session_start();
header("Content-Type: application/json");
require_once "db.php";

// Check login
if (!isset($_SESSION["user_id"])) {
    echo json_encode([
        "error" => "User not logged in"
    ]);
    exit;
}

$user_id = $_SESSION["user_id"];

// Read JSON sent from frontend
$data = json_decode(file_get_contents("php://input"), true);

if (!$data || !isset($data["symptoms"])) {
    echo json_encode([
        "error" => "Missing symptoms field"
    ]);
    exit;
}

$text = trim($data["symptoms"]);

if ($text === "") {
    echo json_encode([
        "error" => "Please enter symptoms."
    ]);
    exit;
}

// ------------------------------------------
// 1) Get patient health profile from database
// ------------------------------------------
$profile_sql = "SELECT 
                    age,
                    gender,
                    blood_type,
                    height,
                    weight,
                    allergies,
                    chronic_diseases,
                    medications,
                    past_surgeries,
                    smoking_status,
                    family_history,
                    emergency_contact
                FROM patient_health_profile
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1";

$profile_stmt = $conn->prepare($profile_sql);

$health_profile = null;

if ($profile_stmt) {
    $profile_stmt->bind_param("i", $user_id);
    $profile_stmt->execute();
    $profile_result = $profile_stmt->get_result();

    if ($profile_result->num_rows > 0) {
        $health_profile = $profile_result->fetch_assoc();
    }

    $profile_stmt->close();
}

// If no profile exists, block analyzer
if ($health_profile === null) {
    echo json_encode([
        "error" => "Please complete your health profile before using the AI analyzer."
    ]);
    exit;
}

// ------------------------------------------
// 2) Send symptoms + health profile to Flask
// ------------------------------------------
$url = "http://127.0.0.1:5000/analyze";

$request_body = [
    "text" => $text,
    "health_profile" => $health_profile
];

$options = [
    "http" => [
        "header"  => "Content-Type: application/json\r\n",
        "method"  => "POST",
        "content" => json_encode($request_body),
        "ignore_errors" => true
    ]
];

$context = stream_context_create($options);
$result = @file_get_contents($url, false, $context);

if ($result === FALSE) {
    $error = error_get_last();

    echo json_encode([
        "error" => "Failed to connect to Flask API",
        "details" => $error ? $error["message"] : "Unknown error"
    ]);
    exit;
}

// ------------------------------------------
// 3) Decode Flask response
// ------------------------------------------
$predictionData = json_decode($result, true);

if (!$predictionData) {
    echo json_encode([
        "error" => "Invalid response from Flask API",
        "raw_response" => $result
    ]);
    exit;
}

if (isset($predictionData["error"])) {
    echo json_encode($predictionData);
    exit;
}

// ------------------------------------------
// 4) Save prediction result in database
// ------------------------------------------
$input_text = $text;
$detected_symptoms = isset($predictionData["detected_symptoms"])
    ? implode(", ", $predictionData["detected_symptoms"])
    : "";

$predicted_disease = $predictionData["predicted_disease"] ?? "";
$confidence_score = isset($predictionData["confidence_score"])
    ? (float)$predictionData["confidence_score"]
    : 0;

$top_predictions = isset($predictionData["top_predictions"])
    ? json_encode($predictionData["top_predictions"])
    : "";

$severity_level = $predictionData["severity_level"] ?? "";
$severity_score = isset($predictionData["severity_score"])
    ? (int)$predictionData["severity_score"]
    : 0;

$recommended_doctor = $predictionData["recommended_doctor"] ?? "";
$urgent_action = $predictionData["urgent_action"] ?? "";

$duration_days = isset($predictionData["duration_days"])
    ? (int)$predictionData["duration_days"]
    : 0;

$sql = "INSERT INTO predictions 
        (user_id, input_text, detected_symptoms, predicted_disease, confidence_score, top_predictions, severity_level, severity_score, recommended_doctor, urgent_action, duration_days)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);

if ($stmt) {
    $stmt->bind_param(
        "isssdssissi",
        $user_id,
        $input_text,
        $detected_symptoms,
        $predicted_disease,
        $confidence_score,
        $top_predictions,
        $severity_level,
        $severity_score,
        $recommended_doctor,
        $urgent_action,
        $duration_days
    );

    $stmt->execute();
    $stmt->close();
}

$conn->close();

// ------------------------------------------
// 5) Return AI result to frontend
// ------------------------------------------
echo json_encode($predictionData);
