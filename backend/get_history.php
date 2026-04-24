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

$sql = "SELECT id, input_text, detected_symptoms, predicted_disease, confidence_score, severity_level, severity_score, recommended_doctor, duration_days, created_at 
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC";

$stmt = $conn->prepare($sql);

if (!$stmt) {
    echo json_encode([
        "success" => false,
        "message" => "Prepare failed: " . $conn->error
    ]);
    exit;
}

$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

$history = [];

while ($row = $result->fetch_assoc()) {
    $history[] = $row;
}

echo json_encode([
    "success" => true,
    "history" => $history
]);

$stmt->close();
$conn->close();
