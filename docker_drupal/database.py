import os
import tarfile
from .archive import Archive
from .helpers import message as msg, run as run_cmd


class Database:

    def __init__(self, config, drush):
        self.config = config
        self.host = config.DBHOST
        self.db = config.DB_NAME
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.root_password = config.ROOT_PASS
        self.drush = drush
        self.archive = Archive(config)

    def create_db(self):
        msg('Create DB')
        run_cmd('mysql -h %s -u root -p%s -e "CREATE DATABASE IF NOT EXISTS %s;"' % (self.host, self.root_password, self.db))

    def drop_db(self):
        msg('Drop DB')
        run_cmd('mysql -h %s -u root -p%s -e "DROP DATABASE %s;"' % (self.host, self.root_password, self.db))

    def import_db(self):
        msg('Import DB')
        files = self.archive.unpack_db()
        for file_path in files:
            self.drush_import(file_path)

    def mysql_import(self, file_path):
        run_cmd('mysql -h %s -u %s -p%s %s < %s' %
            (
                 self.host,
                 self.user,
                 self.password,
                 self.db,
                 file_path
            )
        )

    def drush_import(self, file_path):
        self.drush.run('sql-cli <%s' % file_path)

    def drush_drop_tables(self):
        msg('Drop Tables')
        self.drush.run('sql-drop -y')

    def dump(self, path):
        time = self.config.TIME_STR
        if not path[-1] == '/':
            path += '/'
        self.drush.run('sql-dump >%s', path + time + '.sql')
        return path + time + '.sql'

    def create_dump(self):
        dump = self.db.dump(self.config.TMP_PATH)
        tar = tarfile.TarFile(os.path.join(self.config.BUILD_PATH, 'databases', ))
        tar.add(dump)