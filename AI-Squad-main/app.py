# app.py
import os
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from urllib.request import urlopen
from PIL import Image
import io

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'models/deepfake_detector_cnn.keras'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = load_model(MODEL_PATH)

def preprocess_image(image):
    """Resize and normalize the image."""
    img = cv2.resize(image, (128, 128))  # Ensure this matches your training
    img = img / 255.0  # Normalize to [0,1]
    img = np.reshape(img, (1, 128, 128, 3))
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        # Check if a file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            # Read the image file
            in_memory_file = io.BytesIO()
            file.save(in_memory_file)
            data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is None:
                return jsonify({'error': 'Invalid image file.'}), 400
            processed_img = preprocess_image(img)
            prediction = model.predict(processed_img)[0][0]
            label = "Fake" if prediction > 0.5 else "Real"
            confidence = float(prediction)
            return jsonify({'result': label, 'confidence': confidence}), 200

        # Check if a link is submitted
        elif 'link' in request.form and request.form['link'].strip() != '':
            link = request.form['link']
            # Download the image from the URL
            with urlopen(link) as response:
                data = response.read()
            img = Image.open(io.BytesIO(data)).convert('RGB')
            img = np.array(img)
            processed_img = preprocess_image(img)
            prediction = model.predict(processed_img)[0][0]
            label = "Fake" if prediction > 0.5 else "Real"
            confidence = float(prediction)
            return jsonify({'result': label, 'confidence': confidence}), 200

        else:
            return jsonify({'error': 'No file or link provided.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

