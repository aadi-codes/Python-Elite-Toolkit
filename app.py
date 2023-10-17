from flask import Flask, request, render_template, send_file, url_for, jsonify
from werkzeug.utils import secure_filename
import os

# imported custom modules
from Modules import merge_pdfs, watermark_pdfs, image_editor, split_pdf, file_compression, perform_ocr, crop_image, file_conversion, feedback_support

app = Flask(__name__)
app.static_folder = 'static'


# create directories if they don't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('downloads'):
    os.makedirs('downloads')


@app.route('/')
def main():
    return render_template('main.html')


# link to function section from navbar
@app.route('/functions')
def functions():
    return render_template('main.html')


# Merge PDFs route
@app.route('/merge', methods=['GET', 'POST'])
def merge_pdfs_route():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdfs')
        merger = merge_pdfs.merge_pdfs(pdf_files)

        merged_filename = 'merged_pdf.pdf'
        merged_path = os.path.join('downloads', merged_filename)
        merger.write(merged_path)
        merger.close()

        # Provide the merged PDF file path to the template
        merged_pdf = url_for('download', filename=merged_filename)

        return render_template('merge.html', merged_pdf=merged_pdf)

    return render_template('merge.html', merged_pdf=None)


# Watermark PDFs route
@app.route('/watermark', methods=['GET', 'POST'])
def watermark_pdfs_route():
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

            watermark_pdfs.apply_watermark(
                input_pdf_path, watermark_path, output_path)

            watermarked_pdf = url_for('download', filename=output_filename)

            return render_template('watermark.html', watermarked_pdf=watermarked_pdf)

    return render_template('watermark.html', watermarked_pdf=None)


# PDF Splitting route
@app.route('/split_pdf', methods=['GET'])
def render_split_pdf_form():
    return render_template('split_pdf.html', split_output=None)


@app.route('/split_pdf', methods=['POST'])
def pdf_split_route():
    if 'pdf_file' in request.files and 'page_range' in request.form:
        pdf_file = request.files['pdf_file']
        page_range = request.form['page_range']

        if pdf_file and page_range:
            try:
                # Save the uploaded PDF file
                filename = secure_filename(pdf_file.filename)
                pdf_path = os.path.join('uploads', filename)
                pdf_file.save(pdf_path)

                # calling split_pdf function
                output_path = split_pdf(pdf_path, page_range)

                if output_path:
                    return send_file(output_path, as_attachment=True)
                else:
                    return "Invalid page range", 400
            except Exception as e:
                return str(e), 400

    return "Invalid request", 400


# File Compression route
@app.route('/compress', methods=['GET', 'POST'])
def compress_file_route():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Get compression level
            compression_level = int(request.form['compression_level'])

            # Call the compression function
            compressed_file = file_compression.compress(
                file_path, compression_level)

            if compressed_file:
                # Provide the compressed file
                return send_file(compressed_file, as_attachment=True)

    return render_template('compress.html')


