import streamlit as st
import requests
from io import BytesIO

API_URL = "http://localhost:8000"

st.header("📝 Register Patient Face")

mr_number = st.text_input("Enter Patient MR Number", placeholder="E.g. MR-2024-001")

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

if st.button("Lookup Patient"):
    if mr_number:
        try:
            res = requests.get(f"{API_URL}/patient/{mr_number}")
            if res.status_code == 200:
                st.session_state.patient_data = res.json()
                st.success(f"Found: {st.session_state.patient_data['name']}")
            else:
                st.error("Patient not found.")
                st.session_state.patient_data = None
        except requests.exceptions.ConnectionError:
            st.error("Backend seems down. Please ensure FastAPI is running.")
            
if st.session_state.patient_data:
    p = st.session_state.patient_data
    st.info(f"Registering for: **{p['name']}** (MR: {p['mrNumber']})")
    
    if p['has_face']:
        st.warning("⚠️ This patient already has a registered face. Overwriting will replace the old embedding.")
    
    img_buffer = st.camera_input("Capture Face")
    
    if img_buffer is not None:
        if st.button("Save Face Biometrics"):
            with st.spinner("Processing & Registering..."):
                try:
                    files = {"file": ("face.jpg", img_buffer, "image/jpeg")}
                    data = {"mr_number": p['mrNumber']}
                    res = requests.post(f"{API_URL}/register", data=data, files=files)
                    
                    if res.status_code == 200:
                        st.success("✅ Face Registered Successfully!")
                        st.session_state.patient_data["has_face"] = True # Update local state
                    else:
                        err = res.json().get('detail', 'Unknown error')
                        st.error(f"Registration Failed: {err}")
                except Exception as e:
                    st.error(f"Error: {e}")

