import random

def get_engagement_state(predictions, looking):
   
    if not looking:
        return "Attentive", {}

    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    engagement_mapping = {
        'Attentive': ['Neutral', 'Happy', 'Surprise'],
        'Bored': ['Sad', 'Disgust'],
        'Distracted': ['Fear', 'Surprise'],
        'Confused': ['Fear', 'Angry']
    }

    emotion_probs = dict(zip(emotions, predictions))

    engagement_scores = {
        'Attentive': sum(emotion_probs[emotion] for emotion in engagement_mapping['Attentive']),
        'Bored': sum(emotion_probs[emotion] for emotion in engagement_mapping['Bored']),
        'Distracted': sum(emotion_probs[emotion] for emotion in engagement_mapping['Distracted']),
        'Confused': sum(emotion_probs[emotion] for emotion in engagement_mapping['Confused'])
    }

    engagement_state = max(engagement_scores, key=engagement_scores.get)
    return engagement_state, engagement_scores