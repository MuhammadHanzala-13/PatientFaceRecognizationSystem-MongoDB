import streamlit as st
import requests
from datetime import date
import sys
import os

# Add parent directory to path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from styles import apply_custom_styles

API_URL = "http://localhost:8000"

apply_custom_styles()

st.header("Add New Patient Record")
st.markdown("Enter comprehensive patient demographic details below.")

with st.container():
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    with st.form("new_patient_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. Ali Khan")
            father_name = st.text_input("Father Name *", placeholder="e.g. Muhammad Khan")
            gender = st.selectbox("Gender *", ["male", "female"])
            dob = st.date_input("Date of Birth *", value=date(2000, 1, 1))
            
        with col2:
            cnic = st.text_input("CNIC *", placeholder="e.g. 42101-1234567-1")
            phone = st.text_input("Phone *", placeholder="e.g. 0300-1234567")
            age = st.number_input("Age *", min_value=0, max_value=120, value=30)
            address = st.text_input("Address *", placeholder="e.g. Gulshan, Karachi")

        st.markdown("---")
        st.subheader("Hospital Data")
        
        col3, col4 = st.columns(2)
        with col3:
             mr_number = st.text_input("MR Number (Unique) *", placeholder="e.g. PT-4878")
             amount = st.number_input("Consultation Amount", min_value=0.0, value=200.0, step=50.0)
        with col4:
            receptionist_id = st.text_input("Receptionist ID *", placeholder="e.g. 6949240404")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Create Patient Record")
        
        if submitted:
            required_fields = [name, father_name, mr_number, cnic, phone, address, receptionist_id]
            if not all(required_fields):
                st.error("Please fill in all required fields marked with *")
            else:
                payload = {
                    "name": name,
                    "father_name": father_name,
                    "mr_number": mr_number,
                    "phone": phone,
                    "cnic": cnic,
                    "gender": gender,
                    "date_of_birth": str(dob),
                    "age": age,
                    "address": address,
                    "amount": amount,
                    "receptionist_id": receptionist_id
                }
                
                try:
                    with st.spinner("Saving to database..."):
                        res = requests.post(f"{API_URL}/patients/create", json=payload)
                        
                    if res.status_code == 200:
                        st.success(f"Patient Created Successfully! (ID: {res.json()['id']})")
                        st.info("You can now proceed to the 'Register Patient' page.")
                    else:
                        err = res.json().get('detail', 'Unknown error')
                        st.error(f"Creation Failed: {err}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