# Image Editor route
@app.route('/image_editor', methods=['GET', 'POST'])
def image_editor_route():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                input_image_path = os.path.join('uploads', image_file.filename)
                output_image_path = os.path.join(
                    'downloads', 'edited_image.png')
                image_file.save(input_image_path)

                operation = request.form['operation']

                if operation == "resize":
                    image_editor.resize_image(
                        input_image_path, output_image_path, (800, 600))
                elif operation == "rotate":
                    degrees = int(request.form['degrees'])
                    image_editor.rotate_image(
                        input_image_path, output_image_path, degrees)
                elif operation == "sharpen":
                    image_editor.sharpen_image(
                        input_image_path, output_image_path)
                elif operation == "brightness":
                    factor = float(request.form['factor'])
                    image_editor.enhance_brightness(
                        input_image_path, output_image_path, factor)
                elif operation == "contrast":
                    factor = float(request.form['factor'])
                    image_editor.enhance_contrast(
                        input_image_path, output_image_path, factor)
                elif operation == "grayscale":
                    image_editor.grayscale_image(
                        input_image_path, output_image_path)
                elif operation == "horizontal_flip":
                    image_editor.flip_horizontal(
                        input_image_path, output_image_path)
                elif operation == "vertical_flip":
                    image_editor.flip_vertical(
                        input_image_path, output_image_path)
                elif operation == "sepia_filter":
                    image_editor.apply_sepia_filter(
                        input_image_path, output_image_path)
                elif operation == "custom_threshold":
                    threshold = int(request.form['threshold'])
                    image_editor.grayscale_with_custom_threshold(
                        input_image_path, output_image_path, threshold)
                elif operation == "invert_colors":
                    image_editor.invert_colors(
                        input_image_path, output_image_path)
                else:
                    return "Invalid operation. Supported operations: resize, rotate, sharpen, brightness, contrast, grayscale, horizontal_flip, vertical_flip, sepia_filter, custom_threshold, invert_colors"

                edited_image = url_for('download', filename='edited_image.png')

                return render_template('image_editor.html', edited_image=edited_image)

    return render_template('image_editor.html', edited_image=None)


# OCR route (Optical Character Recognition)
@app.route('/perform_ocr', methods=['GET', 'POST'])
def perform_ocr_route():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                # Save the uploaded image
                image_path = os.path.join('uploads', image_file.filename)
                image_file.save(image_path)

                # get optional parameters
                language = request.form.get('language', 'eng')
                threshold = int(request.form.get('threshold', 128))
                segmentation_mode = int(
                    request.form.get('segmentation_mode', 6))

                # perform OCR and store the result
                ocr_result = perform_ocr(
                    image_path, language, threshold, segmentation_mode)

                return render_template('ocr.html', ocr_result=ocr_result)

    return render_template('ocr.html', ocr_result=None)


# Image Cropping route
@app.route('/crop_image', methods=['GET', 'POST'])
def crop_image_route():
    if 'image_file' in request.files:
        input_file = request.files['image_file']
        if input_file.filename != '':
            # Save the uploaded image
            input_path = os.path.join(
                app.config['UPLOAD_FOLDER'], input_file.filename)
            input_file.save(input_path)

            x = int(request.form.get('x', 0))
            y = int(request.form.get('y', 0))
            width = int(request.form.get('width', 0))
            height = int(request.form.get('height', 0))

            coordinates = (x, y, x + width, y + height)

            output_path = os.path.join(
                app.config['UPLOAD_FOLDER'], 'cropped_' + input_file.filename)

            if crop_image.crop_image(input_path, output_path, coordinates):
                return send_file(output_path, as_attachment=True)

    # if cropping not successful/no image uploaded
    return render_template('crop_image.html', cropping_result='Cropping failed')


# File Conversion route
@app.route('/convert_file', methods=['POST', 'GET'])
def convert_file_route():
    if 'input_file' in request.files:
        input_file = request.files['input_file']
        if input_file.filename != '':
            # Save the uploaded file
            input_path = os.path.join(
                app.config['UPLOAD_FOLDER'], input_file.filename)
            input_file.save(input_path)

            # Get input and output
            input_format = request.form.get('input_format', 'png')
            output_format = request.form.get('output_format', 'png')

            # generate output filename
            output_filename = f'converted_file.{output_format}'

            # output file path
            output_path = os.path.join(
                app.config['UPLOAD_FOLDER'], output_filename)

            # call conversion function
            success = file_conversion.convert_file(
                input_path, output_path, input_format, output_format)

            if success:
                return send_file(output_path, as_attachment=True)

    # if conversion unsuccessful/no file uploaded
    return render_template('conversion.html', conversion_result='Conversion failed')


# Feedback Route
@app.route('/store_feedback', methods=['POST'])
def store_feedback_route():
    feedback = request.form['feedback']

    # call the function
    feedback_data = feedback_support.store_feedback(feedback)

    return jsonify({"feedback_data": feedback_data})


# 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
