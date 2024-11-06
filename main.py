import cv2
import dlib
from participants import participants_dict, add_participant, remove_participant
import time
import math

# Initialize dlib's face detector and define global variables
detector = dlib.get_frontal_face_detector()
trackers = {}  # Dictionary to hold trackers with timeout for each participant

# Configuration constants
TIMEOUT_DURATION = 5.0    # Time (in seconds) to consider a participant as "left" if no face is detected
FRAME_SKIP = 4            # Process every N-th frame to reduce load
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.5
font_color = (255, 0, 0)
line_type = 1
# Initialize frame counter
frame_counter = 0

def add_or_update_participants(frame):
    global trackers
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    current_time = time.time()

    # Update existing trackers or add new ones
    for face in faces:
        matched_tracker = None
        face_center = ((face.left() + face.right()) / 2, (face.top() + face.bottom()) / 2)

        for participant_id, (tracker, last_seen) in trackers.items():
            pos = tracker.get_position()
            tracker_center = ((pos.left() + pos.right()) / 2, (pos.top() + pos.bottom()) / 2)

            # Allow more tolerance in matching for smoother tracking
            if distance(tracker_center, face_center) < 100:  # Increase threshold for tolerance
                matched_tracker = (participant_id, tracker)
                trackers[participant_id] = (tracker, current_time)  # Update last seen
                tracker.start_track(frame, face)  # Update tracker
                break
        # If no match, add a new tracker and initialize participant analysis
        if matched_tracker is None:
            participant_id = len(trackers) + 1
            tracker = dlib.correlation_tracker()
            tracker.start_track(frame, face)
            trackers[participant_id] = (tracker, current_time)
            add_participant(participant_id, frame)  # Only pass the ID to add participant
  # Add new participant for analysis

    # Remove participants who haven’t been seen within the timeout
    to_remove = [participant_id for participant_id, (tracker, last_seen) in trackers.items()
                 if current_time - last_seen > TIMEOUT_DURATION]
    for participant_id in to_remove:
        remove_participant(participant_id)  # Remove participant from analysis
        del trackers[participant_id]  # Remove the tracker

    return trackers

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Main function
if __name__ == "__main__":
    cap = cv2.VideoCapture('data/samplevideo2.mp4')

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Only process every Nth frame for performance (adjust as needed)
        frame_count += 1
        if frame_count % FRAME_SKIP != 0:
            continue
        else:
            trackers = add_or_update_participants(frame)
            for participant_id, participant in participants_dict.items():
                # Perform analysis for the current frame
                engagement_state, engagement_scores = participant.analyze(frame)
                
                # Only render text if we have a valid engagement state
                if engagement_state:
                    tracker_position = trackers[participant_id][0].get_position()
                    pos_x, pos_y = int(tracker_position.left()), int(tracker_position.top()) - 30
                    
                    # Overlay the engagement state on the main frame
                    cv2.putText(frame, f"Participant {participant_id}: {engagement_state}", 
                                (pos_x, pos_y), font, font_scale, (255, 255, 51), line_type)

        # Draw rectangles around tracked faces
        for participant_id, (tracker, _) in trackers.items():
            pos = tracker.get_position()
            cv2.rectangle(frame, (int(pos.left()), int(pos.top())), (int(pos.right()), int(pos.bottom())), (0, 255, 0), 2)
            cv2.putText(frame, f"Participant {participant_id}", (int(pos.left()), int(pos.top()) - 10),
                        font, font_scale, font_color, line_type)

        cv2.imshow("Participants Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()












