import modules.system as system, modules.data_handling as data_handling, modules.perm_manager as perm_manager
import modules.commands.rmdir as rmdir


def run(args: list[str], sudo: bool):
    file_system = data_handling.get_data(2)

    if (len(args) == 0) or (len(args) == 1 and "-r" in args):
        system.out(["userdel: missing operand"])
        return

    if args[0] != "-r": del_user_name = args[0].lower()
    else: del_user_name = args[1].lower()

    if not sudo:
        system.out(["userdel: Permission denied."])
        return

    if not perm_manager.validate_session(): return
    system_data = data_handling.get_data(1)

    if del_user_name not in system_data["users"]:
        system.out([f"userdel: user '{del_user_name}' does not exist"])
        return

    if system_data["curr_user"] == del_user_name:
        system.out([f"userdel: user {del_user_name} is currently used"])
        return

    del system_data["users"][del_user_name]
    if "-r" in args and f"/home/{del_user_name}/" in file_system: rmdir.run(["-rf", f"/home/{del_user_name}/"], sudo)
    elif "-r" in args: system.out([f"userdel: {del_user_name} home directory (/home/{del_user_name}) not found"])

    data_handling.set_data(system_data, 1)
