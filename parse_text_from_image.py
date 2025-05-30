# rail_text_parser.py

"""
This script preprocesses images of rail text (chalk/paint marker) and parses the text using Tesseract OCR.
"""

import cv2
import numpy as np
from PIL import Image
import pytesseract
import sys

def preprocess_image_for_rail_text(image_path):
    """
    Preprocesses an image for better OCR performance on painted text.
    Returns a PIL image ready for pytesseract.
    """
    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to increase contrast
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
        15, 10
    )

    # Save or display the preprocessed image for debugging
    # cv2.imwrite('preprocessed.jpg', img_thresh)

    # Convert back to PIL for pytesseract
    return Image.fromarray(img_thresh)

def parse_text_from_image(image_path):
    """
    Preprocesses the image and extracts text using pytesseract.
    """
    preprocessed_img = preprocess_image_for_rail_text(image_path)

    # Use Tesseract with custom config
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)

    print("\n=== Parsed Text ===\n")
    print(text)
    print("\n===================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rail_text_parser.py path/to/image.jpg")
    else:
        image_path = sys.argv[1]
        parse_text_from_image(image_path)
