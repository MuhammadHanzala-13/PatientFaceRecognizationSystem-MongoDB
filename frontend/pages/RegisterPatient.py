import streamlit as st
import requests
import sys
import os

# Add parent directory to path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles import apply_custom_styles

API_URL = "http://localhost:8000"

apply_custom_styles()

st.header("Biometric Registration")
st.markdown("Enroll patient facial data for secure identity verification.")

# Search
st.markdown('<div class="css-card">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    mr_number = st.text_input("Search Patient (MR Number)", placeholder="e.g. PT-0000", label_visibility="collapsed")
with col2:
    search_btn = st.button("Search Database", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

if search_btn and mr_number:
    try:
        res = requests.get(f"{API_URL}/patient/{mr_number}")
        if res.status_code == 200:
            st.session_state.patient_data = res.json()
        else:
            st.error("Patient not found.")
            st.session_state.patient_data = None
    except requests.exceptions.ConnectionError:
        st.error("Connection failed.")

# Result
if st.session_state.patient_data:
    p = st.session_state.patient_data
    
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("👤 Patient Details")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Name:** {p['name']}")
        st.write(f"**MR Number:** {p['mrNumber']}")
    with col_b:
        if p['has_face']:
            st.success("Status: Biometrics Registered")
        else:
            st.warning("Status: Biometrics Missing")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📸 Biometric Enrollment")
    img_buffer = st.camera_input("Capture Face")
    
    if img_buffer is not None:
        if st.button("Save Face Data"):
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
                st.error(f"Error: {e}")
