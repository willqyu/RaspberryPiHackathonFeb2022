from gesture_recognition import *
import cv2
import time
import numpy as np
from joblib import load
from mediapipe.python.solutions import drawing_utils, hands

# load the models
gesture_model = load('./model/gesture_model.pkl')
hand_model = hands.Hands(static_image_mode=True, 
    min_detection_confidence=0.85, 
    min_tracking_confidence=0.7, max_num_hands=1)
txt_offset = (-60, 30)


# pass video into network
image = []
resolution = (640, 480)
results = hand_model.process(image)

# process results
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        x, y = [], []
        for lm in hand_landmarks.landmark:
            x.append(lm.x)
            y.append(lm.y)
            
        txt_pos = np.add(np.multiply(resolution, (x[0], y[0])), txt_offset)
            
        # normalize points
        points = np.asarray([x,y])
        min = points.min(axis=1, keepdims=True)
        max = points.max(axis=1, keepdims=True)
        normalized = np.stack((points-min)/(max-min), axis=1).flatten()

        # get prediction and confidence
        pred = gesture_model.predict_proba([normalized])
        gesture = pred.argmax(axis=1)[0]
        confidence = pred.max()

        # add text
        cv2.putText(image, "'{}',{:.1%}".format(gesture, confidence), 
        txt_pos.astype(int), cv2.FONT_HERSHEY_DUPLEX,  1, 
        (0, 255, 255), 1, cv2.LINE_AA)