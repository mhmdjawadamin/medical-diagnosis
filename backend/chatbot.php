<?php
header("Content-Type: application/json");

$data = json_decode(file_get_contents("php://input"), true);

if (!$data || !isset($data["message"])) {
    echo json_encode(["error" => "Missing message"]);
    exit;
}

$url = "http://127.0.0.1:5000/chatbot";

$options = [
    "http" => [
        "header" => "Content-Type: application/json\r\n",
        "method" => "POST",
        "content" => json_encode($data),
        "ignore_errors" => true
    ]
];

$context = stream_context_create($options);
$result = @file_get_contents($url, false, $context);

if ($result === FALSE) {
    echo json_encode(["error" => "Failed to connect to chatbot API"]);
    exit;
}

echo $result;
