from flask import Flask, request, render_template, send_file, url_for, jsonify, flash, redirect
from werkzeug.utils import secure_filename
import os

# imported custom modules
from Modules import merge_pdfs, watermark_pdfs, image_editor, split_pdf, file_compression, perform_ocr, crop_image, file_conversion, feedback_support

app = Flask(__name__)
app.secret_key = 'Aditya@123    '


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


# merge pdf route
@app.route('/merge', methods=['GET', 'POST'])
def merge_pdfs_route():
    if request.method == 'POST':
        pdf_files = request.files.getlist('pdfs')
        merger = merge_pdfs.merge_pdfs(pdf_files)

        try:
            merged_filename = 'merged_pdf.pdf'
            merged_path = os.path.join('downloads', merged_filename)
            merger.write(merged_path)
            merger.close()

            # Flash a success message
            flash("PDFs merged successfully!", 'success')

            # Open a window to save the merged PDF file
            return send_file(merged_path, as_attachment=True)
        except Exception as e:
            # Flash an error message
            flash(f"Error: {str(e)}", 'error')
            return redirect(url_for('merge_pdfs_route'))

    return render_template('merge.html', merged_pdf=None)


# Watermark PDFs route
@app.route('/watermark', methods=['POST', 'GET'])
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

            try:
                watermark_pdfs.apply_watermark(
                    input_pdf_path, watermark_path, output_path)

                # Flash a success message
                flash("PDFs watermarked successfully!", 'success')

                # Open a window to save the watermarked PDF file
                return send_file(output_path, as_attachment=True)

            except Exception as e:
                # Flash an error message if there's an exception
                flash(f"Error: {str(e)}", 'error')

    return render_template('watermark.html', watermark_pdfs=None)


# PDF Splitting route
@app.route('/split_pdf', methods=['POST', 'GET'])
def pdf_split_route():
    if request.method == 'POST':
        if 'pdf_file' in request.files and 'page_range' in request.form:
            pdf_file = request.files['pdf_file']
            page_range = request.form['page_range']

            if pdf_file and page_range:
                try:
                    # Save the uploaded PDF file
                    filename = secure_filename(pdf_file.filename)
                    pdf_path = os.path.join('uploads', filename)
                    pdf_file.save(pdf_path)

                    # Calling the split_pdf function
                    output_path = split_pdf.split_pdf(pdf_path, page_range)

                    if output_path:
                        # Flash a success message
                        flash("PDF split successfully!", 'success')

                        # Open a window to save the split PDF file
                        return send_file(output_path, as_attachment=True)
                    else:
                        # Flash an error message for invalid page range
                        flash("Invalid page range", 'error')
                        return redirect(url_for('pdf_split_route'))
                except Exception as e:
                    # Flash an error message if there's an exception
                    flash(f"Error: {str(e)}", 'error')
                    return redirect(url_for('pdf_split_route'))

    return render_template('split_pdf.html')


# File Compression route
@app.route('/compress', methods=['GET', 'POST'])
def compress_file():
    if request.method == 'POST':
        input_file = request.files['input_file']
        compression_level = request.form['compression_level']

        if input_file:
            # Save the uploaded file to the 'uploads' directory
            filename = secure_filename(input_file.filename)
            file_path = os.path.join('uploads', filename)
            input_file.save(file_path)

            # Call the file_compression function to compress the file
            success, compressed_file_path = file_compression.compress(
                file_path, compression_level)

            if success:
                # Flash a success message and provide the compressed file for download
                flash("File compressed successfully!", 'success')
                return send_file(compressed_file_path, as_attachment=True)

            # If compression fails, flash an error message
            flash("File compression failed. Please try again.", 'error')

    return render_template('compress.html')


