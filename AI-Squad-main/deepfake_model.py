import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the trained or pre-trained deepfake detection model
model = load_model('/Users/samreshkumar/TrueSight/FaceForensics.keras')  # Replace with your trained model path

def check_deepfake(file_path):
    """
    Uses the trained deepfake detection model to analyze an image or video.
    """
    try:
        # Load the image
        image = cv2.imread(file_path)
        image = cv2.resize(image, (224, 224))
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image / 255.0  # Normalize
        
        # Predict if the content is real or fake
        prediction = model.predict(image)
        return "fake" if prediction > 0.5 else "real"
    except Exception as e:
        return f"Error: {str(e)}"

