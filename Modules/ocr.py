# ocr.py
import pytesseract
from PIL import Image


def perform_ocr(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return str(e)
