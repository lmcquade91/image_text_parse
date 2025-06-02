# app.py
import streamlit as st
from PIL import Image
from io import BytesIO
import pandas as pd
import piexif
import base64

def extract_gps_from_image(image_file):
    try:
        exif_dict = piexif.load(image_file.info["exif"])
        gps_data = exif_dict.get("GPS", {})

        def get_coord(coord, ref):
            d, m, s = [x[0] / x[1] for x in coord]
            result = d + (m / 60.0) + (s / 3600.0)
            if ref in ['S', 'W']:
                result = -result
            return result

        if gps_data:
            lat = get_coord(gps_data[piexif.GPSIFD.GPSLatitude], gps_data[piexif.GPSIFD.GPSLatitudeRef].decode())
            lon = get_coord(gps_data[piexif.GPSIFD.GPSLongitude], gps_data[piexif.GPSIFD.GPSLongitudeRef].decode())
            return lat, lon
    except Exception:
        return None, None
    return None, None

st.title("Rail Text Field Entry & Geotag Extraction 🚂")

# Step 1: Upload Image
uploaded_file = st.file_uploader("Upload an image of rail text...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Extract GPS data
    lat, lon = extract_gps_from_image(image)
    if lat and lon:
        st.success(f"GPS Data found! Latitude: {lat}, Longitude: {lon}")
    else:
        st.warning("No GPS data found in the image.")

    # Step 2: Show form for manual entry
    with st.form("rail_info_form"):
        st.subheader("Enter Rail Info (manually if needed)")
        date = st.text_input("DATE")
        time = st.text_input("TIME")
        temp = st.text_input("TEMP")
        welder1 = st.text_input("WELDER1")
        welder2 = st.text_input("WELDER2")
        profile = st.text_input("PROFILE")
        truck = st.text_input("TRUCK")
        km = st.text_input("KM")
        tapping = st.text_input("TAPPING")
        weld = st.text_input("WELD")
        portion = st.text_input("PORTION")
        rail_type = st.text_input("RAIL TYPE")

        submitted = st.form_submit_button("Save to Excel")

        if submitted:
            # Compile data
            data = {
                "DATE": [date],
                "TIME": [time],
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
                "Latitude": [lat],
                "Longitude": [lon]
            }

            df = pd.DataFrame(data)

            # Save to Excel
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Rail Data")
                with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Rail Data")
# No need for writer.save()
excel_data = excel_buffer.getvalue()
            excel_data = excel_buffer.getvalue()

            # Provide download link
            b64 = base64.b64encode(excel_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="rail_data.xlsx">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)

