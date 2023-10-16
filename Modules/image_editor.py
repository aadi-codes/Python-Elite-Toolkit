from PIL import Image, ImageFilter, ImageEnhance, ImageOps


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


def apply_sepia_filter(input_image, output_image):
    img = Image.open(input_image)
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255
            pixels[px, py] = (tr, tg, tb)

    img.save(output_image)


def grayscale_with_custom_threshold(input_image, output_image, threshold=128):
    img = Image.open(input_image)
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < threshold else 255, "1")
    img.save(output_image)


def invert_colors(input_image, output_image):
    img = Image.open(input_image)
    img = ImageOps.invert(img)
    img.save(output_image)
