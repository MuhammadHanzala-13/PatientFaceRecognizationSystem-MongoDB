import streamlit as st
import requests
from io import BytesIO

API_URL = "http://localhost:8000"

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1e3c72;">Register Patient Biometrics</h1>
    <p style="color: #666;">Enroll facial recognition data for secure identity verification</p>
</div>
""", unsafe_allow_html=True)

# Search Section with Enhanced UI
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
    <h3 style="color: white; margin: 0 0 1rem 0;">🔍 Patient Lookup</h3>
</div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        mr_number = st.text_input(
            "MR Number", 
            placeholder="Enter Patient MR (e.g. PT-0000)", 
            label_visibility="collapsed",
            help="Enter the unique Medical Record Number"
        )
    with col2:
        search_btn = st.button("🔎 Search Patient", use_container_width=True)

if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

if search_btn and mr_number:
    try:
        with st.spinner("🔍 Searching database..."):
            res = requests.get(f"{API_URL}/patient/{mr_number}")
            if res.status_code == 200:
                st.session_state.patient_data = res.json()
                st.success("✅ Patient found!")
            else:
                st.error("❌ Patient not found in the database. Please add them first.")
                st.session_state.patient_data = None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to server. Please check your connection or server status.")

# Display Patient Data with Card Design
if st.session_state.patient_data:
    p = st.session_state.patient_data
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Patient Info Card
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 1.5rem; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 2rem;">
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Patient Details")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"**Name:** {p['name']}")
    with col_b:
        st.markdown(f"**MR Number:** `{p['mrNumber']}`")
    with col_c:
        if p['has_face']:
            st.markdown("**Status:** :green[✓ Biometrics Registered]")
        else:
            st.markdown("**Status:** :red[✗ Biometrics Missing]")
    
    st.markdown("</div>", unsafe_allow_html=True)

    if p['has_face']:
        st.warning("⚠️ This patient already has registered biometrics. Re-enrolling will overwrite the existing data.")

    # Enrollment Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">📸 Biometric Enrollment</h3>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Position face in center, ensure good lighting, and look directly at camera
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if p['has_face']:
        st.info("ℹ️ Re-enrollment available if biometric update is required")
    
    img_buffer = st.camera_input("📷 Capture Face", help="Ensure proper lighting and face alignment")
    
    if img_buffer is not None:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("💾 Save Face Data", use_container_width=True):
                with st.spinner("🔄 Processing image and extracting biometric features..."):
                    try:
                        files = {"file": ("face.jpg", img_buffer, "image/jpeg")}
                        data = {"mr_number": p['mrNumber']}
                        res = requests.post(f"{API_URL}/register", data=data, files=files)
                        
                        if res.status_code == 200:
                            st.success("✅ Face Registered Successfully!")
                            st.balloons()
                            st.session_state.patient_data["has_face"] = True 
                        else:
                            err = res.json().get('detail', 'Unknown error')
                            st.error(f"❌ Registration Failed: {err}")
                    except Exception as e:
                        st.error(f"⚠️ An error occurred: {e}")
