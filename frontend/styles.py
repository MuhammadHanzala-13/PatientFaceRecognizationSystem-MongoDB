import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        /* Import a clean Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

        /* Global Styles for Dark Theme */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1A1C24; /* Slightly darker/neutral sidebar */
            border-right: 1px solid #2D303E;
        }
        
        [data-testid="stSidebar"] .css-1d391kg {
            padding-top: 2rem;
        }
        
        /* Sidebar Nav Links */
        [data-testid="stSidebar"] a {
            color: #B0B3B8 !important;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: 400;
            padding: 10px 15px;
            margin: 5px 0;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            border-left: 3px solid transparent;
        }
        
        [data-testid="stSidebar"] a:hover {
            color: #FFFFFF !important;
            background-color: #2D303E;
            border-left: 3px solid #4facfe;
        }
        
        /* Active Page Highlighting workaround (Streamlit 1.10+) */
        [data-testid="stSidebar"] a[aria-current="page"] {
             color: #4facfe !important;
             background-color: rgba(79, 172, 254, 0.1);
             border-left: 3px solid #4facfe;
             font-weight: 500;
        }

        /* Headers */
        h1, h2, h3 {
            color: #FAFAFA !important;
            font-weight: 600;
            font-family: 'Roboto', sans-serif;
        }
        
        p, label {
            color: #E6E6E6 !important;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Block Containers (Cards) */
        .block-container {
            max-width: 1200px;
        }
        
        /* Custom Cards */
        .css-card {
            background-color: #1F2229;
            padding: 2rem;
            border-radius: 8px; /* Slightly tighter radius */
            border: 1px solid #2D303E;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            margin-bottom: 1.5rem;
        }
        
        /* Inputs - Improved Design */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stDateInput>div>div>input,
        .stSelectbox>div>div>select {
            background-color: #13151A; /* Darker input bg */
            color: #FAFAFA;
            border: 1px solid #41444C;
            border-radius: 4px; /* Professional slight roundness */
            padding: 10px 12px;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stDateInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus {
            border-color: #4facfe;
            box-shadow: 0 0 0 1px rgba(79, 172, 254, 0.5);
        }
        
        /* Input Labels */
        .stTextInput label, .stNumberInput label, .stDateInput label, .stSelectbox label {
            font-size: 14px;
            font-weight: 500;
            color: #B0B3B8 !important;
            margin-bottom: 4px;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #4facfe;
            color: #0E1117;
            border: none;
            border-radius: 4px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 24px;
            transition: all 0.2s;
            box-shadow: 0 2px 5px rgba(79, 172, 254, 0.3);
        }
        
        .stButton>button:hover {
            background-color: #00DBDE;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0, 219, 222, 0.4);
        }
        
        .stButton>button:active {
            transform: translateY(0px);
        }
        
        /* Success/Error/Info boxes */
        .stSuccess, .stError, .stInfo, .stWarning {
            background-color: #1F2229;
            color: #FAFAFA;
            border: 1px solid #41444C;
            border-left-width: 4px;
        }
        
        .stSuccess { border-left-color: #00C851; }
        .stError { border-left-color: #ff4444; }
        .stWarning { border-left-color: #ffbb33; }
        .stInfo { border-left-color: #33b5e5; }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #4facfe !important;
            font-weight: 700;
        }
        
        [data-testid="stMetricDelta"] {
            color: #00f2fe !important;
        }
    </style>
    """, unsafe_allow_html=True)
