
import tarfile
import os


class Archive:

    def __init__(self, config):
        self.config = config

    def _unpack(self, dest, src):
        pass

    @staticmethod
    def _sql_files(members):
        for tarinfo in members:
            if os.path.splitext(tarinfo.name)[1] == ".sql":
                yield tarinfo

    def unpack_db(self):
        src = os.path.join(self.config.BUILD_PATH, 'databases', self.config.DBDUMP_FILE)
        if src[-6:] == 'tar.gz':
            tar = tarfile.open(src)
            tar.extractall(self.config.TMP_PATH, self._sql_files(tar))
            tar.close()
            return [os.path.join(self.config.TMP_PATH, member.name) for member in self._sql_files(tar)]

    def unpack_files(self):
        src = os.path.join(self.config.BUILD_PATH, 'files', self.config.FILES_ARCHIVE)
        tar = tarfile.open(src)
        dest = os.path.join(self.config.DRUPAL_ROOT, self.config.FILES_DST)
        tar.extractall(dest)
        tar.close()
