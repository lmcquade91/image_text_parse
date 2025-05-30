# parse_text_from_image.py
"""
This script allows the user to select an image file and extract the text from it.
It uses pytesseract for OCR and Pillow for image handling.

Dependencies:
- pytesseract
- pillow

To install the dependencies, run:
    pip install pytesseract pillow

Make sure Tesseract is installed on your machine:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

Usage:
    python parse_text_from_image.py path/to/image.jpg

"""

import sys
import pytesseract
from PIL import Image

def parse_text(image_path):
    try:
        # Open the image file
        img = Image.open(image_path)

        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        # Print the parsed text
        print("\n=== Parsed Text ===\n")
        print(text)
        print("\n===================\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_text_from_image.py path/to/image.jpg")
    else:
        image_path = sys.argv[1]
        parse_text(image_path)

