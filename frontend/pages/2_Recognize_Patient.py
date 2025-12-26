import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.header("🔍 Recognize Patient")
st.markdown("Ensure the patient is looking directly at the camera. One person only.")

img_buffer = st.camera_input("Scan Face")

if img_buffer is not None:
    if st.button("Verify Identity"):
        with st.spinner("Analyzing..."):
            try:
                files = {"file": ("query.jpg", img_buffer, "image/jpeg")}
                res = requests.post(f"{API_URL}/recognize", files=files)
                
                if res.status_code == 200:
                    data = res.json()
                    score = data["similarity_score"]
                    msg = data["message"]
                    
                    st.metric("Confidence Score", f"{score:.4f}")
                    
                    if "Identity Verified" in msg:
                        st.success(f"✅ **MATCH CONFIRMED**")
                        st.subheader(f"{data['name']}")
                        st.write(f"MR Number: **{data['mr_number']}**")
                        st.caption(f"Reason: {msg}")
                    else:
                        st.error(f"❌ **NO MATCH FOUND**")
                        st.write(f"Reason: {msg}")
                else:
                    err = res.json().get('detail', 'Unknown error')
                    st.error(f"Processing Error: {err}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
