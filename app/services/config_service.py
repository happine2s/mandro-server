import json
import os
from pathlib import Path

CONFIG_PATH = os.getenv("CONFIG_PATH", "app/storage/config.json")
CONFIG_FILE = Path(CONFIG_PATH)

config_data = {
    "gap": 76,
    "cameras": {
        "cam0": {"order": 1, "rotation": 0, "flipped": False},
        "cam1": {"order": 2, "rotation": 0, "flipped": False}
    },
    "stream": {
        "resolution": [640, 480],
        "quality": 80,
        "fps": 30
    }
}

def load_config():
    global config_data
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
    return config_data

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=2)

def get_config():
    return config_data

def update_config(gap: int, cam0: dict, cam1: dict, stream: dict):
    config_data["gap"] = gap
    config_data["cameras"]["cam0"].update(cam0)
    config_data["cameras"]["cam1"].update(cam1)
    config_data["stream"].update(stream)
    save_config()
    return config_data

