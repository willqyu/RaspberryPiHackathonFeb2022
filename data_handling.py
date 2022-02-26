from gesture_recognition import *
import cv2
import time
import numpy as np
    
def process_hand(image, hand_model, gesture_model):
    # pass video into network
    resolution = (640, 480)
    results = hand_model.process(image)
    gesture, confidence = 0, 0
    # process results
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x, y = [], []
            for lm in hand_landmarks.landmark:
                x.append(lm.x)
                y.append(lm.y)
                
            txt_pos = np.add(np.multiply(resolution, (x[0], y[0])), (-60, 30))
                
            # normalize points
            points = np.asarray([x,y])
            min = points.min(axis=1, keepdims=True)
            max = points.max(axis=1, keepdims=True)
            normalized = np.stack((points-min)/(max-min), axis=1).flatten()

            # get prediction and confidence
            pred = gesture_model.predict_proba([normalized])
            gesture = pred.argmax(axis=1)[0]
            confidence = pred.max()

    return gesture, confidence