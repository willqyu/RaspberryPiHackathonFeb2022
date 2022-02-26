from curses import raw
from picamera2 import *
from null_preview import *

cam = Picamera2()
cam.configure(cam.still_configuration())
preview = NullPreview(picam2)
cam.start()
raw_np_array = cam.capture_array("raw")

print(raw_np_array)