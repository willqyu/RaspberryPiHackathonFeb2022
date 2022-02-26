import socket
import numpy as np
import time

HOST = '192.168.137.71'    # The remote host
PORT = 42069              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    frame_count = 0
    incoming = b''
    try:
        while True:
            message = s.recv(1024)
            if message == b'':
                s.close()
                break
            elif message[:4] == b"head":
                print("head")
                incoming = b''
                incoming += message[4:]
            elif message[-4:] == b"tail":
                print("tail")
                incoming += message[:-4]
                decoded = np.frombuffer(incoming, dtype = 'uint8').reshape((480, 640, 4))
                print("frame", frame_count)
                frame_count += 1
            else:
                incoming+=message
            
            pass
    except KeyboardInterrupt:
        s.close()