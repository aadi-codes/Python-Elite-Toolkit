from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def edit_image(input_image, operation, parameters):
    img = Image.open(input_image)

    if operation == "resize":
        size = parameters.get("size", (800, 600))
        img.thumbnail(size)
    elif operation == "rotate":
        degrees = parameters.get("degrees", 0)
        img = img.rotate(degrees)
    elif operation == "sharpen":
        img = img.filter(ImageFilter.SHARPEN)
    elif operation == "brightness":
        factor = parameters.get("factor", 1.0)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(factor)
    elif operation == "contrast":
        factor = parameters.get("factor", 1.0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(factor)
    elif operation == "grayscale":
        img = img.convert("L")
    elif operation == "horizontal_flip":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif operation == "vertical_flip":
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif operation == "sepia_filter":
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
    elif operation == "grayscale_with_custom_threshold":
        threshold = parameters.get("threshold", 128)
        img = img.convert("L")
        img = img.point(lambda x: 0 if x < threshold else 255, "1")
    elif operation == "invert_colors":
        img = ImageOps.invert(img)

    edited_image_path = "downloads/edited_image.png"
    img.save(edited_image_path)
    return edited_image_path
