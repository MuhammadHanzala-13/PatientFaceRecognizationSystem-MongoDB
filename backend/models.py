from pydantic import BaseModel
from typing import Optional, List



class PatientUpdate(BaseModel):
    # Used when registering a face to an existing patient
    patient_id: str  # MongoDB _id as string
    
class RecognitionResponse(BaseModel):
    patient_id: Optional[str] = None
    name: Optional[str] = None
    mr_number: Optional[str] = None
    similarity_score: float
    message: str

class RegisterBase64(BaseModel):
    mr_number: str
    image_base64: str

class RecognizeBase64(BaseModel):
    image_base64: str
