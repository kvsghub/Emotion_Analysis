import cv2
import numpy as np
from tensorflow.keras.models import load_model 

# Load pre-trained emotion detection model
emotion_model = load_model("facial_emotion_recognition_model.keras")  # Specify your actual model path

def detect_emotions(frame):
    # Convert the frame to grayscale for the emotion detection model
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize the gray image to the input size expected by the model
    gray_resized = cv2.resize(gray, (48, 48))
    
    # Normalize the image
    gray_resized = gray_resized.astype("float32") / 255.0

    # Reshape for the model (1, 48, 48, 1) for grayscale
    gray_input = gray_resized.reshape(1, 48, 48, 1)

    # Convert grayscale to RGB for the model input
    rgb_input = np.repeat(gray_input, 3, axis=-1)  # This will convert to shape (1, 48, 48, 3)

    # Get predictions from the model
    predictions = emotion_model.predict(rgb_input)[0]  # Use rgb_input instead of gray_input

    # Process predictions as necessary
    return predictions

