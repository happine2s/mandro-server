config_data = {
    "gap": 76,
    "cameras": {
        "cam0": {"order": 1, "rotation": 0, "flipped": False},
        "cam1": {"order": 2, "rotation": 0, "flipped": False}
    }
}


def get_config():
    return config_data


def update_config(gap: int, cam0: dict, cam1: dict):
    config_data["gap"] = gap
    config_data["cameras"]["cam0"].update(cam0)
    config_data["cameras"]["cam1"].update(cam1)
    return config_data
