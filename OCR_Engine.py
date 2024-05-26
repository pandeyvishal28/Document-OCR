
import pytesseract
import ftfy
import aadhaar_read_data
import pan_read_data


pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


def extract_aadhaar(img_f, img_b):
    
    text_f = pytesseract.image_to_string(img_f, lang='eng')
    text_b = pytesseract.image_to_string(img_b, lang='eng')

    # writing the text of both imag
    text_output = open('output.txt', 'w', encoding='utf-8')
    # text_output.write("Data Of Front Image")
    text_output.write(text_f)

    # text_output.write("Data Of Back Image")
    text_output.write(text_b)

    text_output.close()

    file = open('output.txt', 'r', encoding='utf-8')
    text = file.read()

    # Fixing the Encoding
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    data = aadhaar_read_data.adhaar_read(text)

    return data


def extract_pan(img):
    img_text = pytesseract.image_to_string(img, lang='eng')

    # writing the text of image
    text_output = open('output.txt', 'w', encoding='utf-8')

    text_output.write(img_text)

    text_output.close()

    file = open('output.txt', 'r', encoding='utf-8')
    text = file.read()

    # Fixing the Encoding
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)

    data = pan_read_data.pan_read(text)

    return data
