import streamlit as st
import requests
import sys
import os

# Add parent directory to path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles import apply_custom_styles

API_URL = "http://localhost:8000"

apply_custom_styles()

st.header("ID Verification")
st.markdown("Real-time biometric analysis.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("### Camera Feed")
    img_buffer = st.camera_input("Capture", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("### Analysis Log")
    
    if img_buffer is not None:
        if st.button("Verify Identity", use_container_width=True):
            try:
                files = {"file": ("query.jpg", img_buffer, "image/jpeg")}
                res = requests.post(f"{API_URL}/recognize", files=files)
                
                if res.status_code == 200:
                    data = res.json()
                    score = data["similarity_score"]
                    msg = data["message"]
                    
                    st.metric("Confidence Score", f"{score:.4f}")
                    st.markdown("---")
                    
                    if "Identity Verified" in msg:
                        st.success("MATCH CONFIRMED")
                        st.markdown(f"**Name:** {data['name']}")
                        st.markdown(f"**MR Number:** {data['mr_number']}")
                    else:
                        st.error("NO MATCH FOUND")
                        st.write(f"Reason: {msg}")
                else:
                    try:
                        err_data = res.json()
                        st.error(f"Error: {err_data.get('detail', 'Unknown Error')}")
                    except:
                        st.error(f"Processing Error: {res.status_code}")
            except Exception as e:
                st.error("Connection Error")
    else:
        st.info("Waiting for image input...")
        
    st.markdown('</div>', unsafe_allow_html=True)
