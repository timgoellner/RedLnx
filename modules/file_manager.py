import modules.data_handling as data_handling
import os, datetime

PATH = os.path.join(os.path.dirname(__file__), '../file_system')


def create_directory(underlying_directory_name: str, directory_name: str):
    file_system = data_handling.get_data(2)

    file_system[underlying_directory_name][directory_name] = {"type": 1, "author": data_handling.get_data(1)["curr_user"], "creation_date": datetime.date.today().strftime("%b %d %Y")}
    file_system[underlying_directory_name + directory_name + '/'] = {}
    data_handling.set_data(file_system, 2)

    os.mkdir(PATH + underlying_directory_name + directory_name)


def remove_directory(underlying_directory_name: str, directory_name: str):
    file_system = data_handling.get_data(2)

    del file_system[underlying_directory_name][directory_name]
    del file_system[underlying_directory_name + directory_name + '/']
    data_handling.set_data(file_system, 2)

    os.rmdir(PATH + underlying_directory_name + directory_name)


def create_file(directory_name: str, file_name: str):
    file_system = data_handling.get_data(2)

    file_system[directory_name][file_name] = {"type": 2, "author": data_handling.get_data(1)["curr_user"], "creation_date": datetime.date.today().strftime( "%b %d %Y")}
    data_handling.set_data(file_system, 2)

    new_file = os.open(PATH + directory_name + file_name, os.O_CREAT)
    os.close(new_file)


def remove_file(directory_name: str, file_name: str):
    file_system = data_handling.get_data(2)

    del file_system[directory_name][file_name]
    data_handling.set_data(file_system, 2)

    os.remove(PATH + directory_name + file_name)


def read_file(directory_name: str, file_name: str) -> list[str]:
    with open(PATH + directory_name + file_name) as file:
        return file.read().split('\n')

def write_file(directory_name: str, file_name: str, data: list[str]):
    with open(PATH + directory_name + file_name) as file:
        file.writelines(data)


def absolute_path_converter(input_path: str, location: str) -> str:
    system_data = data_handling.get_data(1)

    if input_path.startswith('/'):
        if not input_path.endswith('/'): input_path += '/'
        return input_path

    input_path = input_path.split('/')
    curr_location = location
    for path_snippet in input_path:
        if path_snippet == "": continue
        elif path_snippet == "..": curr_location = '/'.join((curr_location.split('/'))[:-2]) + '/'
        else: curr_location += path_snippet + '/'

    return curr_location
