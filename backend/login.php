<?php
session_start();
header("Content-Type: application/json");
require_once "db.php";

$data = json_decode(file_get_contents("php://input"), true);

if (
    !$data ||
    !isset($data["email"]) ||
    !isset($data["password"])
) {
    echo json_encode([
        "success" => false,
        "message" => "Missing email or password."
    ]);
    exit;
}

$email = trim($data["email"]);
$password = $data["password"];

if ($email === "" || $password === "") {
    echo json_encode([
        "success" => false,
        "message" => "All fields are required."
    ]);
    exit;
}

$sql = "SELECT id, full_name, email, password FROM users WHERE email = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 1) {
    $user = $result->fetch_assoc();

    if (password_verify($password, $user["password"])) {
        $_SESSION["user_id"] = $user["id"];
        $_SESSION["full_name"] = $user["full_name"];
        $_SESSION["email"] = $user["email"];

        echo json_encode([
            "success" => true,
            "message" => "Login successful.",
            "user_id" => $user["id"],
            "full_name" => $user["full_name"]
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "message" => "Invalid password."
        ]);
    }
} else {
    echo json_encode([
        "success" => false,
        "message" => "Email not found."
    ]);
}

$stmt->close();
$conn->close();
