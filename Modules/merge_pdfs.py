from PyPDF2 import PdfFileMerger


def merge_pdfs(pdf_files):
    merger = PdfFileMerger()
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    return merger
