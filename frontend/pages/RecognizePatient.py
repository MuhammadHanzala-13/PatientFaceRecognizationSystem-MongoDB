import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1e3c72;">Patient Recognition</h1>
    <p style="color: #666;">Real-time biometric identity verification</p>
</div>
""", unsafe_allow_html=True)

# Instructions Card
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; color: white;">
    <h3 style="color: white; margin: 0 0 1rem 0;">📋 Verification Guidelines</h3>
    <ul style="margin: 0; padding-left: 1.5rem;">
        <li>Position face in the center of the frame</li>
        <li>Ensure adequate front lighting (avoid backlighting)</li>
        <li>Look directly at the camera</li>
        <li>Remove glasses or masks if possible</li>
        <li>Only one person should be visible</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 1rem; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    img_buffer = st.camera_input("📸 Scan Face", help="Align face in center of frame")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1.5rem; border-radius: 15px; color: white; height: 100%;">
        <h4 style="color: white; margin: 0 0 1rem 0;">⚡ Quick Tips</h4>
        <p style="font-size: 0.9rem; margin: 0.5rem 0;">
            ✓ Good lighting improves accuracy<br>
            ✓ Face should fill 60-80% of frame<br>
            ✓ Neutral expression works best<br>
            ✓ Hold still for 2-3 seconds
        </p>
    </div>
    """, unsafe_allow_html=True)

if img_buffer is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        verify_btn = st.button("🔐 Verify Identity", use_container_width=True)
    
    if verify_btn:
        with st.spinner("🔄 Analyzing biometric data..."):
            try:
                files = {"file": ("query.jpg", img_buffer, "image/jpeg")}
                res = requests.post(f"{API_URL}/recognize", files=files)
                
                if res.status_code == 200:
                    data = res.json()
                    score = data["similarity_score"]
                    msg = data["message"]
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if "Identity Verified" in msg:
                        # Success Card
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center; color: white;
                                    box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4); margin-bottom: 2rem;">
                            <h2 style="color: white; font-size: 3rem; margin: 0;">✅</h2>
                            <h2 style="color: white; margin: 1rem 0;">MATCH CONFIRMED</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Patient Info Card
                        st.markdown("""
                        <div style="background: white; border-radius: 15px; padding: 2rem; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        """, unsafe_allow_html=True)
                        
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown(f"### {data['name']}")
                            st.markdown(f"**MR Number:** `{data['mr_number']}`")
                        with col_info2:
                            st.metric("Confidence Score", f"{score:.4f}", delta="High Confidence")
                        
                        st.caption(f"ℹ️ {msg}")
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.balloons()
                        
                    else:
                        # Failure Card
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center; color: white;
                                    box-shadow: 0 8px 25px rgba(235, 51, 73, 0.4); margin-bottom: 2rem;">
                            <h2 style="color: white; font-size: 3rem; margin: 0;">❌</h2>
                            <h2 style="color: white; margin: 1rem 0;">NO MATCH FOUND</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div style="background: white; border-radius: 15px; padding: 2rem; 
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**Reason:** {msg}")
                        st.metric("Similarity Score", f"{score:.4f}", delta="Below Threshold", delta_color="inverse")
                        
                        st.info("💡 **Suggestions:** Ensure the patient is registered in the system, improve lighting, or try again.")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    err = res.json().get('detail', 'Unknown error')
                    st.error(f"⚠️ Processing Error: {err}")
            except Exception as e:
                st.error(f"🔌 Connection Error: {e}")
