import os
import requests

# URLs for OpenCV Zoo models (Lightweight & Accurate)
MODELS = {
    "face_detection_yunet_2023mar.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_recognition_sface_2021dec.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
}

DEST_DIR = os.path.join(os.path.dirname(__file__), "models")

def download_file(url, dest_path):
    if os.path.exists(dest_path):
        print(f"✅ Exists: {dest_path}")
        return
    
    print(f"⬇️ Downloading {os.path.basename(dest_path)}...")
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded: {dest_path}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

if __name__ == "__main__":
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    
    for filename, url in MODELS.items():
        download_file(url, os.path.join(DEST_DIR, filename))
        
    print("\n🎉 Model setup complete. You can now run the system.")
