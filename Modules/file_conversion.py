from PIL import Image


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


convert_file = {
    ('png', 'jpeg'): convert_png_to_jpeg,
    ('png', 'gif'): convert_png_to_gif,
    ('jpeg', 'png'): convert_jpeg_to_png,
    ('jpeg', 'gif'): convert_jpeg_to_gif,
    ('gif', 'png'): convert_gif_to_png,
    ('gif', 'jpeg'): convert_gif_to_jpeg,
}
