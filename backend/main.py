from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from contextlib import asynccontextmanager
from typing import Optional
from datetime import datetime
from backend.database import init_db, get_patient_by_mr_number, update_patient_embedding, search_patient_by_embedding, get_patient_by_id
from backend.face_utils import face_handler
from backend.models import RecognitionResponse
from backend.similarity import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        init_db()
    except Exception as e:
        print(f"Warning: DB connection failed: {e}")
    yield
    # Shutdown

app = FastAPI(title="Patient Face Recognition API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SIMILARITY_THRESHOLD = 0.6

@app.get("/")
def read_root():
    return {"status": "online", "system": "Patient Face Recognition System For Saylani Medical Center "}

@app.get("/patient/{mr_number}")
def lookup_patient(mr_number: str):
    patient = get_patient_by_mr_number(mr_number)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name"),
        "mrNumber": patient.get("mrNumber"),
        "cnic": patient.get("cnic"),
        "has_face": "faceEmbedding" in patient and len(patient["faceEmbedding"]) > 0
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
    logger.info("Starting Face Recognition Request...")
    # 1. Process Image
    content = await file.read()
    embedding, error = face_handler.process_image(content)
    
    if error:
        logger.error(f"Face Processing Error: {error}")
        raise HTTPException(status_code=400, detail=error)
        
    # 2. Vector Search
    results = search_patient_by_embedding(embedding)
    logger.info(f"Vector performed search. Found {len(results)} candidates.")
    
    if not results:
        return RecognitionResponse(
            similarity_score=0.0,
            message="No match found (no candidates)"
        )
        
    best_match = results[0]
    mongodb_score = best_match.get("score", 0.0)
    
    # CRITICAL FIX: Calculate TRUE cosine similarity
    # MongoDB's score is NOT cosine similarity - it's a relevance score
    # We need to fetch the stored embedding and calculate manually
    stored_patient = get_patient_by_id(str(best_match["_id"]))
    if not stored_patient or "faceEmbedding" not in stored_patient:
        return RecognitionResponse(
            similarity_score=0.0,
            message="No face embedding found for matched patient"
        )
    
    stored_embedding = stored_patient["faceEmbedding"]
    true_similarity = cosine_similarity(embedding, stored_embedding)
    
    print(f"DEBUG: MongoDB Score={mongodb_score:.4f}, True Cosine Similarity={true_similarity:.4f}")
    
    # 3. Threshold Check using TRUE similarity
    if true_similarity >= SIMILARITY_THRESHOLD:
        return RecognitionResponse(
            patient_id=str(best_match["_id"]),
            name=best_match.get("name"),
            mr_number=best_match.get("mrNumber"),
            similarity_score=true_similarity,
            message="Identity Verified"
        )
    else:
        return RecognitionResponse(
            similarity_score=true_similarity,
            message=f"Identity verification failed: Similarity {true_similarity:.3f} < threshold {SIMILARITY_THRESHOLD}"
        )
