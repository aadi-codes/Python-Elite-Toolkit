from flask import Flask, request, render_template, send_file, url_for, send_from_directory
from PIL import Image, ImageEnhance, ImageFilter
import PyPDF2
import sys
import os

app = Flask(__name__)

# Create directories if they don't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('downloads'):
    os.makedirs('downloads')


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/merge', methods=['GET', 'POST'])
def merge_pdfs():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdfs')
        merger = PyPDF2.PdfFileMerger()

        for pdf_file in pdf_files:
            merger.append(pdf_file)

        merged_filename = 'merged_pdf.pdf'
        merged_path = os.path.join('downloads', merged_filename)
        merger.write(merged_path)
        merger.close()

        # Provide the merged PDF file path to the template
        merged_pdf = url_for('download', filename=merged_filename)

        return render_template('merge.html', merged_pdf=merged_pdf)

    # If it's a GET request, render the merge.html template
    return render_template('merge.html', merged_pdf=None)


# ----------------------------------X----------------------------------
# watermark starts here

@app.route('/watermark', methods=['GET', 'POST'])
def watermark_pdfs():
    if request.method == 'POST':
        watermark_file = request.files['watermark']
        input_pdf = request.files['input_pdf']

        if watermark_file and input_pdf:
            watermark_path = 'uploads/' + watermark_file.filename
            input_pdf_path = 'uploads/' + input_pdf.filename

            watermark_file.save(watermark_path)
            input_pdf.save(input_pdf_path)

            output_filename = f'watermarked_{input_pdf.filename}'
            output_path = os.path.join('downloads', output_filename)

            apply_watermark(input_pdf_path, watermark_path, output_path)

            # Provide the watermarked PDF file path to the template
            watermarked_pdf = url_for('download', filename=output_filename)

            return render_template('watermark.html', watermarked_pdf=watermarked_pdf)

    # If it's a GET request, render the watermark.html template
    return render_template('watermark.html', watermarked_pdf=None)


def apply_watermark(super_pdf, watermark_pdf, output_path):
    super_reader = PyPDF2.PdfFileReader(open(super_pdf, 'rb'))
    watermark_reader = PyPDF2.PdfFileReader(open(watermark_pdf, 'rb'))
    output_writer = PyPDF2.PdfFileWriter()

    for page_num in range(super_reader.getNumPages()):
        page = super_reader.getPage(page_num)
        watermark_page = watermark_reader.getPage(0)

        page.mergePage(watermark_page)
        output_writer.addPage(page)

    with open(output_path, 'wb') as output_file:
        output_writer.write(output_file)


# ----------------------------------X----------------------------------
# image ediotor code starts here :)


@app.route('/downloads/<filename>')
def download(filename):
    return send_from_directory('downloads', filename)


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


@app.route('/image_editor', methods=['GET', 'POST'])
def image_editor():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                # Save the uploaded image
                input_image_path = os.path.join('uploads', image_file.filename)
                output_image_path = os.path.join(
                    'downloads', 'edited_image.png')
                image_file.save(input_image_path)

                # Get the selected operation
                operation = request.form['operation']

                # Call the appropriate image editing function based on the operation
                if operation == "resize":
                    resize_image(input_image_path,
                                 output_image_path, (800, 600))
                elif operation == "rotate":
                    rotate_image(input_image_path, output_image_path, 90)
                elif operation == "sharpen":
                    sharpen_image(input_image_path, output_image_path)
                elif operation == "enhance_brightness":
                    enhance_brightness(
                        input_image_path, output_image_path, 1.5)
                elif operation == "enhance_contrast":
                    enhance_contrast(input_image_path, output_image_path, 1.5)
                elif operation == "grayscale":
                    grayscale_image(input_image_path, output_image_path)
                elif operation == "flip_horizontal":
                    flip_horizontal(input_image_path, output_image_path)
                elif operation == "flip_vertical":
                    flip_vertical(input_image_path, output_image_path)
                else:
                    return "Invalid operation. Supported operations: resize, rotate, sharpen, enhance_brightness, enhance_contrast, grayscale, sepia, flip_horizontal, flip_vertical"

                # Provide the edited image path to the template
                edited_image = url_for(
                    'download', filename='edited_image.png')

                return render_template('image_editor.html', edited_image=edited_image)

    return render_template('image_editor.html', edited_image=None)


# error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
