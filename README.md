# Patient Face Recognition MVP

This is a Minimum Viable Product (MVP) for identity verification in a small clinic environment. It runs entirely on CPU and is designed to be lightweight, explainable, and easy to maintain.

## 🏗 System Architecture

The system consists of two main components:
1. **Backend (FastAPI)**: Handles logic, face processing, and database interactions.
2. **Frontend (Streamlit)**: simple UI for receptionists to register and verify patients.

**Why this stack?**
- **FastAPI**: Modern, fast, and gives us automatic API documentation (`/docs`).
- **InsightFace (Buffalo_S)**: A state-of-the-art face recognition model that is surprisingly lightweight. We use the `buffalo_s` model which uses ResNet50 for verification—fast enough for an i3 CPU (~300ms inference).
- **MongoDB Atlas**: Used for storing patient data. We leverage **Atlas Vector Search** to find the closest face match efficiently without loading all embeddings into memory.
- **Streamlit**: Allows building the UI in pure Python without needing a separate frontend team.

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Required for compiling insightface dependencies on Windows)

### 2. Install Dependencies
Run via terminal in this directory:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your MongoDB connection string:
```ini
MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

### 4. Database Setup (Crucial!)
You must configure the **Vector Search Index** in MongoDB Atlas for the matching to work.

1. Go to **Atlas Search** -> **Vector Search** -> **Create Search Index**.
2. Select your `clinic_db.patients` collection.
3. Select **JSON Editor** and paste this configuration:
   ```json
   {
     "fields": [
       {
         "numDimensions": 512,
         "path": "faceEmbedding",
         "similarity": "cosine",
         "type": "vector"
       }
     ]
   }
   ```
4. Name the index `vector_index`.

---

## ▶️ Running the System

You need two terminals running simultaneously.

**Terminal 1: Backend**
```bash
uvicorn backend.main:app --reload
```
*Verify it's running at: http://localhost:8000/docs*

**Terminal 2: Frontend**
```bash
streamlit run frontend/app.py
```
*Access the UI at: http://localhost:8501*

---

## 🧠 Technical Decisions & Trade-offs

### Face Model (InsightFace Buffalo_S)
We avoided heavy Transformer-based models or deep tracking pipelines. `Buffalo_S` detects faces (RetinaFace) and extracts embeddings (ArcFace) in one go. It handles alignment automatically. 
- **Trade-off**: Slightly less accurate than massive server-grade models on non-frontal faces, but perfect for a cooperative "look at the camera" clinic setting.

### Vector Search vs. In-Memory
We use MongoDB Vector Search instead of loading all 10,000+ embeddings into a generic `scikit-learn` model in RAM.
- **Benefit**: Scalable. The app startup time remains fast even if you have 1 million patients.

### Correctness > Cleverness
We enforce a strict **One Face Per Image** rule. If the receptionist captures a photo with background faces, the system rejects it rather than guessing. This prevents identity mix-ups.

### Thresholding
We use a similarity threshold (default `0.5`). 
- **>= 0.5**: Identity Verified.
- **< 0.5**: Verification Failed.
*Note: This threshold is tuned for Cosine Similarity on ArcFace embeddings. Adjust in `backend/main.py` if false negatives occur.*

