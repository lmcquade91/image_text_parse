# app.py
"""
Streamlit Image Text Parser App
This app lets users upload an image, extracts the text using pytesseract, and displays it.
"""

import streamlit as st
from PIL import Image
import pytesseract

# Set the title of the app
st.title("🖼️ Image Text Parser")

# Description / instructions
st.write("""
Upload an image (JPEG, PNG, etc.), and this app will use **OCR (pytesseract)** to extract any text it can find!
""")

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


    # OCR processing
    st.write("Parsing text from image... 🕵️‍♂️")
    text = pytesseract.image_to_string(image)

    # Display the extracted text
    st.subheader("Parsed Text:")
    st.text_area("Extracted Text", text, height=200)

    # Optional: Download button to save the text as a .txt file
    st.download_button(
        label="Download Extracted Text",
        data=text,
        file_name="parsed_text.txt",
        mime="text/plain"
    )

else:
    st.info("Please upload an image to get started.")

# Footer
st.markdown("""
---
Created with ❤️ using Streamlit and pytesseract.
""")
