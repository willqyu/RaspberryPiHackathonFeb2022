import time

class gesture_response:
    def __init__(self, cam):
        
        self.busy_state = False
        self.cam = cam

    # processes gesture and confidence level
    def gesture_action(self, gesture):
        self.gesture = gesture
        if not self.busy_state and int(self.gesture) == 0:
            self.delay_capture()

    # function for delaying image capture
    def delay_capture(self):
        self.busy_state = True
        print("Picture taking in 5!")
        for i in range(1, 5):
            time.sleep(1)
            print(str(i))
        # capture_image(insert image capture function)       
        self.cam.capture_file("../images/{}.jpeg".format(int(time.time())))
        self.busy_state = False
