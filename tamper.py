

from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import cv2
import io
import os
import tempfile



def perform_ela(image_bytes, quality=90):

    original = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        temp_path = tmp.name
        original.save(temp_path, "JPEG", quality=quality)

    resaved = Image.open(temp_path)

    diff = ImageChops.difference(original, resaved)
    enhancer = ImageEnhance.Brightness(diff)
    ela_image = enhancer.enhance(20)

    ela_array = np.array(ela_image)
    brightness_score = ela_array.mean()

    os.remove(temp_path)

    return brightness_score



def blur_score(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    return cv2.Laplacian(img, cv2.CV_64F).var()



def edge_density(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    edges = cv2.Canny(img, 100, 200)

    edge_pixels = np.count_nonzero(edges)
    total_pixels = edges.shape[0] * edges.shape[1]

    return edge_pixels / total_pixels


def exif_check(image_bytes):

    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif = img._getexif()

        if exif is None:
            return False

        return True

    except:
        return False



def noise_variance(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    noise = cv2.Laplacian(img, cv2.CV_64F)

    return np.var(noise)



def resolution_check(image_bytes):

    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size

    if width < 500 or height < 300:
        return False

    return True

def face_region_consistency(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "No face detected"

    x, y, w, h = faces[0]

    face_region = gray[y:y+h, x:x+w]

    card_region = gray

    face_var = np.var(face_region)
    card_var = np.var(card_region)

    diff = abs(face_var - card_var)

    return diff

def lighting_direction(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1)

    gradient = np.mean(np.sqrt(sobelx**2 + sobely**2))

    return gradient

def rectangular_boundary_score(image_bytes):

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    edges = cv2.Canny(img, 100, 200)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100)

    if lines is None:
        return 0

    return len(lines)


def tamper_analysis(image_bytes):

    ela = perform_ela(image_bytes)
    blur = blur_score(image_bytes)
    edges = edge_density(image_bytes)
    noise = noise_variance(image_bytes)

    has_exif = exif_check(image_bytes)
    good_resolution = resolution_check(image_bytes)
    face_consistency = face_region_consistency(image_bytes)
    boundary_lines = rectangular_boundary_score(image_bytes)
    lighting = lighting_direction(image_bytes)

    risk = 0
    findings = []

    
    if ela > 25:
        risk += 40
        findings.append("Compression anomalies detected")

 
    if blur < 100:
        risk += 20
        findings.append("Unusual blur levels")

    if isinstance(face_consistency, (int, float)) and face_consistency > 200:
        risk += 30
        findings.append("Face region inconsistent with document background")

    if boundary_lines > 50:
        risk += 20
        findings.append("Strong rectangular boundaries detected")

    if lighting > 50:
        risk += 10
        findings.append("Lighting gradient unusually high")

    if edges > 0.18:
        risk += 20
        findings.append("Suspicious edge density")


    if not has_exif:
        risk += 10
        findings.append("Missing camera metadata")


    if noise < 5:
        risk += 10
        findings.append("Unnatural smooth regions detected")

    if not good_resolution:
        risk += 10
        findings.append("Unusually low resolution")

    if risk >= 60:
        level = "High"
    elif risk >= 30:
        level = "Medium"
    else:
        level = "Low"

    return {
        "ela_score": round(float(ela), 2),
        "blur_score": round(float(blur), 2),
        "edge_density": round(float(edges), 4),
        "noise_variance": round(float(noise), 2),
        "has_exif_metadata": has_exif,
        "resolution_valid": good_resolution,
        "tamper_risk_score": risk,
        "tamper_risk_level": level,
        "findings": findings
    }