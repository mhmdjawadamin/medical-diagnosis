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
        "message" => "No data received"
    ]);
    exit;
}

$age = !empty($data["age"]) ? (int)$data["age"] : null;
$gender = $data["gender"] ?? null;
$blood_type = $data["blood_type"] ?? null;
$height = !empty($data["height"]) ? (float)$data["height"] : null;
$weight = !empty($data["weight"]) ? (float)$data["weight"] : null;
$allergies = $data["allergies"] ?? null;
$chronic = $data["chronic_diseases"] ?? null;
$medications = $data["medications"] ?? null;
$surgeries = $data["past_surgeries"] ?? null;
$smoking = $data["smoking_status"] ?? null;
$family = $data["family_history"] ?? null;
$emergency = $data["emergency_contact"] ?? null;

$sql = "INSERT INTO patient_health_profile 
(user_id, age, gender, blood_type, height, weight, allergies, chronic_diseases, medications, past_surgeries, smoking_status, family_history, emergency_contact)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);

if (!$stmt) {
    echo json_encode([
        "success" => false,
        "message" => "Prepare failed: " . $conn->error
    ]);
    exit;
}

$stmt->bind_param(
    "iissddsssssss",
    $user_id,
    $age,
    $gender,
    $blood_type,
    $height,
    $weight,
    $allergies,
    $chronic,
    $medications,
    $surgeries,
    $smoking,
    $family,
    $emergency
);

if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "message" => "Profile saved successfully"
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Insert failed: " . $stmt->error
    ]);
}

$stmt->close();
$conn->close();
