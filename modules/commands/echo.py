import modules.system as system


def run(args: list[str], sudo: bool):
    if '-n' in args: out_list = args[1:]
    else: out_list = args

    out_list = " ".join(out_list)

    if '-n' in args: system.out([out_list], end_newline=False)
    else: system.out([out_list])
