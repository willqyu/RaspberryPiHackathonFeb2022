from curses import raw
from picamera2 import *

cam = Picamera2()

raw_np_array = cam.capture_array("raw")

print(raw_np_array)