import socket
from picamera2 import *
from null_preview import *

cam = Picamera2()
config = cam.still_configuration()
cam.configure(config)

preview = NullPreview(cam)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", 42069))
sock.listen()

conn, addr = sock.accept()

cam.start()

np_array = cam.capture_array().tobytes()
print(len(np_array))
#sock.send(np_array)
sock.send("Hi".encode())
cam.stop()
sock.close()
