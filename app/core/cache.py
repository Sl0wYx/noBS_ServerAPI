from app.core import common

class FileCache:
    def __init__(self, path, data, type, lmdate = None):
        self.path = path
        self.data = data
        self.type = type
        self.lmdate = lmdate

    def check(self) -> None:
        current_change = common.file_last_change(self.path)
        if self.lmdate != current_change:
            self.data = common.load_file(self.path, self.type)
            self.lmdate = current_change
