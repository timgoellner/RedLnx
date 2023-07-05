import os
import modules.system as system, modules.data_handling as data_handling

CMD_PATH = os.path.join(os.path.dirname(__file__), 'commands/')
CMD_DATA = data_handling.get_data(3)


def parse_cmd(cmd: str, args: list[str], sudo: bool):
    for module in os.listdir(CMD_PATH):
        if module[:-3] != cmd: continue
        if check_cmd_options(cmd, args) and check_cmd_args(cmd, args): __import__(f"commands.{module[:-3]}", globals(), locals(), ['run'], level=1).run(args, sudo)
        break
    else: system.out([f"-bash: {cmd}: command not found"])


def check_cmd_args(cmd: str, args: list[str]) -> bool:
    cmd_max_args = CMD_DATA[cmd]["max_args"]
    input_args = 0
    for arg in args:
        if not arg.startswith('-'): input_args += 1

    if (input_args > cmd_max_args) and cmd_max_args != -1:
        system.out([f"-bash: {cmd}: too many arguments"])
        return False

    return True


def check_cmd_options(cmd: str, args: list[str]) -> bool:
    cmd_options = CMD_DATA[cmd]["options"]
    for arg in args:
        if arg.startswith('-') and arg not in cmd_options:
            system.out([f"-bash: {cmd}: {arg}: invalid option"])
            send_command_usage(cmd)
            return False

    return True


def send_command_usage(cmd: str):
    cmd_usage = data_handling.get_data(3)[cmd]["usage"]
    system.out([f"{cmd}: usage: {cmd_usage}"])
