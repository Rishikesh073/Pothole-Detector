import os
import shutil
import random
import yaml

# --- SETTINGS ---
# We use abspath to automatically find the folders you created in Step 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = os.path.join(BASE_DIR, 'raw_data')
DEST_FOLDER = os.path.join(BASE_DIR, 'dataset_prepared')
SPLIT_RATIO = 0.8  # 80% Training, 20% Validation
# ----------------

def main():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"❌ Error: 'raw_data' folder not found at {SOURCE_FOLDER}")
        return

    # 1. Create Destination Structure
    for split in ['train', 'val']:
        for dtype in ['images', 'labels']:
            os.makedirs(os.path.join(DEST_FOLDER, split, dtype), exist_ok=True)

    # 2. Get Files
    all_files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    if not all_files:
        print("❌ No images found in 'raw_data'. Please paste your files there first.")
        return
        
    random.shuffle(all_files)
    split_idx = int(len(all_files) * SPLIT_RATIO)
    train_files = all_files[:split_idx]
    val_files = all_files[split_idx:]

    # 3. Move Files
    def move_batch(files, split_type):
        for filename in files:
            src_img = os.path.join(SOURCE_FOLDER, filename)
            # Find matching text file (checks .txt)
            base_name = os.path.splitext(filename)[0]
            src_txt = os.path.join(SOURCE_FOLDER, base_name + ".txt")
            
            if os.path.exists(src_txt):
                shutil.copy(src_img, os.path.join(DEST_FOLDER, split_type, 'images', filename))
                shutil.copy(src_txt, os.path.join(DEST_FOLDER, split_type, 'labels', base_name + ".txt"))

    print(f"Processing {len(all_files)} images...")
    move_batch(train_files, 'train')
    move_batch(val_files, 'val')

    # 4. Create data.yaml
    yaml_content = {
        'path': DEST_FOLDER.replace("\\", "/"), # Fix windows paths for YOLO
        'train': 'train/images',
        'val': 'val/images',
        'nc': 1,
        'names': ['pothole']
    }
    
    with open(os.path.join(DEST_FOLDER, 'data.yaml'), 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)

    print("✅ Success! Data organized. You can now run train.py")

if __name__ == "__main__":
    main()