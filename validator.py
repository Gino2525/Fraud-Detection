

from PIL import Image
import io


def check_magic_bytes(file_bytes):
    header = file_bytes[:8]

    if header.startswith(b'\xff\xd8\xff'):
        return "JPEG"

    if header.startswith(b'\x89PNG\r\n\x1a\n'):
        return "PNG"

    if header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
        return "GIF"

    return "UNKNOWN"


ALLOWED_FORMATS = ["JPEG", "PNG"]

def validate_image(file_bytes):
    real_format = check_magic_bytes(file_bytes)

    if real_format == "UNKNOWN":
        return False, "File is not a valid image"

    if real_format not in ALLOWED_FORMATS:
        return False, f"Unsupported format: {real_format}"

    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()
    except Exception:
        return False, "Image is corrupted or unreadable"

    return True, f"Valid {real_format} image"