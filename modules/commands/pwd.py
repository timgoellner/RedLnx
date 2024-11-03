import modules.data_handling as data_handling, modules.system as system

def run(args: list[str], sudo: bool):
    system.out([data_handling.get_data(1)["path"]])
