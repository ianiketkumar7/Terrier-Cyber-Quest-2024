import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Check if the file exists
file_path = '../models/deepfake_detector_cnn.keras'
if os.path.exists(file_path):
    print(f"File found: {file_path}")
else:
    print(f"File not found: {file_path}")

# Load the trained model
model = load_model('../models/deepfake_detector_cnn.keras')

# Function to predict
def predict_image(image):
    img_resized = cv2.resize(image, (224, 224))
    img_normalized = img_resized / 255.0
    img_reshaped = np.reshape(img_normalized, (1, 224, 224, 3))
    prediction = model.predict(img_reshaped)
    return prediction[0][0]

# Real-time detection
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    prediction = predict_image(frame)
    label = "Fake" if prediction > 0.5 else "Real"
    color = (0, 0, 255) if prediction > 0.5 else (0, 255, 0)

    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Real-time Deepfake Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

