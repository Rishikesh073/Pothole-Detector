print("--- 1. Script started... Importing libraries (this takes a few seconds) ---")
from ultralytics import YOLO
import os

if __name__ == '__main__':
    print("--- 2. Libraries imported. Setting up paths ---")
    
    # 1. Setup Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_YAML_PATH = os.path.join(BASE_DIR, 'dataset_prepared', 'data.yaml')

    print(f"--- 3. Looking for data at: {DATA_YAML_PATH}")

    # Check if data exists
    if not os.path.exists(DATA_YAML_PATH):
        print("❌ CRITICAL ERROR: data.yaml not found.")
        print(f"   Please make sure a folder named 'dataset_prepared' exists inside: {BASE_DIR}")
        exit()

    print("--- 4. Loading the YOLO model... ---")
    # Load the model
    model = YOLO('yolov8n.pt') 

    print("--- 5. Starting Training (Press Ctrl+C to stop if it freezes) ---")
    
    # 3. Train
    # I removed device='0' so it defaults to CPU if GPU fails
    results = model.train(
        data=DATA_YAML_PATH,
        epochs=5,       # Reduced to 5 just to test if it runs
        imgsz=640,
        batch=4,        # Reduced batch size to prevent memory crashes
        name='pothole_model'
    )
    
    print("--- 6. Training Finished Successfully! ---")
