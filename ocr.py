# ocr.py

import pytesseract
import cv2
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_data(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    data = pytesseract.image_to_data(
        img,
        output_type=pytesseract.Output.DICT
    )

    text = " ".join(data["text"])

    return data, text


def confidence_anomaly(data):

    confidences = []

    for c in data["conf"]:
        try:
            c = int(c)
            if c >= 0:
                confidences.append(c)
        except:
            continue

    if len(confidences) == 0:
        return 0

    avg_conf = sum(confidences) / len(confidences)

    return avg_conf



def pattern_anomaly(text):

    findings = []

    # Example ID number pattern
    id_pattern = r"[A-Z]{2}[0-9]{6,10}"

    if not re.search(id_pattern, text):
        findings.append("ID number pattern not detected")

    # Date pattern
    date_pattern = r"\b\d{2}/\d{2}/\d{4}\b"

    if not re.search(date_pattern, text):
        findings.append("Date format not detected")

    return findings


def missing_fields(text):

    keywords = ["name", "dob", "id", "expiry"]

    missing = []

    lower_text = text.lower()

    for k in keywords:
        if k not in lower_text:
            missing.append(k)

    return missing



def character_noise(text):

    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    symbols = sum(not c.isalnum() and not c.isspace() for c in text)

    total = len(text)

    if total == 0:
        return 0

    ratio = symbols / total

    return ratio


def alignment_anomaly(data):

    y_positions = []

    for i, word in enumerate(data["text"]):

        if word.strip() != "":
            y_positions.append(data["top"][i])

    if len(y_positions) < 2:
        return 0

    variance = np.var(y_positions)

    return variance



def analyze_ocr(image_bytes):

    data, text = extract_text_data(image_bytes)

    risk = 0
    findings = []

    avg_conf = confidence_anomaly(data)

    if avg_conf < 70:
        risk += 20
        findings.append("Low OCR confidence detected")

    pattern_findings = pattern_anomaly(text)

    if pattern_findings:
        risk += 20
        findings.extend(pattern_findings)


    missing = missing_fields(text)

    if len(missing) > 2:
        risk += 15
        findings.append("Multiple expected fields missing")

    noise_ratio = character_noise(text)

    if noise_ratio > 0.1:
        risk += 10
        findings.append("High symbol density in text")

    align_var = alignment_anomaly(data)

    if align_var > 500:
        risk += 15
        findings.append("Text alignment anomaly detected")

    if risk >= 60:
        level = "High"
    elif risk >= 30:
        level = "Medium"
    else:
        level = "Low"

    return {
        "ocr_text_sample": text[:200],
        "ocr_confidence_avg": round(avg_conf, 2),
        "ocr_alignment_variance": round(float(align_var), 2),
        "ocr_noise_ratio": round(float(noise_ratio), 3),
        "ocr_risk_score": risk,
        "ocr_risk_level": level,
        "ocr_findings": findings
    }