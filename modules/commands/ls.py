import modules.file_manager as file_manager, modules.data_handling as data_handling, modules.system as system


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if len(args) == 0 or (args[0].startswith('-') and len(args) == 1): directory_path = data_handling.get_data(1)["path"]
    elif args[0].startswith('-') and len(args) == 2: directory_path = file_manager.absolute_path_converter(args[1], data_handling.get_data(1)["path"])
    else: directory_path = file_manager.absolute_path_converter(args[0], data_handling.get_data(1)["path"])

    if directory_path not in file_system:
        system.out([f"ls: {directory_path}: No such directory"])
        return

    ls_out = []
    if "-la" not in args: ls_out.append("")

    for element in file_system[directory_path]:
        if file_system[directory_path][element]["type"] == 1:
            element_name = "&9" + element + "&f"
        else:
            element_name = element

        if "-la" in args:
            ls_out.append(file_system[directory_path][element]["author"] + "  " + file_system[directory_path][element][
                "creation_date"] + "  " + element_name)
        elif not element.startswith('.'):
            ls_out[0] += element_name + "  "

    if len(ls_out) == 0 or ls_out[0] != "": system.out(ls_out, colors=True)
