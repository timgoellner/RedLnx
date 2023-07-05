import modules.system as system, modules.file_manager as file_manager, modules.data_handling as data_handling, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if (len(args) == 0) or (len(args) == 1 and args[0].startswith('-')):
        system.out(["mkdir: missing operand"])
        return

    if "-p" in args:
        args.remove("-p")
        parent_create = True
    else: parent_create = False

    for directory_relative_path in args:
        full_directory_path = file_manager.absolute_path_converter(directory_relative_path, data_handling.get_data(1)["path"])
        directory_path = '/'.join((full_directory_path.split('/'))[:-2]) + '/'
        directory_name = (full_directory_path.split('/'))[-2:][0].replace('/', '')

        for forbidden_char in ['&', '.']:
            if forbidden_char in directory_name:
                system.out([f"mkdir: forbidden character in directory name: {forbidden_char}"])
                return

        if directory_path not in file_system:
            if not parent_create:
                system.out([f"mkdir: cannot create directory '{directory_relative_path}': No such directory"])
                return
            else: run(["-p", directory_path], sudo)
        elif full_directory_path in file_system:
            system.out([f"mkdir: cannot create directory '{directory_relative_path}': Directory already exists"])
            return

        if (not sudo and directory_path == '/') or (not sudo and not perm_manager.validate_directory_access(directory_path)):
            system.out([f"mkdir: cannot create directory '{directory_relative_path}': Permission denied"])
            return

        if not perm_manager.validate_directory_access(directory_path) and not perm_manager.validate_session(): return

        file_manager.create_directory(directory_path, directory_name)
