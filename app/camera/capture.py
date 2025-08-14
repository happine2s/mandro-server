from picamera2 import Picamera2

def open_camera():
    cam = Picamera2()
    config = cam.configure(cam.create_still_configuration())
    cam.configure(config)
    cam.start()
    return cam

def capture_frame(cam):
    return cam.capture_array()
