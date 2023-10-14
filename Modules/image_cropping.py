# image_cropping.py
from PIL import Image


def crop_image(input_file, output_file, coordinates):
    try:
        img = Image.open(input_file)
        cropped = img.crop(coordinates)
        cropped.save(output_file)
        return True
    except Exception as e:
        return str(e)
