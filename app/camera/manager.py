from picamera2 import Picamera2
from libcamera import Transform

_camera_instances = {}

def get_camera(index: int) -> Picamera2:
    if index not in _camera_instances:
        cam = Picamera2(index=index)
        config = cam.create_still_configuration(transform=Transform(vflip=1), buffer_count=1)
        cam.configure(config)
        cam.start()
        _camera_instances[index] = cam
    return _camera_instances[index]

def capture_frame(index: int):
    cam = get_camera(index)
    return cam.capture_array()
