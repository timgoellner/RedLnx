import os
import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager, modules.perm_manager as perm_manager


def run(args: list[str], sudo: bool):
  file_system = data_handling.get_data(2)

  if len(args) == 0:
    system.out(["vi: missing operand"])
    return

  file_path = args[0]
  file_path_splits = file_path.split('/')

  if file_path_splits[-1] == '':
    system.out([f"vi: cannot read '{file_path}': No file provided"])
    return

  file_name = file_path_splits[-1]
  if len(file_path_splits) > 1:
    file_path = file_manager.absolute_path_converter('/'.join(file_path_splits[:-1]) + '/', data_handling.get_data(1)["path"])
  else:
    file_path = data_handling.get_data(1)["path"]

  if file_path not in file_system:
    system.out([f"vi: cannot access '{file_path}': No such directory"])
    return
  elif file_name not in file_system[file_path]:
    system.out([f"vi: cannot read '{file_path}': No such file"])
    return

  if not sudo and not perm_manager.validate_directory_access(file_path):
    system.out([f"vi: cannot read '{file_path}': Permission denied"])
    return

  if not perm_manager.validate_directory_access(file_path) and not perm_manager.validate_session(): return

  #os.system('cls')