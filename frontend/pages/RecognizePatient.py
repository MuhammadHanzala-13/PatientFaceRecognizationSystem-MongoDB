import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.header("Patient Recognition")
st.markdown("Ensure the patient is looking directly at the camera with good lighting.")

col1, col2 = st.columns([2, 1])

with col1:
    img_buffer = st.camera_input("Scan Face", help="Align face in center")

with col2:
    st.markdown("### Instructions")
    st.markdown("""
    1. Look straight at the camera.
    2. Ensure no backlighting.
    3. Click 'Verify Identity' to scan.
    """)

if img_buffer is not None:
    if st.button("Verify Identity"):
        with st.spinner("Analyzing biometric data..."):
            try:
                files = {"file": ("query.jpg", img_buffer, "image/jpeg")}
                res = requests.post(f"{API_URL}/recognize", files=files)
                
                if res.status_code == 200:
                    data = res.json()
                    score = data["similarity_score"]
                    msg = data["message"]
                    
                    st.markdown("---")
                    
                    if "Identity Verified" in msg:
                        st.success("MATCH CONFIRMED")
                        
                        # Result Card
                        with st.container():
                            st.markdown(f"## {data['name']}")
                            st.markdown(f"**MR Number:** `{data['mr_number']}`")
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                st.metric("Confidence Score", f"{score:.4f}")
                            with c2:
                                st.caption(f"Verification Note: {msg}")
                    else:
                        st.error("NO MATCH FOUND")
                        st.markdown(f"**Reason:** {msg}")
                        st.metric("Similarity Score", f"{score:.4f}")
                else:
                    err = res.json().get('detail', 'Unknown error')
                    st.error(f"Processing Error: {err}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
