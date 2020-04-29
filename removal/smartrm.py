import json
import logging
import os
from pathlib import Path
from removal.removafile import File

module_logger = logging.getLogger('SmartRM')


class SmartRM:
    def __init__(self):
        home = str(Path.home())
        self.trash_path = os.path.join(home, 'Trash')

        if not os.path.exists(self.trash_path):
            os.mkdir(self.trash_path)
            os.chmod(self.trash_path, 0o777)
            self.trash_path = os.path.abspath(self.trash_path)
            module_logger.debug(f'Create trash can on {self.trash_path}')
            module_logger.info(f'Trash can created on {self.trash_path}')

    def save_information(self, my_trash):
        module_logger.debug('Start saving information about file')
        json_path = os.path.join(self.trash_path, 'trash_information.json')
        data = {}
        with open(json_path) as file:
            data.update(json.load(file))
        with open(json_path, 'w') as file:
            data[f'{my_trash.file_name}'] = my_trash.information()
            json.dump(my_trash.information(), file)

    def load_information(self):
        module_logger.debug('Start load information')
        json_path = os.path.join(self.trash_path, 'trash_info.json')
        data = {}
        if os.path.exists(json_path):
            with open(json_path) as file:
                data.update(json.load(file))
                return data

    def update_information(self, name):
        json_path = os.path.join(self.trash_path, 'trash_information.json')
        module_logger.debug('Information in trash updated')
        old_data = self.load_information()
        old_data.pop(name)
        with open(json_path, 'w') as file:
            json.dump(old_data, file)

    def get_trash_information(self):
        module_logger.debug('Start get information')
        new_trash_path = os.path.join(self.trash_path, 'trash_info.json')
        information = (f"Trash information:\n"
                       f"{'name':^30} | {'size':^10} | {'removal time':^30}\n")
        if not os.path.exists(new_trash_path):
            with open(new_trash_path) as file:
                json_file = json.load(file)
                if not json_file:
                    return 'Trash is empty'
                for files in json_file:
                    information = json_file[files]
                    information += (f"{information['file_name']:^30} | "
                                    f"{information['size']:^10} | "
                                    f"{information['removal_time']:^30}\n")
        return information

    def move_file(self, file_path, path_to_move):
        if os.path.isfile(file_path):
            new_file_path = os.path.join(path_to_move, os.path.basename(file_path))
            os.replace(file_path, new_file_path)
        elif os.path.isdir(file_path):
            dir_path = os.path.join(path_to_move, os.path.basename(file_path))
            for file in os.listdir(file_path):
                new_file_path = os.path.join(file_path, file)
                self.move_file(new_file_path, dir_path)
            os.rmdir(file_path)

    def remove(self, path):
        module_logger.debug('Start removing file to trash')
        space = os.statvfs(self.trash_path).f_bfree
        new_trash_path = os.path.join(self.trash_path, os.path.basename(path))
        my_trash = File(path, new_trash_path)
        if space < my_trash.size:
            module_logger.error('No free space')
        self.move_file(path, self.trash_path)
        self.save_information(my_trash)
        module_logger.info('File has been removed to the trash')

    def remove_forever(self, path):
        if os.path.isfile(path):
            module_logger.debug('Remove file')
            os.remove(path)
        else:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                self.remove_forever(file_path)
            module_logger.debug('Remove directory')
            os.rmdir(path)

    def remove_file_in_trash(self, file):
        module_logger.debug('Start of removing file from trash')
        trash_path = os.path.join(self.trash_path, file)
        data = self.load_information()
        self.remove_forever(trash_path)
        data.pop(f'{file}')
        self.update_information(file)
        module_logger.debug(f'File {file} removed')

    def clear_trash(self):
        module_logger.debug('Start cleaning trash')
        for file in os.listdir(self.trash_path):
            self.remove_file_in_trash(file)
        module_logger.debug('Trash cleared')
