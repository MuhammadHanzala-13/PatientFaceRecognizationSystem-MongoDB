from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from contextlib import asynccontextmanager
from typing import Optional
from backend.database import init_db, get_patient_by_mr_number, update_patient_embedding, search_patient_by_embedding, get_patient_by_id
from backend.face_utils import face_handler
from backend.models import RecognitionResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: DB connection failed: {e}")
    yield
    # Shutdown

SIMILARITY_THRESHOLD = 0.4  # Adjusted for SFace (Cosine Similarity)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Patient Face Recognition MVP"}

@app.get("/patient/{mr_number}")
def lookup_patient(mr_number: str):
    patient = get_patient_by_mr_number(mr_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name"),
        "mrNumber": patient.get("mrNumber"),
        "has_face": "faceEmbedding" in patient
    }

@app.post("/register")
async def register_patient_face(
    mr_number: str = Form(...),
    file: UploadFile = File(...)
):
    # 1. Verify patient exists
    patient = get_patient_by_mr_number(mr_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # 2. Process Image
    content = await file.read()
    embedding, error = face_handler.process_image(content)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
        
    # 3. Store Embedding
    update_patient_embedding(str(patient["_id"]), embedding)
    
    return {"message": f"Face registered successfully for {patient.get('name')}"}

@app.post("/recognize", response_model=RecognitionResponse)
async def recognize_patient(file: UploadFile = File(...)):
    # 1. Process Image
    content = await file.read()
    embedding, error = face_handler.process_image(content)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
        
    # 2. Vector Search
    results = search_patient_by_embedding(embedding)
    
    if not results:
        return RecognitionResponse(
            similarity_score=0.0,
            message="No match found (no candidates)"
        )
        
    best_match = results[0]
    score = best_match.get("score", 0.0)
    
    # 3. Threshold Check
    if score >= SIMILARITY_THRESHOLD:
        return RecognitionResponse(
            patient_id=str(best_match["_id"]),
            name=best_match.get("name"),
            mr_number=best_match.get("mrNumber"),
            similarity_score=score,
            message="Identity Verified"
        )
    else:
        return RecognitionResponse(
            similarity_score=score,
            message="Identity verification failed: Low similarity score"
        )
