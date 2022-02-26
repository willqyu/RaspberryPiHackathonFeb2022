from gesture_recognition import *
import cv2
import time
import numpy as np
from joblib import load
from mediapipe.python.solutions import drawing_utils, hands

# load the models
gesture_model = load('./model/gesture_model.pkl')
hand_model = hands.Hands(static_image_mode=True, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7, max_num_hands=1)


# pass video into network
image = []
resolution = (640, 480)
results = hand_model.process(image)

# process results
if results.multi_hand_landmarks:
    