# Image Editor route
@app.route('/image_editor', methods=['POST', 'GET'])
def image_editor_route():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                input_image_path = os.path.join('uploads', image_file.filename)
                image_file.save(input_image_path)

                operation = request.form['operation']
                parameters = {}

                if operation == "resize":
                    parameters['size'] = (800, 600)
                elif operation == "rotate":
                    # Default rotation degree 90 degrees
                    parameters['degrees'] = 90
                elif operation == "sharpen":
                    pass
                elif operation == "brightness":
                    parameters['factor'] = 1.5
                elif operation == "contrast":
                    parameters['factor'] = 1.5
                elif operation == "grayscale":
                    pass
                elif operation == "horizontal_flip":
                    pass
                elif operation == "vertical_flip":
                    pass
                elif operation == "sepia_filter":
                    pass
                elif operation == "grayscale_with_custom_threshold":
                    parameters['threshold'] = 128
                elif operation == "invert_colors":
                    pass
                else:
                    return "Invalid operation. Supported operations: resize, rotate, sharpen, brightness, contrast, grayscale, horizontal_flip, vertical_flip, sepia_filter, custom_threshold, invert_colors"

                edited_image_path = image_editor.edit_image(
                    input_image_path, operation, parameters)

                # Flash a success message
                flash("Image editing successful!", 'success')

                # After applying edits to the image, open a window to save it
                return send_file(edited_image_path, as_attachment=True)

    return render_template('image_editor.html')


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

                language = request.form.get('language', 'eng')
                threshold = int(request.form.get('threshold', 128))
                segmentation_mode = int(
                    request.form.get('segmentation_mode', 6))

                # Perform OCR and store the result
                ocr_result = perform_ocr.perform_ocr(
                    image_path, language, threshold, segmentation_mode)

                return render_template('ocr.html', ocr_result=ocr_result)

    return render_template('ocr.html', ocr_result=None)


# Image Cropping route
@app.route('/crop_image', methods=['POST', 'GET'])
def crop_image_route():
    if 'image_file' in request.files:
        input_file = request.files['image_file']
        if input_file.filename != '':
            try:
                # Save the uploaded image
                filename = secure_filename(input_file.filename)
                input_path = os.path.join('uploads', filename)
                input_file.save(input_path)

                x = int(request.form.get('x', 0))
                y = int(request.form.get('y', 0))
                width = int(request.form.get('width', 0))
                height = int(request.form.get('height', 0))

                coordinates = (x, y, x + width, y + height)

                # Modify the output path using the uploaded file's name
                output_path = os.path.join('uploads', 'cropped_' + filename)

                if crop_image.crop_image(input_path, output_path, coordinates):
                    # Flash a success message
                    flash("Image cropping successful!", 'success')
                    return send_file(output_path, as_attachment=True)
                else:
                    # Flash an error message for failed cropping
                    flash("Image cropping failed.", 'error')
            except Exception as e:
                # Flash an error message if there's an exception
                flash(f"Error: {str(e)}", 'error')

    return render_template('crop_image.html')


# File Conversion route
@app.route('/convert_file', methods=['POST', 'GET'])
def convert_file_route():
    if 'input_file' in request.files:
        input_file = request.files['input_file']
        if input_file.filename != '':
            try:
                # Save the uploaded file with a secure filename in the 'uploads' folder
                filename = secure_filename(input_file.filename)
                input_path = os.path.join('uploads', filename)
                input_file.save(input_path)

                # Get input and output formats
                input_format = request.form.get('input_format', 'png')
                output_format = request.form.get('output_format', 'png')

                # Check if the conversion is supported
                if (input_format, output_format) in file_conversion.convert_file:
                    # Generate output filename
                    output_filename = f'converted_file.{output_format}'

                    # Output file path in the 'uploads' folder
                    output_path = os.path.join('uploads', output_filename)

                    # Call the conversion function using the dictionary
                    conversion_function = file_conversion.convert_file[(
                        input_format, output_format)]
                    success = conversion_function(input_path, output_path)

                    if success:
                        # Flash a success message
                        flash("File conversion successful!", 'success')

                        # Open a window to save the converted file
                        return send_file(output_path, as_attachment=True)
                    else:
                        # Flash an error message if the conversion fails
                        flash("File conversion failed", 'error')
                else:
                    flash("Unsupported conversion: {} to {}".format(
                        input_format, output_format), 'error')
            except Exception as e:
                # Flash an error message if there's an exception
                flash(f"Error: {str(e)}", 'error')

    return render_template('conversion.html', ocr_result=None)


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
