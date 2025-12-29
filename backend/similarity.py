import numpy as np

def cosine_similarity(vec1, vec2):
    """
    Calculate true cosine similarity between two vectors.
    Returns a value between -1 and 1 (typically 0 to 1 for face embeddings).
    Higher = more similar.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))
