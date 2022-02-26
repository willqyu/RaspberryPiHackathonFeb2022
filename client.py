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
                gesture, confidence = process_hand(decoded_image, hand_model, gesture_model)
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