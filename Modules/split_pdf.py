import PyPDF2


def split_pdf(pdf_path, page_range):
    try:
        pdf = PyPDF2.PdfFileReader(open(pdf_path, 'rb'))
        pdf_writer = PyPDF2.PdfFileWriter()

        page_numbers = [int(page) for page in page_range.split('-')]

        if len(page_numbers) != 2:
            return None

        for page_num in range(page_numbers[0] - 1, page_numbers[1]):
            pdf_writer.addPage(pdf.getPage(page_num))

        # Generate an output filename based on the input filename
        output_path = pdf_path.replace('.pdf', '_split.pdf')

        with open(output_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        return output_path
    except Exception as e:
        return str(e)
