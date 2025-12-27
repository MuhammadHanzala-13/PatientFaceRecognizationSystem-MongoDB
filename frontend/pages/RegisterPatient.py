import streamlit as st
import requests
from io import BytesIO

API_URL = "http://localhost:8000"

st.header("Register Patient Biometrics")
st.markdown("Search for a patient by MR Number to enroll their facial data.")

# Search Section
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        mr_number = st.text_input("MR Number", placeholder="Enter Patient MR (e.g. PT-0000)", label_visibility="collapsed")
    with col2:
        search_btn = st.button("Search Patient")

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

if search_btn and mr_number:
    try:
        with st.spinner("Searching..."):
            res = requests.get(f"{API_URL}/patient/{mr_number}")
            if res.status_code == 200:
                st.session_state.patient_data = res.json()
            else:
                st.error("Patient not found in the database. Please add them first.")
                st.session_state.patient_data = None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Please check your internet connection or server status.")

# Display Patient Data
if st.session_state.patient_data:
    p = st.session_state.patient_data
    
    st.markdown("---")
    st.subheader("Patient Details")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Name:** {p['name']}")
        st.markdown(f"**MR Number:** {p['mrNumber']}")
    with col_b:
        status_color = "red" if not p['has_face'] else "green"
        status_text = "Biometrics Missing" if not p['has_face'] else "Biometrics Registered"
        st.markdown(f"**Status:** :{status_color}[{status_text}]")

    if p['has_face']:
        st.warning("This patient already has a registered face. Enrolling again will overwrite the existing data.")

    st.markdown("### Enrollment")
    st.markdown("*If Need of Enrollment Again*")
    img_buffer = st.camera_input("Capture Face")
    
    if img_buffer is not None:
        if st.button("Save Face Data"):
            with st.spinner("Processing image and extracting features..."):
                try:
                    files = {"file": ("face.jpg", img_buffer, "image/jpeg")}
                    data = {"mr_number": p['mrNumber']}
                    res = requests.post(f"{API_URL}/register", data=data, files=files)
                    
                    if res.status_code == 200:
                        st.success("Face Registered Successfully!")
                        st.session_state.patient_data["has_face"] = True 
                    else:
                        err = res.json().get('detail', 'Unknown error')
                        st.error(f"Registration Failed: {err}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
