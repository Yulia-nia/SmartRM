import os
from datetime import datetime


def file_convert(size):
    for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.3f} {i}'
        else:
            size /= 1024.0


def get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        size = 0
        for path, subdir, files in os.walk(path):
            for file in files:
                filename = os.path.join(path, file)
                size += os.path.getsize(filename)
        return size


class File:
    def __init__(self, removal_path, current_path):
        self.removal_path = os.path.split(removal_path)[0]
        self.current_path = current_path
        self.removal_time = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")
        self.size = get_size(removal_path)
        self.file_name = os.path.basename(removal_path)

    def information(self):
        file_information = {
            'file_name': self.file_name,
            'file_size': file_convert(self.size),
            'removal_path': self.removal_path,
            'removal_time': self.removal_time,
        }
        return file_information
