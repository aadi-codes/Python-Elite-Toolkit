# file_conversion.py
from PIL import Image


def convert_to_png(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'PNG')
        return True
    except Exception as e:
        return str(e)
