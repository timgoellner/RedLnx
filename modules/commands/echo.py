import modules.system as system


def run(args: list[str], sudo: bool):
    if '-n' in args: out_list = args[1:]
    else: out_list = args

    echo_out = ""
    for out_snippet in out_list: echo_out += out_snippet + " "

    if '-n' in args: system.out([echo_out[:-1]], end_newline=False)
    else: system.out([echo_out[:-1]])
