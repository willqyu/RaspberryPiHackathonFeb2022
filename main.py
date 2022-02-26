import socket
import time
from picamera2 import *
from null_preview import *

from gesture_recognition import gesture_response

cam = Picamera2()
gesture_object = gesture_response(cam)

config = cam.preview_configuration(main={"size": (640, 480), "format": "BGR888"})
cam.configure(config)

preview = NullPreview(cam)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 42069))
sock.listen()

conn, addr = sock.accept()
conn.send("Hi".encode())

cam.start()
np_array = cam.capture_array()
np_bytes = np_array.tobytes()
print(len(np_bytes))
print(np_array.shape, np_array.dtype.name)
while True:
    np_array = cam.capture_array()
    np_bytes = np_array.tobytes()

    conn.send(b"head")
    conn.send(np_bytes)
    conn.send(b"tail")

    message = conn.recv(8).decode()
    print(message)
    if message[0] == "g":
        gesture_object.gesture_action(message[1])


sock.close()
cam.stop()
