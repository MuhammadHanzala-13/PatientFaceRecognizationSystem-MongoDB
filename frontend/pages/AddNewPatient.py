import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #1e3c72;">Add New Patient Record</h1>
    <p style="color: #666;">Enter comprehensive patient demographic details</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    with st.form("new_patient_form"):
        # Personal Information Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px 10px 0 0; margin-bottom: 1.5rem;">
            <h3 style="color: white; margin: 0;">👤 Personal Information</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. Ali Khan", help="Patient's complete legal name")
            father_name = st.text_input("Father Name *", placeholder="e.g. Muhammad Khan")
            gender = st.selectbox("Gender *", ["male", "female"], help="Select patient gender")
            dob = st.date_input("Date of Birth *", value=date(2000, 1, 1), help="Patient's date of birth")
            
        with col2:
            cnic = st.text_input("CNIC *", placeholder="e.g. 42101-1234567-1", help="13-digit national ID")
            phone = st.text_input("Phone *", placeholder="e.g. 0300-1234567", help="Primary contact number")
            age = st.number_input("Age *", min_value=0, max_value=120, value=30, help="Current age in years")
            address = st.text_input("Address *", placeholder="e.g. Gulshan, Karachi", help="Residential address")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hospital & Administrative Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1rem; border-radius: 10px 10px 0 0; margin-bottom: 1.5rem;">
            <h3 style="color: white; margin: 0;">🏥 Hospital & Administrative Data</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
             mr_number = st.text_input("MR Number (Unique) *", placeholder="e.g. PT-4878", help="Medical Record Number - must be unique")
             amount = st.number_input("Consultation Amount", min_value=0.0, value=200.0, step=50.0, help="Consultation fee")
        with col4:
            receptionist_id = st.text_input("Receptionist ID *", placeholder="e.g. 6949240404", help="ID of staff member creating record")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅ Create Patient Record")
        
        if submitted:
            # Validation
            required_fields = [name, father_name, mr_number, cnic, phone, address, receptionist_id]
            if not all(required_fields):
                st.error("⚠️ Please fill in all required fields marked with *")
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
                    with st.spinner("💾 Saving to database..."):
                        res = requests.post(f"{API_URL}/patients/create", json=payload)
                        
                    if res.status_code == 200:
                        st.success(f"✅ Patient Created Successfully! (ID: {res.json()['id']})")
                        st.info("➡️ You can now proceed to the 'Register Patient' page to enroll their biometrics.")
                    else:
                        err = res.json().get('detail', 'Unknown error')
                        st.error(f"❌ Creation Failed: {err}")
                except Exception as e:
                    st.error(f"🔌 Connection Error: {e}")
