import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager, modules.perm_manager as perm_manager
import modules.commands.rm as rm


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if (len(args) == 0) or (len(args) == 1 and args[0].startswith('-')):
        system.out(["rmdir: missing operand"])
        return

    if "-rf" in args:
        args.remove("-rf")
        child_remove = True
    else:
        child_remove = False

    for directory_relative_path in args:
        full_directory_path = file_manager.absolute_path_converter(directory_relative_path,
                                                                   data_handling.get_data(1)["path"])
        directory_path = '/'.join((full_directory_path.split('/'))[:-2]) + '/'
        directory_name = (full_directory_path.split('/'))[-2:][0].replace('/', '')

        if directory_name not in file_system[directory_path]:
            system.out([f"rmdir: failed to remove '{directory_relative_path}': No such directory"])
            return

        if (not sudo and full_directory_path == '/') or (not sudo and not perm_manager.validate_directory_access(full_directory_path)):
            system.out([f"rmdir: cannot remove directory '{directory_relative_path}': Permission denied"])
            return

        if not perm_manager.validate_directory_access(full_directory_path) and not perm_manager.validate_session(): return

        if len(file_system[full_directory_path]) != 0:
            if not child_remove: system.out([f"rmdir: failed to remove '{directory_relative_path}': Directory not empty"])
            else:
                for child_content_name in file_system[full_directory_path]:
                    if file_system[full_directory_path][child_content_name]["type"] == 1: run(["-rf", full_directory_path + child_content_name + '/'], sudo)
                    elif file_system[full_directory_path][child_content_name]["type"] == 2: rm.run([full_directory_path + child_content_name], sudo)
                file_manager.remove_directory(directory_path, directory_name)
            return

        file_manager.remove_directory(directory_path, directory_name)
