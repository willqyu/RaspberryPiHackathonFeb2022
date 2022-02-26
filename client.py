import socket
import numpy as np
import time
from gesture_recognition import *
import cv2
from joblib import load
from mediapipe.python.solutions import drawing_utils, hands

from data_handling import process_hand

# load the models
gesture_model = load('./model/gesture_model.pkl')
hand_model = hands.Hands(static_image_mode=True, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7, max_num_hands=1)

HOST = '192.168.137.71'    # The remote host
PORT = 42069              # The same port as used by the server

def process_hand(image):
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    incoming = b''
    try:
        while True:
            message = s.recv(1024)
            if message == b'':
                s.close()
                break
            elif message[:4] == b"head":
                incoming = b''
                incoming += message[4:]
            elif message[-4:] == b"tail":
                incoming += message[:-4]
                decoded_image = np.frombuffer(incoming, dtype = 'uint8').reshape((480, 640, 3))
                rgb_image = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB)
                #cv2.imshow("Gesture Recognition", rgb_image)
                cv2.waitKey(3)
                print("before process!")
                gesture, confidence = process_hand(decoded_image)
                if confidence:
                    print(gesture)
                    return_message = "g" + str(gesture)
                    s.send(return_message.encode())
                print("after!")

            else:
                incoming+=message
            
            pass
    except KeyboardInterrupt:
        s.close()