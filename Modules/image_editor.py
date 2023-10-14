# image_editor.py
from PIL import Image, ImageFilter, ImageEnhance


def resize_image(input_image, output_image, size):
    img = Image.open(input_image)
    img.thumbnail(size)
    img.save(output_image)


def rotate_image(input_image, output_image, degrees):
    img = Image.open(input_image)
    img = img.rotate(degrees)
    img.save(output_image)


def sharpen_image(input_image, output_image):
    img = Image.open(input_image)
    sharpened = img.filter(ImageFilter.SHARPEN)
    sharpened.save(output_image)


def enhance_brightness(input_image, output_image, factor):
    img = Image.open(input_image)
    enhancer = ImageEnhance.Brightness(img)
    enhanced = enhancer.enhance(factor)
    enhanced.save(output_image)


def enhance_contrast(input_image, output_image, factor):
    img = Image.open(input_image)
    enhancer = ImageEnhance.Contrast(img)
    enhanced = enhancer.enhance(factor)
    enhanced.save(output_image)


def grayscale_image(input_image, output_image):
    img = Image.open(input_image).convert("L")
    img.save(output_image)


def flip_horizontal(input_image, output_image):
    img = Image.open(input_image)
    flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
    flipped.save(output_image)


def flip_vertical(input_image, output_image):
    img = Image.open(input_image)
    flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
    flipped.save(output_image)
