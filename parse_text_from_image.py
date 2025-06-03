import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Make sure no GPU is visible

import streamlit as st
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch

# Load TrOCR
@st.cache_resource(show_spinner="Loading TrOCR model…")
def load_trocr_model():
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained(
        'microsoft/trocr-base-handwritten',
        device_map="cpu"  # <--- Forcibly load everything on CPU!
    )
    return processor, model

processor, model = load_trocr_model()

st.title("📝 Handwritten OCR Test with TrOCR")
uploaded_file = st.file_uploader("Upload your handwritten image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Extracting handwritten text…"):
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    st.subheader("Extracted Handwritten Text")
    st.write(extracted_text)
