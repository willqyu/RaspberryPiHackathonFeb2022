import time
class gesture_response:
    def __init__(self, confidence, gesture, busy_state, cam):
        self.confidence = confidence
        self.gesture = gesture
        self.busy_state = busy_state
        self.cam = cam
    
    # processes gesture and confidence level
    def gesture_action(self):
        if not self.busy_state and self.confidence >= 85:
                self.cam.delay_capture(self.gesture)
        else:
            pass
    # function for delaying image capture
    def delay_capture(self):
        self.busy_state = True
        time.sleep(int(self.gesture))
        # capture_image(insert image capture function)       
