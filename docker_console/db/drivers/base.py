import os
from docker_console.utils.files import unpack_tar, sql_files

class BaseDatabase(object):

    def __init__(self, config, alias):
        self.config = config
        self.alias = alias
        for setting in config.DB[alias]:
            setting_value = config.DB[alias][setting]
            setattr(self, setting, setting_value)

    def unpack_db(self):
        src = os.path.join(self.config.BUILD_PATH, self.DUMP_IMPORT_FILE)
        tar = unpack_tar(src, self.config.WEB['TMP_PATH'])
        return [os.path.join(self.config.WEB['TMP_PATH'], member.name) for member in sql_files(tar)]
