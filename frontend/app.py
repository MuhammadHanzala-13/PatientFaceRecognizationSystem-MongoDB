import streamlit as st

st.set_page_config(
    page_title="Patient FaceID Verification",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS for Professional Medical UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Medical Pattern */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(255,255,255,.05) 35px, rgba(255,255,255,.05) 70px);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Content Container with Glassmorphism */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        border-right: 2px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Sidebar Navigation Links */
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 3rem;
    }
    
    [data-testid="stSidebar"] a {
        color: rgba(255, 255, 255, 0.8) !important;
        text-decoration: none;
        padding: 12px 20px;
        margin: 5px 10px;
        border-radius: 10px;
        display: block;
        transition: all 0.3s ease;
        font-weight: 500;
        border-left: 3px solid transparent;
    }
    
    [data-testid="stSidebar"] a:hover {
        background: rgba(255, 255, 255, 0.1);
        color: white !important;
        border-left: 3px solid #4CAF50;
        transform: translateX(5px);
    }
    
    /* Active Page */
    [data-testid="stSidebar"] a[aria-current="page"] {
        background: rgba(76, 175, 80, 0.2);
        color: white !important;
        border-left: 3px solid #4CAF50;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        color: #1e3c72;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2, h3 {
        color: #2a5298;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stDateInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Cards */
    .css-1r6slb0 {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #667eea;
        font-weight: 700;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
        border-radius: 8px;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1);
        border-left: 4px solid #f44336;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: rgba(255, 152, 0, 0.1);
        border-left: 4px solid #ff9800;
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: rgba(33, 150, 243, 0.1);
        border-left: 4px solid #2196F3;
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Camera Input */
    [data-testid="stCameraInput"] {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">Patient Identity Verification System</h1>
    <p style="font-size: 1.2rem; color: #666; font-weight: 300;">Secure Biometric Authentication for Healthcare</p>
</div>
""", unsafe_allow_html=True)

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; color: white;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);">
        <h2 style="color: white; font-size: 2.5rem; margin: 0;">🔐</h2>
        <h3 style="color: white; margin: 1rem 0 0.5rem 0;">Secure</h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
            Vector-based encryption ensures patient privacy
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; color: white;
                box-shadow: 0 8px 20px rgba(245, 87, 108, 0.3);">
        <h2 style="color: white; font-size: 2.5rem; margin: 0;">⚡</h2>
        <h3 style="color: white; margin: 1rem 0 0.5rem 0;">Fast</h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
            Real-time recognition in under 2 seconds
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 2rem; border-radius: 15px; text-align: center; color: white;
                box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3);">
        <h2 style="color: white; font-size: 2.5rem; margin: 0;">💻</h2>
        <h3 style="color: white; margin: 1rem 0 0.5rem 0;">Efficient</h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
            Optimized for low-compute environments
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# System Information
with st.expander("📊 System Technical Specifications", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        **Core Features**
        - Patient demographic management
        - Facial biometric enrollment
        - Real-time identity verification
        - Duplicate prevention system
        """)
    with col_b:
        st.markdown("""
        **Technical Stack**
        - Model: OpenCV SFace (128-dim embeddings)
        - Database: MongoDB Atlas with Vector Search
        - Security: No raw images stored
        - Performance: CPU-optimized inference
        """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Select a module from the sidebar to begin</p>
</div>
""", unsafe_allow_html=True)
