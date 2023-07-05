import modules.system as system, modules.file_manager as file_manager, modules.data_handling as data_handling


def run(args: list[str], sudo: bool):
    system_data = data_handling.get_data(1)

    if len(args) != 0:
        directory_path = file_manager.absolute_path_converter(args[0], system_data["path"])
    elif system_data["users"][system_data["curr_user"]]["home_folder"]:
        directory_path = "/home/" + system_data["curr_user"] + "/"
    else: directory_path = '/'

    if directory_path not in data_handling.get_data(2):
        system.out([f"cd: {directory_path}: No such directory"])
        return

    system_data["path"] = directory_path
    data_handling.set_data(system_data, 1)
