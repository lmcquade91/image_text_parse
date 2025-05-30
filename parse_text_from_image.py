import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np

st.title("Rail Text OCR Parser 🚂")

uploaded_file = st.file_uploader("Upload an image of rail text...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Preprocess with OpenCV
        img = np.array(image)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_thresh = cv2.adaptiveThreshold(
            img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
        )
        st.image(img_thresh, caption="Preprocessed Image", use_container_width=True)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(Image.fromarray(img_thresh), config=custom_config)

        st.subheader("Raw OCR Output:")
        st.text_area("OCR Text", text, height=200)

        # Parse key-value pairs
        import re
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
            fields[field] = match.group(1).strip() if match else "Not found"

        st.subheader("Parsed Fields:")
        st.json(fields)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
else:
    st.info("Please upload an image to begin parsing.")

