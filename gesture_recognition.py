class gesture_response:
    def __init__(self, confidence, gesture, video_state, cam):
        self.confidence = confidence
        self.gesture = gesture
        self.video_state = video_state
        self.cam = cam

    def gesture_action(self):
        if not self.video_state and self.confidence >= 85:
            if self.gesture == 0:
                self.cam.capture_picture()
            elif self.gesture == 1:
                self.cam.capture_video_start()
            else:
                pass
        elif self.video_state and self.confidence >= 85:
            if self.gesture == 2:
                self.cam.capture_video_stop()
            else:
                pass
        else:
            pass
