from docker_console.utils.console import message as msg, run as run_cmd
from docker_console.db.drivers.base import BaseDatabase

class Database(BaseDatabase):

    def __init__(self, config, alias):
        super(Database, self).__init__(config, alias)
        # additional things

    def create_db(self):
        msg('Create DB')
        run_cmd('mysql -h %s -u root -p%s -e "CREATE DATABASE IF NOT EXISTS %s;"' % (self.host, self.root_password, self.db))

    def drop_db(self):
        msg('Drop DB')
        run_cmd('mysql -h %s -u root -p%s -e "DROP DATABASE %s;"' % (self.host, self.root_password, self.db))

    def import_db(self):
        msg('Import DB')
        files = self.unpack_db()
        for file_path in files:
            self.import_file(file_path)

    def import_file(self, file_path):
        run_cmd('mysql -h %s -u root -p%s %s < %s' % (self.host, self.root_password, self.db, file_path))

