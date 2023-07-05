import modules.system as system, modules.data_handling as data_handling, modules.login as login, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
    if not sudo:
        system.out(["passwd: Permission denied."])
        return

    if not perm_manager.validate_session(): return
    system_data = data_handling.get_data(1)

    if len(args) == 0: user = system_data["curr_user"]
    else: user = args[0].lower()

    if user not in system_data["users"]:
        system.out([f"passwd: user '{user}' does not exist"])
        return

    if user == system_data["curr_user"]: system.out([f"Changing password for {user}."])

    system.out(["New password: "], end_newline=False)
    new_password = login.get_pass()
    system.out(["Retype new password: "], end_newline=False)
    retyped_new_password = login.get_pass()

    if new_password != retyped_new_password:
        system.out(["passwd: Passwords do not match.", "passwd: password unchanged"])
        return

    system.out(["passwd: password updated successfully"])

    system_data["users"][user]["passwd"] = new_password
    data_handling.set_data(system_data, 1)
