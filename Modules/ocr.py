import pytesseract
from PIL import Image


def perform_ocr(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return str(e)


def perform_ocr_with_language(image_path, language='eng'):
    try:
        text = pytesseract.image_to_string(
            Image.open(image_path), lang=language)
        return text
    except Exception as e:
        return str(e)


def perform_ocr_with_threshold(image_path, threshold=128):
    try:
        image = Image.open(image_path)
        image = image.convert('L')  # Convert to grayscale
        image = image.point(lambda p: p > threshold and 255)  # Apply threshold
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)


def perform_ocr_with_language_and_threshold(image_path, language='eng', threshold=128):
    try:
        image = Image.open(image_path)
        image = image.convert('L')  # Convert to grayscale
        image = image.point(lambda p: p > threshold and 255)  # Apply threshold
        text = pytesseract.image_to_string(image, lang=language)
        return text
    except Exception as e:
        return str(e)


def perform_ocr_with_page_segmentation(image_path, segmentation_mode=6):
    try:
        text = pytesseract.image_to_string(Image.open(
            image_path), config=f'--psm {segmentation_mode}')
        return text
    except Exception as e:
        return str(e)
