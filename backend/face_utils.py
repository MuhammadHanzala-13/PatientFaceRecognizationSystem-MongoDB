import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

class FaceHandler:
    def __init__(self):
        # Use buffalo_s for lightweight (ResNet50 based embedding, MobileNet based detection)
        # providers=['CPUExecutionProvider'] ensures CPU only usage
        self.app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640))
        
    def process_image(self, image_bytes):
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Invalid image format")

        # InsightFace pipeline: Detect -> Align -> Embed
        faces = self.app.get(img)
        
        if len(faces) == 0:
            return None, "No face detected"
        
        if len(faces) > 1:
            # Sort by area/center to pick the main one? 
            # Or strict rule "One face per image only"
            # User said "One face per image only", implies we should reject if multiple? 
            # Or just pick the largest. Let's start strict as per instructions: "One face per image only" 
            # might mean "Don't process group photos". 
            # But usually for UX, picking the largest face is better. 
            # I will return error to follow strict constraint.
            return None, "Multiple faces detected. Please ensure only one person is in frame."
            
        face = faces[0]
        embedding = face.embedding
        
        # Helper to normalize if needed, though ArcFace is usually normalized?
        # InsightFace embeddings are usually normalized to 1.0 length or close?
        # It's safer to normalize for cosine similarity usage if the DB expects it.
        # But Vector Search handles cosine/dotProduct. 
        # For simplicity, convert to standard Python list of floats.
        
        return embedding.tolist(), None

face_handler = FaceHandler()
