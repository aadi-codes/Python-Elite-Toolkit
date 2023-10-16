import pytesseract
from PIL import Image


def perform_ocr(image_path, language='eng', threshold=128, segmentation_mode=6):
    try:
        image = Image.open(image_path)
        image = image.convert('L')  # Convert to grayscale
        image = image.point(lambda p: p > threshold and 255)  # Apply threshold
        text = pytesseract.image_to_string(
            image, lang=language, config=f'--psm {segmentation_mode}')
        return text
    except Exception as e:
        return str(e)
