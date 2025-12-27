import streamlit as st

st.set_page_config(
    page_title="Patients FaceID Verification",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    h1 {
        color: #2c3e50;
    }
    h2, h3 {
        color: #34495e;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("Patient Identity Verification System")

with st.container():
    st.markdown("### Welcome")
    st.markdown("""
    This system provides a secure and efficient way to verify patient identities using facial recognition technology.
    Designed for clinical environments, it ensures quick retrieval of patient records and prevents identity fraud.
    """)

with st.expander("System Capabilities", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Core Features**
        *   **Patient Registration**: comprehensive demographic data entry.
        *   **Biometric Enrollment**: Secure facial embedding storage.
        *   **Real-time Recognition**: Instant identity verification via webcam.
        """)
    with col2:
        st.markdown("""
        **Technical Specs**
        *   **Privacy**: Vector-based storage (no raw images saved).
        *   **Performance**: Optimized for CPU inference.
        *   **Database**: Encrypted MongoDB Atlas storage.
        """)

st.markdown("---")
st.markdown("Select a module from the sidebar to begin.")
