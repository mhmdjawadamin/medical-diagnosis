<?php
require_once __DIR__ . '/fpdf/fpdf.php';

$data = json_decode(file_get_contents("php://input"), true);

$pdf = new FPDF();
$pdf->AddPage();

$pdf->SetFont('Arial','B',16);
$pdf->Cell(0,10,'AI Medical Report',0,1);

$pdf->SetFont('Arial','',12);

$pdf->Cell(0,10,'Date: '.date("Y-m-d H:i"),0,1);

$pdf->Cell(0,10,'Predicted Disease: '.$data["predicted_disease"],0,1);
$pdf->Cell(0,10,'Confidence: '.($data["confidence_score"]*100).'%',0,1);
$pdf->Cell(0,10,'Risk Level: '.$data["severity_level"],0,1);
$pdf->Cell(0,10,'Recommended Doctor: '.$data["recommended_doctor"],0,1);

$pdf->Ln(5);

$pdf->MultiCell(0,10,'Symptoms: '.implode(", ", $data["detected_symptoms"]));

$pdf->Ln(5);

$pdf->MultiCell(0,10,'Urgent Guidance: '.$data["urgent_action"]);

$pdf->Output();
?>