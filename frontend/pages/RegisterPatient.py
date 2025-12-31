import streamlit as st
import requests
import sys
import os

# Add parent directory to path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles import apply_custom_styles

API_URL = "http://localhost:8000"

apply_custom_styles()

st.header("Patient Registration (Biometric)")
st.markdown("Link a face to an existing patient record.")

# 1. Search Patient
mr_number = st.text_input("Enter MR Number", placeholder="e.g. PT-1001")

if mr_number:
    if st.button("Search Patient"):
        try:
            res = requests.get(f"{API_URL}/patient/{mr_number}")
            if res.status_code == 200:
                patient = res.json()
                st.session_state["patient_data"] = patient
                st.session_state["verification_passed"] = False  # Reset
                st.rerun()
            else:
                st.error("Patient Not Found")
        except:
            st.error("Connection Error")

# 2. Display Result & Handle Logic
if "patient_data" in st.session_state:
    p = st.session_state["patient_data"]
    
    # Card Display
    st.markdown(f"""
    <div style="background-color: #1E1E1E; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="margin:0; color: #4CAF50;">{p['name']}</h3>
        <p style="margin:0; color: #aaa;">MR: {p['mrNumber']}</p>
        <p style="margin:0; color: #aaa;">Status: { "✅ Biometric Registered" if p['has_face'] else "❌ Not Registered" }</p>
    </div>
    """, unsafe_allow_html=True)

    # LOGIC: Check if update is allowed
    allow_upload = False
    
    if not p['has_face']:
        # Case A: New Registration -> Direct Access
        allow_upload = True
        st.info("Ready for new registration.")
        
    else:
        # Case B: Already Registered -> Security Check
        if not st.session_state.get("verification_passed", False):
            st.warning("⚠️ Biometric already registered!")
            st.markdown("**To update, please verify Patient CNIC:**")
            
            cnic_input = st.text_input("Enter CNIC for Validation")
            
            if st.button("Verify CNIC"):
                # Backend returns 'cnic' in lookup_patient, so we can verify securely here.
                stored_cnic = p.get('cnic', '')
                
                if cnic_input.strip() == stored_cnic.strip():
                     st.success("✅ Identity Verified! Update Unlocked.")
                     st.session_state["verification_passed"] = True
                     st.rerun()
                else:
                     st.error(f"❌ CNIC Mismatch! Entered: {cnic_input}")
        else:
            allow_upload = True
            st.warning("⚠️ UPDATE MODE ENABLED")

    # 3. Camera & Upload
    if allow_upload:
        img_buffer = st.camera_input("Capture Face", label_visibility="collapsed")
        
        if img_buffer and st.button("Register / Update Face"):
            try:
                # Prepare Data
                files = {"file": ("face.jpg", img_buffer, "image/jpeg")}
                data = {"mr_number": p['mrNumber']}
                
                res = requests.post(f"{API_URL}/register", data=data, files=files)
                
                if res.status_code == 200:
                    st.success("✅ Successfully Registered!")
                    st.session_state["patient_data"]['has_face'] = True # Update local state
                    st.session_state["verification_passed"] = False # Reset
                    st.rerun()
                else:
                    st.error(f"Error: {res.json().get('detail')}")
                    
            except Exception as e:
                st.error(f"Connection Failed: {e}")
