import os
from docker_console.utils.files import unpack_tar

class Archive:

    def __init__(self, config):
        self.config = config

    def unpack_files(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['FILES_ARCHIVE'])
        dest = os.path.join(self.config.WEB['APP_ROOT'], self.config.DRUPAL[self.config.drupal_site]['FILES_DST'])
        unpack_tar(src, dest)

    def unpack_private_files(self):
        src = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['PRIVATE_FILES_ARCHIVE'])
        dest = os.path.join(self.config.WEB['APP_ROOT'], self.config.DRUPAL[self.config.drupal_site]['PRIVATE_FILES_DST'])
        unpack_tar(src, dest)
