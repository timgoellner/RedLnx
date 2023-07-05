import modules.system as system, modules.data_handling as data_handling, modules.login as login


def validate_directory_access(directory_path: str) -> bool:
    system_data = data_handling.get_data(1)
    file_system = data_handling.get_data(2)

    if directory_path == '/': return False
    elif file_system['/'.join((directory_path.split('/'))[:-2]) + '/'][(directory_path.split('/'))[-2:][0].replace('/', '')]["author"] == system_data["curr_user"]: return True
    else: return False


def validate_file_access(file_path: str) -> bool:
    system_data = data_handling.get_data(1)
    file_system = data_handling.get_data(2)

    if file_system['/'.join((file_path.split('/'))[:-1]) + '/'][(file_path.split('/'))[-1:][0].replace('/', '')]["author"] == system_data["curr_user"]: return True
    else: return False


def validate_session() -> bool:
    system_data = data_handling.get_data(1)

    curr_user = system_data["curr_user"]
    if not system_data["users"][curr_user]["sudo_session"]: sudo_session = False
    else: sudo_session = True

    passwd = ""
    if not sudo_session:
        system.out([f"[sudo] password for {curr_user}: "], end_newline=False)
        passwd = login.get_pass()

    if not sudo_session and passwd != system_data["users"][curr_user]["passwd"]:
        system.out(["sudo: incorrect password attempt"])
        return False

    if not system_data["users"][curr_user]["sudo"]:
        system.out([f"sudo: {curr_user} is not in the sudoers file."])
        return False

    if not sudo_session: system_data["users"][curr_user]["sudo_session"] = True
    data_handling.set_data(system_data, 1)

    return True

