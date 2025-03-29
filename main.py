import socket, os
import modules.login as login, modules.data_handling as data_handling, modules.system as system, modules.command_manager as command_manager


def redlnx_runtime():
    global user_name, path
    command = [""]

    while not (command[0] == "exit" or (len(command) > 1 and command[1] == "exit")):
        system_data = data_handling.get_data(1)
        user_name = system_data["curr_user"]
        if system_data["users"][user_name]["home_folder"]: path = (system_data["path"]).replace(f"/home/{user_name}", "~")
        else: path = system_data["path"]
        if path not in ['/', '~']: path = path[:-1]

        if system_data["users"][user_name]["sudo"]: input_char = '#'
        else: input_char = '$'

        command = system.out([f"&a{user_name}@{socket.gethostname()}&f:&9{path}&f{input_char} "], input_mode=True, colors=True).split(' ')
        if command[0].lower() == "sudo" and len(command) > 1 and command[1].lower() not in ["", "exit"]: command_manager.parse_cmd(command[1].lower(), command[2:], True)
        elif command[0].lower() not in ["", "exit", "sudo"]: command_manager.parse_cmd(command[0].lower(), command[1:], False)

    shutdown()


def startup():
    global user_name, path

    os.system('cls')

    system_data = data_handling.get_data(1)
    if len(system_data["users"]) == 0:
        user_name = login.start_setup()
        system_data = data_handling.get_data(1)
    else: user_name = login.start_login()

    if system_data["users"][user_name]["home_folder"]: system_data["path"] = f"/home/{user_name}/"
    else: system_data["path"] = '/'

    system_data["curr_user"] = user_name
    path = system_data["path"]
    data_handling.set_data(system_data, 1)

    redlnx_runtime()


def shutdown():
    system_data = data_handling.get_data(1)

    for user in system_data["users"]: system_data["users"][user]["sudo_session"] = False
    data_handling.set_data(system_data, 1)


if __name__ == "__main__":
    global user_name, path
    startup()
