from picamera2 import *
from h264_encoder import *
from null_preview import *
import socket
import os
import time

# init camera
picam = Picamera2()
video_config = picam.video_configuration({"size": (1280, 720)})
picam.configure(video_config)
preview = NullPreview(picam)
encoder = H264Encoder(1000000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", 10001))
        sock.listen()

        picam.encoder = encoder
        picam.start_encoder()
        picam.start()

        conn, addr = sock.accept()
        stream = conn.makefile("wb")
        picam.encoder.output = stream
        while True:
            time.sleep(1)
        
        
    except KeyboardInterrupt:
        picam.stop()
        picam.stop_encoder()
        conn.close()
