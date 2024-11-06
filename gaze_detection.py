import cv2
import dlib

# Initialize dlib's face detector and shape predictor for gaze detection
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor/shape_predictor_68_face_landmarks.dat')  # Load landmarks model

# Function for gaze detection
def detect_gaze(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Left eye landmarks (more points for accuracy)
        left_eye_points = [landmarks.part(i) for i in range(36, 42)]
        left_eye_ratio = (left_eye_points[3].y - left_eye_points[0].y) / (left_eye_points[3].x - left_eye_points[0].x)

        # Right eye landmarks
        right_eye_points = [landmarks.part(i) for i in range(42, 48)]
        right_eye_ratio = (right_eye_points[3].y - right_eye_points[0].y) / (right_eye_points[3].x - right_eye_points[0].x)

        # Improved threshold logic
        looking_straight = left_eye_ratio > 0.15 and right_eye_ratio > 0.15  # Adjust thresholds based on your needs

        return looking_straight

    return False  # No face detected
