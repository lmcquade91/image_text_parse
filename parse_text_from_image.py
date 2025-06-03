import os
import io
import base64
import pandas as pd
from io import BytesIO
from PIL import Image
import streamlit as st
from google.cloud import vision

# 🔵 Load the Google Vision API credentials from Streamlit secrets
gcp_creds = st.secrets["google"]["credentials"]

# Save to a file for the Google Vision client
with open("gcp_credentials.json", "w") as f:
    f.write(gcp_creds)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_credentials.json"

# 🔵 Initialize Google Vision API client
client = vision.ImageAnnotatorClient()

# 🟢 Helper function to parse extracted text into form fields
def parse_extracted_text(extracted_text):
    fields = {
        "DATE": "",
        "TIME": "",
        "TEMP": "",
        "WELDER1": "",
        "WELDER2": "",
        "PROFILE": "",
        "TRUCK": "",
        "KM": "",
        "TAPPING": "",
        "WELD": "",
        "PORTION": "",
        "RAIL TYPE": ""
    }
    for line in extracted_text.split("\n"):
        for key in fields.keys():
            if line.upper().startswith(key):
                value = line.split(":", 1)[-1].strip()
                fields[key] = value
                break
    return fields

# 🟡 Streamlit app
st.title("🚂 Rail Text Field Entry & Handwritten OCR (Google Vision API)")

uploaded_file = st.file_uploader("Upload a handwritten image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Show the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Use Google Vision API to extract handwritten text
    with st.spinner("Extracting handwritten text…"):
        image_bytes = uploaded_file.read()
        gcv_image = vision.Image(content=image_bytes)
        response = client.document_text_detection(image=gcv_image)
        extracted_text = response.full_text_annotation.text

    st.subheader("📝 Extracted Handwritten Text")
    st.write(extracted_text)

    # Parse extracted text into form fields
    parsed_fields = parse_extracted_text(extracted_text)

    # 🔵 Editable form
    with st.form("rail_info_form"):
        st.subheader("Enter / Confirm Rail Info")
        date = st.text_input("DATE", value=parsed_fields["DATE"])
        time_val = st.text_input("TIME", value=parsed_fields["TIME"])
        temp = st.text_input("TEMP", value=parsed_fields["TEMP"])
        welder1 = st.text_input("WELDER1", value=parsed_fields["WELDER1"])
        welder2 = st.text_input("WELDER2", value=parsed_fields["WELDER2"])
        profile = st.text_input("PROFILE", value=parsed_fields["PROFILE"])
        truck = st.text_input("TRUCK", value=parsed_fields["TRUCK"])
        km = st.text_input("KM", value=parsed_fields["KM"])
        tapping = st.text_input("TAPPING", value=parsed_fields["TAPPING"])
        weld = st.text_input("WELD", value=parsed_fields["WELD"])
        portion = st.text_input("PORTION", value=parsed_fields["PORTION"])
        rail_type = st.text_input("RAIL TYPE", value=parsed_fields["RAIL TYPE"])
        extracted_text_field = st.text_area("Full Extracted Text (editable)", extracted_text)

        submitted = st.form_submit_button("Save to Excel")

        if submitted:
            # Create DataFrame with form data
            data = {
                "DATE": [date],
                "TIME": [time_val],
                "TEMP": [temp],
                "WELDER1": [welder1],
                "WELDER2": [welder2],
                "PROFILE": [profile],
                "TRUCK": [truck],
                "KM": [km],
                "TAPPING": [tapping],
                "WELD": [weld],
                "PORTION": [portion],
                "RAIL TYPE": [rail_type],
                "Extracted Text": [extracted_text_field]
            }
            df = pd.DataFrame(data)

            # Save to Excel
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Rail Data")
            excel_data = excel_buffer.getvalue()

            # Create download link
            b64 = base64.b64encode(excel_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="rail_data.xlsx">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)

