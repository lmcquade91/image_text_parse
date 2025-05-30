# app.py

import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract

# Title
st.title("Rail Track Text Parser 🚂")

# Description
st.write("""
Upload an image of rail text (chalk/paint marker on metal) and extract the text using OCR.
This app uses OpenCV preprocessing to improve text detection.
""")

# File uploader
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

def preprocess_image_for_rail_text(pil_image):
    """
    Preprocess the image to make painted/printed rail text clearer for OCR.
    """
    # Convert PIL image to OpenCV
    img = np.array(pil_image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Apply adaptive thresholding
    img_thresh = cv2.adaptiveThreshold(
        img_gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
        15, 10
    )

    # Convert back to PIL for pytesseract
    return Image.fromarray(img_thresh)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Preprocess
    st.write("🔧 Preprocessing image...")
    preprocessed_img = preprocess_image_for_rail_text(image)
    st.image(preprocessed_img, caption="Preprocessed Image", use_container_width=True)

    # OCR
    st.write("🕵️ Parsing text from image...")
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)

    # Display extracted text
    st.subheader("Parsed Text:")
    st.text_area("Extracted Text", text, height=200)

    # Optional: Download button for the text
    st.download_button(
        label="Download Extracted Text",
        data=text,
        file_name="rail_text.txt",
        mime="text/plain"
    )

else:
    st.info("Please upload an image to begin.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by [Your Name].")

