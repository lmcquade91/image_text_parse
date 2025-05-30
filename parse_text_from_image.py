# parse_rail_fields.py
"""
Script to extract structured key-value pairs from rail images.
"""

import pytesseract
from PIL import Image
import re
import cv2
import numpy as np
import sys

def preprocess_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    # Save the preprocessed image for debugging
    cv2.imwrite('preprocessed.jpg', img_thresh)

    # Convert back to PIL for pytesseract
    return Image.fromarray(img_thresh)

def extract_fields(text):
    """
    Use regex to extract key-value pairs from the OCR text.
    """
    fields = {}
    patterns = {
        "DATE": r"DATE\s*[:\-]?\s*(\S+)",
        "TIME": r"TIME\s*[:\-]?\s*(\S+)",
        "TEMP": r"TEMP\s*[:\-]?\s*(\S+)",
        "WELDER1": r"WELDER ?#?1\s*[:\-]?\s*(\S+)",
        "WELDER2": r"WELDER ?#?2\s*[:\-]?\s*(\S+)",
        "PROFILE": r"PROFILE\s*[:\-]?\s*(\S+)",
        "TRUCK": r"TRUCK ?#?\s*[:\-]?\s*(\S+)",
        "KM": r"KM\s*[:\-]?\s*(\S+)",
        "TAPPING": r"TAPPING\s*[:\-]?\s*(\S+)",
        "WELD": r"WELD ?#?\s*[:\-]?\s*(\S+)",
        "PORTION": r"PORTION ?#?\s*[:\-]?\s*(\S+)",
        "RAIL TYPE": r"RAIL TYPE\s*[:\-]?\s*([\S\s]+?)\s*PEAK"
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            fields[field] = match.group(1).strip()
        else:
            fields[field] = None
    return fields

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_rail_fields.py path/to/image.jpg")
    else:
        image_path = sys.argv[1]

        # Preprocess image
        preprocessed_img = preprocess_image(image_path)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(preprocessed_img, config=custom_config)

        print("\n=== Raw OCR Output ===\n")
        print(text)
        print("\n======================\n")

        # Extract fields
        fields = extract_fields(text)

        print("\n=== Structured Fields ===\n")
        for key, value in fields.items():
            print(f"{key}: {value}")
        print("\n==========================\n")

