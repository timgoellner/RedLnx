import msvcrt, socket
import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager

MOTD = ["      ___           ___          _____                          ___           ___",
        "     /  /\         /  /\        /  /::\     ___                /__/\         /__/|",
        "    /  /::\       /  /:/_      /  /:/\:\   /__/\               \  \:\       |  |:|",
        "   /  /:/\:\     /  /:/ /\    /  /:/  \:\  \  \:\     ___       \  \:\      |  |:|",
        "  /  /:/~/:/    /  /:/ /:/_  /__/:/ \__\:|  \  \:\   /  /\  _____\__\:\   __|__|:|",
        " /__/:/ /:/___ /__/:/ /:/ /\ \  \:\ /  /:/   \  \:\ /  /:/ /__/::::::::\ /__/::::\____",
        " \  \:\/:::::/ \  \:\/:/ /:/  \  \:\  /:/     \  \:\  /:/  \  \:\~~\~~\/    ~\~~\::::/",
        "  \  \::/~~~~   \  \::/ /:/    \  \:\/:/       \  \:\/:/    \  \:\  ~~~      |~~|:|~~",
        "   \  \:\        \  \:\/:/      \  \::/         \  \::/      \  \:\          |  |:|",
        "    \  \:\        \  \::/        \__\/           \__\/        \  \:\         |  |:|",
        "     \__\/         \__\/                                       \__\/         |__|/"]


def get_pass() -> str:
    input_char, input_word = "", ""
    while input_char not in ['\n', '\r']:
        input_char = msvcrt.getwch()
        input_word += input_char
    msvcrt.putwch('\n')

    for sec in ['\n', '\r']: input_word = input_word.replace(sec, '')
    return input_word


def start_login() -> str:
    input_user_name = system.out(["[&2+&f] login as: "], input_mode=True, colors=True)
    system_data = data_handling.get_data(1)
    input_password = None

    while (input_user_name.lower() not in system_data["users"]) or (
            system_data["users"][input_user_name.lower()]["passwd"] != input_password):
        if input_password is not None: system.out([f"[&4-&f] Access denied"], colors=True)
        system.out([f"[&2+&f] {input_user_name}@{socket.gethostbyname(socket.gethostname())}'s password: "],
                   end_newline=False, colors=True)
        input_password = get_pass()

    system.out(["Welcome to RedLnx " + system_data["version"] + " oriented at (GNU/Linux => x86_64)"] + MOTD)

    return input_user_name.lower()


def start_setup() -> str:
    system_data = data_handling.get_data(1)
    system.out(["Welcome to RedLnx " + system_data["version"] + " oriented at (GNU/Linux => x86_64)"] + MOTD)
    while True:
        new_user_name = system.out(["[&e/&f] New RedLnx username: "], input_mode=True, colors=True).lower()

        if new_user_name == '':
            system.out(["-bash: forbidden username: username cannot be empty"])
            continue

        for denied_char in ['&', '/']:
            if denied_char in new_user_name:
                system.out([f"-bash: forbidden character in username: {denied_char}"])
                break
        else: break
    system.out(["[&e/&f] New RedLnx password: "], end_newline=False, colors=True)
    new_passwd = get_pass()

    system_data["users"][new_user_name] = {"passwd": new_passwd, "home_folder": True, "sudo": True, "sudo_session": False}
    system_data["curr_user"] = new_user_name
    data_handling.set_data(system_data, 1)

    file_manager.create_directory("/", "home")
    file_manager.create_directory("/home/", new_user_name)

    return new_user_name
