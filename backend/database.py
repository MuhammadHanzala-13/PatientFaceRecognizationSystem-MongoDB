import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "Medical_Management_System"
COLLECTION_NAME = "patients"

client = None
db = None
collection = None

def init_db():
    global client, db, collection
    if not MONGO_URI:
        raise ValueError("MONGO_URI not found in environment variables")
    
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Ping to check connection
    try:
        client.admin.command('ping')
        print("Connected to MongoDB Atlas!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e

def get_patient_by_id(patient_id: str):
    return collection.find_one({"_id": ObjectId(patient_id)})

def get_patient_by_mr_number(mr_number: str):
    return collection.find_one({"mrNumber": mr_number})

def update_patient_embedding(patient_id: str, embedding: list):
    collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": {"faceEmbedding": embedding}}
    )

def search_patient_by_embedding(embedding: list):
    # Vector Search Aggregation
    # Requires an Atlas Vector Search Index named 'vector_index' (default name suggestion)
    # The field path should be 'faceEmbedding'
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "faceEmbedding",
                "queryVector": embedding,
                "numCandidates": 100,
                "limit": 1
            }
        },
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "mrNumber": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    
    results = list(collection.aggregate(pipeline))
    return results

def get_all_patients_limit(limit=10):
    return list(collection.find({}, {"faceEmbedding": 0}).limit(limit))


