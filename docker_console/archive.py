import tarfile
import os


class Archive:

    def __init__(self, config):
        self.config = config

    def _unpack(self, src, dest):
        if src[-6:] == 'tar.gz':
            tar = tarfile.open(src)
            tar.extractall(dest)
            tar.close()
            return tar

    @staticmethod
    def _sql_files(members):
        for tarinfo in members:
            if os.path.splitext(tarinfo.name)[1] == ".sql" or os.path.splitext(tarinfo.name)[1] == ".msql":
                yield tarinfo

    def unpack_db(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.DBDUMP_FILE)
        tar = self._unpack(src, self.config.TMP_PATH)
        return [os.path.join(self.config.TMP_PATH, member.name) for member in self._sql_files(tar)]

    def unpack_files(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.FILES_ARCHIVE)
        dest = os.path.join(self.config.DRUPAL_ROOT, self.config.FILES_DST)
        self._unpack(src, dest)

    def unpack_private_files(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.PRIVATE_FILES_ARCHIVE)
        dest = os.path.join(self.config.DRUPAL_ROOT, self.config.PRIVATE_FILES_DST)
        self._unpack(src, dest)
