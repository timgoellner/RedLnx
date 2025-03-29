import modules.system as system, modules.data_handling as data_handling, modules.login as login

def run(args: list[str], sudo: bool):
    if (len(args) == 0) or (len(args) == 1 and '-p' in args):
        system.out(["su: missing operand"])
        return

    system_data = data_handling.get_data(1)

    if args[0] != "-p": user = args[0].lower()
    else: user = args[1].lower()

    if user not in system_data["users"]:
        system.out([f"su: user '{user}' does not exist"])
        return

    system.out(["Password: "], end_newline=False)
    password = login.get_pass()

    if password != system_data["users"][user]["passwd"]:
        system.out(["su: incorrect password attempt"])
        return
    
    if '-p' not in args:
        system_data["users"][system_data["curr_user"]]["sudo_session"] = False

        if system_data["users"][user]["home_folder"]: system_data["path"] = f"/home/{user}/"
        else: system_data["path"] = '/'

    system_data["curr_user"] = user

    data_handling.set_data(system_data, 1)
