import os
from docker_console.utils.files import unpack_tar, sql_files

class BaseDatabase(object):

    def __init__(self, config, alias):
        self.config = config
        self.alias = alias
        self.host = config.DB[alias]['HOST']
        self.db = config.DB[alias]['NAME']
        self.user = config.DB[alias]['USER']
        self.password = config.DB[alias]['PASS']
        self.root_password = config.DB[alias]['ROOT_PASS']

    def unpack_db(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.DB[self.alias]['DUMP_IMPORT_FILE'])
        tar = unpack_tar(src, self.config.TMP_PATH)
        return [os.path.join(self.config.TMP_PATH, member.name) for member in sql_files(tar)]
