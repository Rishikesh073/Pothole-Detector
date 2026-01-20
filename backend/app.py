from flask import Flask, request, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)
CORS(app) # Allows the React frontend to talk to this backend

# Load YOUR custom model
# This expects best.pt to be in the same folder as app.py
model = YOLO('best.pt') 

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return "No file uploaded", 400

    # 1. Get the image from the request
    file = request.files['file']
    img = Image.open(file.stream)

    # 2. Run your trained YOLO model
    # conf=0.25 means it will only detect potholes with >25% confidence
    results = model.predict(img, conf=0.25)

    # 3. Draw the bounding boxes onto the image
    # plot() returns a numpy array (BGR format)
    res_plotted = results[0].plot()
    
    # Convert back to an image format that browsers understand (RGB)
    res_img = Image.fromarray(res_plotted[..., ::-1])

    # 4. Save to a memory buffer to send back
    img_io = io.BytesIO()
    res_img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)