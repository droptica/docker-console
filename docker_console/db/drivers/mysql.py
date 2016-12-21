import os
import tarfile
from docker_console.utils.console import message as msg, run as run_cmd
from docker_console.db.drivers.base import BaseDatabase

class Database(BaseDatabase):

    def __init__(self, config, alias):
        super(Database, self).__init__(config, alias)
        # additional things

    def create_db(self):
        msg('Create DB')
        run_cmd('mysql -h %s -u %s -p%s -e "CREATE DATABASE IF NOT EXISTS %s;"' % (self.HOST, self.ROOT_USER, self.ROOT_PASS, self.NAME))

    def drop_db(self):
        msg('Drop DB')
        run_cmd('mysql -h %s -u %s -p%s -e "DROP DATABASE %s;"' % (self.HOST, self.ROOT_USER, self.ROOT_PASS, self.NAME))

    def import_db(self):
        msg('Import DB')
        files = self.unpack_db()
        for file_path in files:
            self.import_file(file_path)

    def import_file(self, file_path):
        run_cmd('mysql -h %s -u %s -p%s %s < %s' % (self.HOST, self.ROOT_USER, self.ROOT_PASS, self.NAME, file_path))

    def export_db(self):
        msg('Export DB')
        filename = 'database_dump_' + self.config.TIME_STR + '.sql'
        dump_path = os.path.join(self.config.BUILD_PATH, self.DUMP_EXPORT_LOCATION, filename)
        run_cmd('mysqldump -h %s -u %s -p%s %s > %s' % (self.HOST, self.ROOT_USER, self.ROOT_PASS, self.NAME, dump_path))
        tar = tarfile.open(dump_path + '.tar.gz', 'w:gz')
        tar.add(dump_path, filename)
        tar.close()
        os.remove(dump_path)
