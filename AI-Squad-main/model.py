# model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Model structure
def create_model(input_shape=(128, 128, 3)):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Binary classification: Real (0) or Fake (1)
    ])
    return model

# Training function
def train_model(data_dir, epochs=5, batch_size=32):
    model = create_model()

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Data augmentation for training
    train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')
    validation_datagen = ImageDataGenerator(rescale=1./255)

    # Load images from directory
    train_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='binary'
    )
    validation_generator = validation_datagen.flow_from_directory(
        os.path.join(data_dir, 'validation'),
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='binary'
    )

    # Train the model
    history = model.fit(train_generator, validation_data=validation_generator, epochs=epochs)

    # Save the model
    model.save('models/deepfake_detector_cnn.keras')
    print("Model training complete and saved as deepfake_detector_cnn.keras")

# Entry point for the script
if __name__ == "__main__":
    data_dir = './dataset'  # Ensure this is the path to your dataset folder
    train_model(data_dir)
