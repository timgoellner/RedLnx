import os
import modules.system as system, modules.data_handling as data_handling, modules.file_manager as file_manager, modules.perm_manager as perm_manager

TERMINAL_LINES = os.get_terminal_size().lines
TERMINAL_COLUMNS = os.get_terminal_size().columns


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
    system.out([f"vi: cannot read '{file_path + file_name}': No such file"])
    return

  if not sudo and not perm_manager.validate_directory_access(file_path):
    system.out([f"vi: cannot read '{file_path + file_name}': Permission denied"])
    return

  if not perm_manager.validate_directory_access(file_path) and not perm_manager.validate_session(): return

  data = file_manager.read_file(file_path, file_name)

  unused_lines = TERMINAL_LINES - len(data) - 2
  if unused_lines < 0:
    system.out(["vi: file is too long for console size"])
    return

  os.system('cls')

  system.out(data)
  system.out(['&1~\n&f' * unused_lines], colors=True, end_newline=False)

  characters = sum(len(line) for line in data)
  system.out([f"\"{file_name}\" {len(data)} lines, {characters} characters"])

  mode = 'normal'
  command = ''

  position = [0, 0]
  system.position(position)


  while True:
    key = system.get()

    if mode == 'insert':
      if len(key) == 1:
        if len(data[position[1]]) + 1 > (TERMINAL_COLUMNS - 1):
          set_status('error: x boundary reached', position)
          continue

        line_chars = data[position[1]][position[0]:]
        system.out([key + line_chars], end_newline=False, instant=True)
        data[position[1]] = data[position[1]][:position[0]] + key + line_chars
        position[0] += 1
        system.position(position)


      elif key == 'enter':
        if unused_lines == 0:
          set_status('error: y boundary reached', position)
          continue

        line_chars = data[position[1]][position[0]:]
        data[position[1]] = data[position[1]][:position[0]]
        system.out([' ' * len(line_chars)], instant=True)

        position[0] = 0

        data.insert(position[1] + 1, "")
        for move_index in range(0, TERMINAL_LINES - unused_lines - 3 - position[1]):
          line = TERMINAL_LINES - unused_lines - move_index - 2
          system.position([position[0], line])
          if len(data) > line + 1: system.out([data[line] + (' ' * max(0, len(data[line + 1]) - len(data[line])))], instant=True)
          elif len(data[line]) == 0: system.out([' '], instant=True)
          else: system.out([data[line]], instant=True)

        unused_lines -= 1
        position[1] += 1
        system.position(position)

        data[position[1]] = line_chars
        if len(data) > position[1] + 1: system.out([line_chars + (' ' * max(0, len(data[position[1]+1]) - len(line_chars)))], instant=True)
        elif len(line_chars) > 0: system.out([line_chars], instant=True)
        else: system.out([' '], instant=True)

        system.position(position)

      elif key == 'backspace':
        line_chars = data[position[1]][position[0]:]

        if position[0] == 0:
          if position[1] == 0: continue
          elif len(line_chars) + len(data[position[1]-1]) > (TERMINAL_COLUMNS - 1):
            set_status('error: x boundary reached', position)
            continue

          data.pop(position[1])
          for move_index in range(0, TERMINAL_LINES - unused_lines - 3 - position[1]):
            line = position[1] + move_index
            if move_index != 0: system.out([data[line] + (' ' * max(0, len(data[line - 1]) - len(data[line])))], instant=True)
            else: system.out([data[line] + (' ' * max(0, len(line_chars) - len(data[line])))], instant=True)

          if position[1] != len(data): system.out(['&1~&f' + (' ' * max(0, len(data[-1])-1))], colors=True, end_newline=False, instant=True)
          else: system.out(['&1~&f' + (' ' * max(0, len(line_chars)-1))], colors=True, end_newline=False, instant=True)
          unused_lines += 1

          position[1] -= 1
          position[0] = len(data[position[1]])
          system.position(position)
          
          data[position[1]] += line_chars
          system.out([line_chars], instant=True, end_newline=False)

          system.position(position)
          continue

        position[0] -= 1
        system.position(position)
        system.out([line_chars + ' '], instant=True)
        data[position[1]] = data[position[1]][:position[0]] + line_chars
        system.position(position)


      elif key == 'up':
        if position[1] == 0: continue

        position[1] -= 1
        position[0] = min(len(data[position[1]]), position[0])
        system.position(position)

      elif key == 'left':
        if position[0] == 0:
          if position[1] == 0: continue

          position[1] -= 1
          position[0] = len(data[position[1]])
          system.position(position)
          continue

        position[0] -= 1
        system.position(position)

      elif key == 'down':
        if position[1] == (TERMINAL_LINES - unused_lines - 3): continue

        position[1] += 1
        position[0] = min(len(data[position[1]]), position[0])
        system.position(position)

      elif key == 'right':
        if position[0] == len(data[position[1]]):
          if position[1] == (TERMINAL_LINES - unused_lines - 3): continue

          position[1] += 1
          position[0] = 0
          system.position(position)
          continue

        if position[0] < len(data[position[1]]):
          position[0] += 1
          system.position(position)

      elif key == 'esc':
        set_status('', position)
        mode = 'normal'

    elif mode == 'normal':
      if key == ':':
        set_status('', [0, TERMINAL_LINES - 2])
        system.out([':'], end_newline=False, instant=True)
        mode = 'command'
        command = ''

      elif key == 'a' or key == 'i':
        set_status(' -- insert -- ', position)
        mode = 'insert'

    elif mode == 'command':
      if len(key) == 1:
        if len(data[position[1]]) + 1 > (TERMINAL_COLUMNS - 1): continue
        system.out([key], end_newline=False, instant=True)
        command += key

      elif key == 'enter':
        if command == 'w':
          file_manager.write_file(file_path, file_name, data)
          characters = sum(len(line) for line in data)
          set_status(f"\"{file_name}\" {len(data)} lines, {characters} characters written", position)
          mode = 'normal'
        elif command == 'q':
          os.system('cls')
          break
        elif command == 'wq':
          file_manager.write_file(file_path, file_name, data)
          characters = sum(len(line) for line in data)
          set_status(f"\"{file_name}\" {len(data)} lines, {characters} characters written", position)
          os.system('cls')
          break
        else:
          set_status(f"&4error: not an editor command: {command}&f", position, colors=True)
          mode = 'normal'

      elif key == 'esc':
        set_status('', position)
        mode = 'normal'



def set_status(status: str, position: list[int], colors: bool = False):
  system.position([0, TERMINAL_LINES - 2])
  system.out([status + (' ' * (TERMINAL_COLUMNS - (len(status) + 1)))], instant=True, colors=colors)
  system.position(position)