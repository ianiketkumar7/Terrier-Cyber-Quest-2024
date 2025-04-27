import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Prepare data generators
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    '../processed',
    target_size=(224, 224),
    batch_size=8,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    '../processed',
    target_size=(224, 224),
    batch_size=8,
    class_mode='binary',
    subset='validation'
)

# Define CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print(f"Training samples found: {train_generator.samples}")
print(f"Validation samples found: {validation_generator.samples}")


# Train the model
model.fit(train_generator, validation_data=validation_generator, epochs=5)

# Save the model
model.save('../models/deepfake_detector_cnn.keras')

