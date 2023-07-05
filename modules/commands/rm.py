import modules.system as system, modules.file_manager as file_manager, modules.data_handling as data_handling, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if len(args) == 0:
        system.out(["mkdir: missing operand"])
        return

    for remove_file_path in args:
        remove_file_path_splits = remove_file_path.split('/')
        if remove_file_path_splits[-1] == '':
            system.out([f"rm: cannot remove '{remove_file_path}': No file provided"])
            return

        file_name = remove_file_path_splits[-1]
        if len(remove_file_path_splits) > 1:
            file_path = file_manager.absolute_path_converter('/'.join(remove_file_path_splits[:-1]) + '/', data_handling.get_data(1)["path"])
        else:
            file_path = data_handling.get_data(1)["path"]

        if file_path not in file_system:
            system.out([f"rm: cannot remove '{remove_file_path}': No such directory"])
            return
        elif file_name not in file_system[file_path]:
            system.out([f"rm: cannot remove '{remove_file_path}': No such file"])
            return

        if not sudo and not perm_manager.validate_file_access(file_path + file_name):
            system.out([f"rm: cannot remove file '{remove_file_path}': Permission denied"])
            return

        if not perm_manager.validate_file_access(file_path + file_name) and not perm_manager.validate_session(): return

        file_manager.remove_file(file_path, file_name)
