<?php
session_start();
header("Content-Type: application/json");
require_once "db.php";

if (!isset($_SESSION["user_id"])) {
    echo json_encode([
        "success" => false,
        "message" => "User not logged in"
    ]);
    exit;
}

$user_id = $_SESSION["user_id"];

$data = json_decode(file_get_contents("php://input"), true);

if (!$data) {
    echo json_encode([
        "success" => false,
        "message" => "No prediction data received"
    ]);
    exit;
}

$input_text = $data["input_text"] ?? "";
$detected_symptoms = isset($data["detected_symptoms"]) ? implode(", ", $data["detected_symptoms"]) : "";
$predicted_disease = $data["predicted_disease"] ?? "";
$confidence_score = isset($data["confidence_score"]) ? (float)$data["confidence_score"] : 0;
$severity_level = $data["severity_level"] ?? "";
$severity_score = isset($data["severity_score"]) ? (int)$data["severity_score"] : 0;
$recommended_doctor = $data["recommended_doctor"] ?? "";
$duration_days = isset($data["duration_days"]) ? (int)$data["duration_days"] : 0;

$sql = "INSERT INTO predictions 
(user_id, input_text, detected_symptoms, predicted_disease, confidence_score, severity_level, severity_score, recommended_doctor, duration_days)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);

if (!$stmt) {
    echo json_encode([
        "success" => false,
        "message" => "Prepare failed: " . $conn->error
    ]);
    exit;
}

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

if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "message" => "Prediction saved successfully"
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Insert failed: " . $stmt->error
    ]);
}

$stmt->close();
$conn->close();
