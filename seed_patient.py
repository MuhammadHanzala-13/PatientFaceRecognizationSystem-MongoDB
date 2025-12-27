from backend import database
from datetime import datetime

def seed_patient():
    # 1. Initialize DB first
    database.init_db()
    
    # 2. Get the collection object explicitly AFTER init
    coll = database.collection
    
    if coll is None:
        print("❌ Error: Database collection is still None. Check DB connection.")
        return

    # Test Patient Data
    patient_data = {
        "name": "John Doe",
        "gender": "Male",
        "dob": "1990-01-01",
        "phone": "1234567890",
        "cnic": "42101-1234567-1",
        "address": "123 Test St, Karachi",
        "mrNumber": "MR-2024-001",
        "status": "Active",
        "created_at": datetime.now()
        
    }
    
    # Check if exists
    if coll.find_one({"mrNumber": "MR-2024-001"}):
        print("Test patient 'MR-2024-001' already exists.")
    else:
        coll.insert_one(patient_data)
        print("✅ Added test patient: John Doe (MR-2024-001)")

if __name__ == "__main__":
    seed_patient()
