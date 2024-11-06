import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.applications import ResNet50 
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint

# Define image data generators
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
    'data/train',  # Change to your train directory
    target_size=(48, 48),  # Ensure this matches your image size
    color_mode='rgb',  # Change to 'rgb' to ensure 3 channels
    batch_size=32,
    class_mode='categorical'
)

validation_datagen = ImageDataGenerator(rescale=1.0/255.0)
validation_generator = validation_datagen.flow_from_directory(
    'data/test',  # Change to your test directory
    target_size=(48, 48),
    color_mode='rgb',  # Change to 'rgb' to ensure 3 channels
    batch_size=32,
    class_mode='categorical'
)

# Define the model with modified input shape
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(48, 48, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(7, activation='softmax')(x)  # Adjust num_classes as per your dataset
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Create a ModelCheckpoint callback
checkpoint = ModelCheckpoint('facial_emotion_recognition_model.keras', 
                             monitor='val_accuracy', 
                             verbose=1, 
                             save_best_only=True, 
                             mode='max')

# Fit the model
history = model.fit(
    train_generator, 
    validation_data=validation_generator, 
    epochs=10, 
    callbacks=[checkpoint]
)


