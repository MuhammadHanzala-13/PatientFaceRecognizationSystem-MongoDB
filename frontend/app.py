import streamlit as st
import sys
import os

# Add the current directory to sys.path so we can import styles
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from styles import apply_custom_styles

st.set_page_config(
    page_title="Patient Identity Verification",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark Theme
apply_custom_styles()

# Hero Section
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1>Patient Identity Verification System</h1>
    <p style="font-size: 1.2rem; color: #aaa;">Secure Biometric Authentication for Healthcare</p>
</div>
""", unsafe_allow_html=True)
#  Feature Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="css-card">
        <h2 style="text-align: center;">🔐</h2>
        <h3 style="text-align: center;">Secure</h3>
        <p style="text-align: center; color: #ccc;">Vector-based encryption for privacy</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="css-card">
        <h2 style="text-align: center;">⚡</h2>
        <h3 style="text-align: center;">Fast</h3>
        <p style="text-align: center; color: #ccc;">Real-time recognition < 2s</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="css-card">
        <h2 style="text-align: center;">💻</h2>
        <h3 style="text-align: center;">Efficient</h3>
        <p style="text-align: center; color: #ccc;">Optimized for CPU inference</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# System Specs
with st.expander("System Technical Specifications", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Core Features**")
        st.markdown("- Patient Demographic Management")
        st.markdown("- Facial Biometric Enrollment")
        st.markdown("- Real-time ID Verification")
    with col_b:
        st.markdown("**Tech Stack**")
        st.markdown("- Model: OpenCV SFace (128-d)")
        st.markdown("- Database: MongoDB Atlas vector search")
        st.markdown("- Embedding for storing face features")
        st.markdown("- UI: Streamlit Dark Mode")

st.markdown("<div style='text-align: center; padding: 2rem; color: #666;'>Please Action for Register & Recognize Patient Face</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; padding: 2rem; color: #666;'>Developed by Muhammad Hanzala Saylani's AI Dev Team</div>", unsafe_allow_html=True)
