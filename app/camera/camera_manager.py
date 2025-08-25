from picamera2 import Picamera2
from threading import Lock
import cv2

class CameraManager:
    def __init__(self):
        self.cameras = [Picamera2(0), Picamera2(1)]
        self.locks = [Lock(), Lock()]
        for cam in self.cameras:
            config = cam.create_video_configuration(main={"size": (960, 540)})
            cam.configure(config)
            cam.start()

    def get_frame(self, index: int):
        with self.locks[index]:
            frame = self.cameras[index].capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame