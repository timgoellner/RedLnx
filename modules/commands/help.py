import modules.system as system, modules.data_handling as data_handling

CMD_DATA = data_handling.get_data(3)


def run(args: list[str], sudo: bool):
    if len(args) == 1:
        args[0] = args[0].lower()
        if args[0] not in CMD_DATA: system.out([f"-bash: help: no help topics match '{args[0]}'"])
        else:
            cmd_usage = CMD_DATA[args[0]]["usage"]
            system.out([f" {args[0]}: {cmd_usage}"])
        return

    help_out = []
    for cmd in CMD_DATA: help_out.append(" " + CMD_DATA[cmd]["usage"])
    system.out(help_out)
