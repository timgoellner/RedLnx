import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
    if (len(args) == 0) or (len(args) == 1 and "-m" in args):
        system.out(["useradd: missing operand"])
        return

    if args[0] != "-m": new_user_name = args[0].lower()
    else: new_user_name = args[1].lower()

    if not sudo:
        system.out(["useradd: Permission denied."])
        return

    if not perm_manager.validate_session(): return
    system_data = data_handling.get_data(1)
    file_system = data_handling.get_data(2)

    if new_user_name in system_data["users"]:
        system.out([f"useradd: user '{new_user_name}' already exists"])
        return

    for denied_char in ['&', '/']:
        if denied_char in new_user_name:
            system.out([f"useradd: forbidden character in username: {denied_char}"])
            return

    system_data["users"][new_user_name] = {"passwd": "", "home_folder": False, "sudo": False, "sudo_session": False}
    if "-m" in args:
        if "/home/"+new_user_name+"/" in file_system:
            system.out([f"useradd: cannot create directory '/home/{new_user_name}/': Directory already exists"])
            return

        system_data["users"][new_user_name]["home_folder"] = True

        prev_user = system_data["curr_user"]
        system_data["curr_user"] = new_user_name
        data_handling.set_data(system_data, 1)

        file_manager.create_directory("/home/", new_user_name)

        system_data["curr_user"] = prev_user
        data_handling.set_data(system_data, 1)

    data_handling.set_data(system_data, 1)
