import streamlit as st

st.set_page_config(
    page_title="Clinic FaceID",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Patient Identity Verification")
st.markdown("""
**MVP Release**
This system is designed for low-compute environments to securely verify patient identity.

**Instructions:**
1. Go to **Register Patient** to enroll a patient's face (requires MR Number).
2. Go to **Recognize Patient** to verify identity using the webcam.

**System Status:**
- Running on CPU
- Model: InsightFace Buffalo_S (ResNet50)
- Database: MongoDB Atlas (Vector)
""")

st.sidebar.info("Select a mode above.")
