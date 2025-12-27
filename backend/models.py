from pydantic import BaseModel
from typing import Optional, List

class PatientCreate(BaseModel):
    name: str
    father_name: str
    mr_number: str
    phone: str
    cnic: str
    gender: str
    date_of_birth: str  # Format: YYYY-MM-DD
    age: int
    address: str
    amount: float
    receptionist_id: str

class PatientUpdate(BaseModel):
    # Used when registering a face to an existing patient
    patient_id: str  # MongoDB _id as string
    
class RecognitionResponse(BaseModel):
    patient_id: Optional[str] = None
    name: Optional[str] = None
    mr_number: Optional[str] = None
    similarity_score: float
    message: str
