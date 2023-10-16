from flask import Flask, request, render_template, send_file, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

# Import custom modules from the "Modules" folder
from Modules import merge_pdfs, watermark_pdfs, image_editor, split_pdf, file_compression, ocr, file_conversion, image_cropping, feedback_support

app = Flask(__name__)
app.static_folder = 'static'


# Create directories if they don't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
if not os.path.exists('downloads'):
    os.makedirs('downloads')


@app.route('/')
def main():
    return render_template('main.html')

# this is the route to function on main page in navbar


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

    # If it's a GET request, render the merge.html template
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

                # Call the split_pdf function to split the PDF
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

            # Get the compression level from the form
            compression_level = int(request.form['compression_level'])

            # Call the compression function from the file_compression module
            compressed_file = file_compression.compress(
                file_path, compression_level)

            if compressed_file:
                # Provide the compressed file to the template
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


# OCR (Optical Character Recognition) route
@app.route('/perform_ocr', methods=['GET', 'POST'])
def perform_ocr_route():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                # Save the uploaded image
                image_path = os.path.join('uploads', image_file.filename)
                image_file.save(image_path)

                language = request.form.get('language', 'eng')
                threshold = int(request.form.get('threshold', 128))
                segmentation_mode = int(
                    request.form.get('segmentation_mode', 6))

                text = perform_ocr(image_path, language,
                                   threshold, segmentation_mode)

                return render_template('ocr.html', ocr_result=text)

    return render_template('ocr.html', ocr_result=None)


# image Conversion route
@app.route('/convert_to_png', methods=['POST'])
def convert_to_png_route():
    if 'input_file' in request.files:
        input_file = request.files['input_file']
        if input_file.filename != '':
            output_file_path = os.path.join('downloads', 'converted_image.png')

            # Call the conversion function
            success = file_conversion.convert_to_png(
                input_file, output_file_path)

            if success:
                return send_from_directory('downloads', 'converted_image.png')
            else:
                return "Conversion failed", 400

# Undo Route


@app.route('/undo', methods=['POST'])
def undo_route():
    # Call the undo function
    undo_success = undo_redo.perform_undo()

    if undo_success:
        return "Undo successful"
    else:
        return "Undo failed", 400

# Redo Route


@app.route('/redo', methods=['POST'])
def redo_route():
    # Call the redo function
    redo_success = undo_redo.perform_redo()

    if redo_success:
        return "Redo successful"
    else:
        return "Redo failed", 400

# Image Cropping Route


@app.route('/crop_image', methods=['POST'])
def crop_image_route():
    if 'input_file' in request.files:
        input_file = request.files['input_file']
        if input_file.filename != '':
            output_file_path = os.path.join('downloads', 'cropped_image.png')

            # Get cropping coordinates from the form
            x1 = int(request.form['x1'])
            y1 = int(request.form['y1'])
            x2 = int(request.form['x2'])
            y2 = int(request.form['y2'])

            # Call the cropping function
            success = image_cropping.crop_image(
                input_file, output_file_path, (x1, y1, x2, y2))

            if success:
                return send_from_directory('downloads', 'cropped_image.png')
            else:
                return "Cropping failed", 400

# Feedback Route


@app.route('/store_feedback', methods=['POST'])
def store_feedback_route():
    feedback = request.form['feedback']

    # Call the function to store feedback
    feedback_data = feedback_support.store_feedback(feedback)

    return jsonify({"feedback_data": feedback_data})


if __name__ == '__main__':
    app.run(debug=True)
