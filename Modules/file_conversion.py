from PIL import Image

# Convert from PNG to other formats


def convert_png_to_jpeg(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'JPEG')
        return True
    except Exception as e:
        return str(e)


def convert_png_to_gif(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'GIF')
        return True
    except Exception as e:
        return str(e)

# Convert from JPEG to other formats


def convert_jpeg_to_png(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'PNG')
        return True
    except Exception as e:
        return str(e)


def convert_jpeg_to_gif(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'GIF')
        return True
    except Exception as e:
        return str(e)

# Convert from GIF to other formats


def convert_gif_to_png(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'PNG')
        return True
    except Exception as e:
        return str(e)


def convert_gif_to_jpeg(input_file, output_file):
    try:
        img = Image.open(input_file)
        img.save(output_file, 'JPEG')
        return True
    except Exception as e:
        return str(e)
