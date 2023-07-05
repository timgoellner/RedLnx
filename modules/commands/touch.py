import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if len(args) == 0:
        system.out(["touch: missing operand"])
        return

    for new_file_path in args:
        new_file_path_splits = new_file_path.split('/')
        if new_file_path_splits[-1] == '':
            system.out([f"touch: cannot touch '{new_file_path}': No file provided"])
            return

        file_name = new_file_path_splits[-1]
        if len(new_file_path_splits) > 1:
            file_path = file_manager.absolute_path_converter('/'.join(new_file_path_splits[:-1]) + '/',
                                                             data_handling.get_data(1)["path"])
        else:
            file_path = data_handling.get_data(1)["path"]

        if '&' in new_file_path:
            system.out(["touch: forbidden character in file name: &"])
            return

        if file_path not in file_system:
            system.out([f"touch: cannot touch '{new_file_path}': No such directory"])
            return
        elif file_name in file_system[file_path]:
            system.out([f"touch: cannot touch '{new_file_path}': File already exists"])
            return

        if not sudo and not perm_manager.validate_directory_access(file_path):
            system.out([f"touch: cannot create file '{new_file_path}': Permission denied"])
            return

        if not perm_manager.validate_directory_access(file_path) and not perm_manager.validate_session(): return

        file_manager.create_file(file_path, file_name)
