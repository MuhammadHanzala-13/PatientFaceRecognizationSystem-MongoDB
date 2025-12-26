import cv2
import numpy as np
import os

class FaceHandler:
    def __init__(self):
        # Paths to models
        base_path = os.path.dirname(__file__)
        det_path = os.path.join(base_path, "models", "face_detection_yunet_2023mar.onnx")
        rec_path = os.path.join(base_path, "models", "face_recognition_sface_2021dec.onnx")
        
        if not os.path.exists(det_path) or not os.path.exists(rec_path):
            raise FileNotFoundError("Models not found! Run backend/setup_models.py first.")

        # Initialize YuNet (Detector)
        self.detector = cv2.FaceDetectorYN.create(
            model=det_path,
            config="",
            input_size=(320, 320), # Init size, will update per image
            score_threshold=0.6,
            nms_threshold=0.3,
            top_k=5000,
            backend_id=cv2.dnn.DNN_BACKEND_OPENCV,
            target_id=cv2.dnn.DNN_TARGET_CPU
        )
        
        # Initialize SFace (Recognizer)
        self.recognizer = cv2.FaceRecognizerSF.create(
            model=rec_path,
            config="",
            backend_id=cv2.dnn.DNN_BACKEND_OPENCV,
            target_id=cv2.dnn.DNN_TARGET_CPU
        )
        
    def process_image(self, image_bytes):
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None, "Invalid image format"

        h, w, _ = img.shape
        # Update detector input size to match image
        self.detector.setInputSize((w, h))
        
        # Detect faces
        # faces = [x, y, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rcm, y_rcm, x_lcm, y_lcm, score]
        _, faces = self.detector.detect(img)
        
        if faces is None or len(faces) == 0:
            return None, "No face detected"
        
        if len(faces) > 1:
            return None, "Multiple faces detected. Please ensure only one person is in frame."
            
        face = faces[0]
        
        # Align and Crop
        aligned_face = self.recognizer.alignCrop(img, face)
        
        # Extract Feature (128D)
        embedding = self.recognizer.feature(aligned_face)
        
        # Flatten to list
        return embedding[0].tolist(), None

face_handler = FaceHandler()
