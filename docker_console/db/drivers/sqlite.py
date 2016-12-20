from docker_console.utils.console import message as msg, run as run_cmd
from docker_console.db.drivers.base import BaseDatabase

class Database(BaseDatabase):

    def __init__(self, config, alias):
        super(Database, self).__init__(config, alias)
        # additional things

    def create_db(self):
        msg('Create DB')
        #TODO:

    def drop_db(self):
        msg('Drop DB')
        #TODO:

    def import_db(self):
        msg('Import DB')
        files = self.unpack_db()
        for file_path in files:
            self.import_file(file_path)

    def import_file(self, file_path):
        msg('Import sql file')
        #TODO:


