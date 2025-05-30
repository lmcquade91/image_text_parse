# app.py

import streamlit as st
from PIL import Image
import numpy as np
import cv2
import pytesseract

st.title("Rail Track Text Parser 🚂")

st.write("""
Upload an image of rail text (chalk/paint marker on metal) and extract the text using OCR.
This app uses OpenCV to automatically crop to the largest text area and preprocess it for better OCR results.
""")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

def crop_largest_text_area(pil_image):
    """
    Automatically crop the image to the largest contour (assumed to be the text area).
    """
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Threshold to binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # Crop the image to this bounding box
        cropped_img = img[y:y+h, x:x+w]
        return cropped_img
    else:
        return img  # fallback: return original image

def preprocess_image_for_rail_text(pil_image):
    """
    Preprocess the image to make painted/printed rail text clearer for OCR.
    """
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
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Crop to largest text area
    st.write("🔍 Cropping to largest text area...")
    cropped_img = crop_largest_text_area(image)
    st.image(cropped_img, caption="Cropped Image", use_container_width=True)

    # Preprocess
    st.write("🔧 Preprocessing image...")
    preprocessed_img = preprocess_image_for_rail_text(Image.fromarray(cropped_img))
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

