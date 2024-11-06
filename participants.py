import cv2
from collections import deque
from gaze_detection import detect_gaze
from emotion_detection import detect_emotions
from utils import get_engagement_state
import numpy as np

# Dictionary to manage participants
participants_dict = {}

class Participant:
    def __init__(self, participant_id, video_source):
        self.participant_id = participant_id
        self.video_source = video_source
        self.engagement_history = deque(maxlen=5)  # For sliding window
        self.current_frame = None
        self.is_active = True

    def analyze(self, frame):
        # Gaze Detection
        looking = detect_gaze(frame)

        # Emotion Detection
        predictions = detect_emotions(frame)
        
        # Update sliding window with current predictions
        self.engagement_history.append(predictions)

        if len(self.engagement_history) == 5:
            # Calculate average of the last 5 frames for smooth analysis
            average_predictions = np.mean(self.engagement_history, axis=0)
            engagement_state, engagement_scores = get_engagement_state(average_predictions, looking)
            return engagement_state, engagement_scores
        return None, None  # Return None if there’s not enough data yet



def add_participant(participant_id, video_source):
    participant = Participant(participant_id, video_source)  # Create a new Participant instance
    participants_dict[participant_id] = participant  # Store the participant in the dictionary
    return participant  # Do not call analyze here, we’ll call it in main.py

def remove_participant(participant_id):
    if participant_id in participants_dict:
        participants_dict[participant_id].is_active = False
        del participants_dict[participant_id]


