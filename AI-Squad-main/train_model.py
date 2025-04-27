import warnings
import os
import certifi
import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module='keras')

# Set SSL certificates (for downloading models)
os.environ['SSL_CERT_FILE'] = certifi.where()

# Load the pre-trained Xception model without the top layer
base_model = Xception(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers on top of the base model
x = base_model.output
x = Flatten()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)  # Binary classification (real or fake)

# Create the final model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base layers (only train custom layers first)
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Set up data generators for training and validation
train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=20, zoom_range=0.2, horizontal_flip=True)
train_generator = train_datagen.flow_from_directory('data', target_size=(224, 224), batch_size=8, class_mode='binary')

validation_datagen = ImageDataGenerator(rescale=1./255)
validation_generator = validation_datagen.flow_from_directory('validation_data', target_size=(224, 224), batch_size=8, class_mode='binary')

# Model checkpoint to save the best model using .keras extension
checkpoint = ModelCheckpoint('/Users/samreshkumar/TrueSight/best_model.keras', monitor='val_loss', save_best_only=True, mode='min', verbose=1)

# Handle interruptions (e.g., Ctrl+C) and save the model
try:
    # Train the model with the checkpoint callback
    model.fit(train_generator, epochs=3, validation_data=validation_generator, callbacks=[checkpoint])
except KeyboardInterrupt:
    print("Training interrupted. Saving the current model...")
    model.save('/Users/samreshkumar/TrueSight/FaceForensics_interrupted.keras')

# Save the final model after training with the .keras extension
model.save('/Users/samreshkumar/TrueSight/FaceForensics.keras')

