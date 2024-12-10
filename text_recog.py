import easyocr

def text_recog(img):
    # Initialize reader
    reader = easyocr.Reader(['en'])

    # Perform OCR
    results = reader.readtext(img)
    string = ""

    # Print results
    for (bbox, text, confidence) in results:
        string += text + " "

    return string
