# list of required libraries 
required_libraries = {
    "Flask": "2.1.1",
    "Werkzeug": "2.1.1",
    "Pillow": "8.2.0",
    "pytesseract": "0.3.8",
    "pdf2image": "1.15.1",
    "ghostscript": "0.7",
    "img2pdf": "0.4.3",
    "reportlab": "3.5.68",
    "Wand": "0.6.7",
    "numpy": "1.21.1"
}

# Install the required libraries
import pip

for library, version in required_libraries.items():
    try:
        pip.main(["install", f"{library}=={version}"])
    except Exception as e:
        print(f"Failed to install {library} ({version}): {str(e)}")
