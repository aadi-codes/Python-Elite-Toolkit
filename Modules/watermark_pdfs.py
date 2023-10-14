from PyPDF2 import PdfFileReader, PdfFileWriter


def apply_watermark(super_pdf, watermark_pdf, output_path):
    super_reader = PdfFileReader(open(super_pdf, 'rb'))
    watermark_reader = PdfFileReader(open(watermark_pdf, 'rb'))
    output_writer = PdfFileWriter()

    for page_num in range(super_reader.getNumPages()):
        page = super_reader.getPage(page_num)
        watermark_page = watermark_reader.getPage(0)

        page.mergePage(watermark_page)
        output_writer.addPage(page)

    with open(output_path, 'wb') as output_file:
        output_writer.write(output_file)
