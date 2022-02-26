import socket
from picamera2 import *
from null_preview import *

cam = Picamera2()

config = cam.preview_configuration(main={"size": (640, 480)})
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
print(np_bytes.shape)

conn.send(b"head")
conn.send(np_bytes)
conn.send(b"tail")

sock.close()
cam.stop()
