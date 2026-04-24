<?php
header("Content-Type: application/json");
require_once "db.php";

$data = json_decode(file_get_contents("php://input"), true);

if (
    !$data ||
    !isset($data["full_name"]) ||
    !isset($data["email"]) ||
    !isset($data["phone"]) ||
    !isset($data["password"])
) {
    echo json_encode(["success" => false, "message" => "Missing required fields."]);
    exit;
}

$full_name = trim($data["full_name"]);
$email = trim($data["email"]);
$phone = trim($data["phone"]);
$password = $data["password"];

if ($full_name === "" || $email === "" || $phone === "" || $password === "") {
    echo json_encode(["success" => false, "message" => "All fields are required."]);
    exit;
}

$check_sql = "SELECT id FROM users WHERE email = ?";
$check_stmt = $conn->prepare($check_sql);
$check_stmt->bind_param("s", $email);
$check_stmt->execute();
$check_stmt->store_result();

if ($check_stmt->num_rows > 0) {
    echo json_encode(["success" => false, "message" => "Email already exists."]);
    exit;
}

$hashed_password = password_hash($password, PASSWORD_DEFAULT);

$sql = "INSERT INTO users (full_name, email, phone, password) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssss", $full_name, $email, $phone, $hashed_password);

if ($stmt->execute()) {
    echo json_encode(["success" => true, "message" => "Registration successful."]);
} else {
    echo json_encode(["success" => false, "message" => "Registration failed."]);
}

$stmt->close();
$check_stmt->close();
$conn->close();
