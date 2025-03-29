import json, os

PATH = os.path.join(os.path.dirname(__file__), '../data/')


def get_data(config_id: int) -> dict:
    if config_id not in [1, 2, 3]: return {}

    if config_id == 1:
        with open(f"{PATH}system_data.json", "r") as data_file: return json.load(data_file)
    elif config_id == 2:
        with open(f"{PATH}file_system.json", "r") as data_file: return json.load(data_file)
    elif config_id == 3:
        with open(f"{PATH}command_data.json", "r") as data_file: return json.load(data_file)


def set_data(data: dict, config_id: int):
    if config_id not in [1, 2]: return
    if config_id == 1:
        with open(f"{PATH}system_data.json", "w") as data_file: json.dump(data, data_file, indent=4)
        return
    with open(f"{PATH}file_system.json", "w") as data_file: json.dump(data, data_file, indent=4)
