import os
import shutil
from docker_console.utils.files import unpack_tar
from docker_console.utils.console import message

class Archive:

    def __init__(self, config):
        self.config = config

    def unpack_files(self, remove_existing=False):
        message('Unpacking files')
        src = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['FILES_ARCHIVE'])
        dest = os.path.join(self.config.WEB['APP_ROOT'], self.config.DRUPAL[self.config.drupal_site]['FILES_DST'])

        if remove_existing and os.path.exists(os.path.join(dest, 'files')):
            shutil.rmtree(os.path.join(dest, 'files'))

        unpack_tar(src, dest)
        os.system("chmod -Rf 777 %s" % os.path.join(dest, 'files'))

    def unpack_private_files(self, remove_existing=False):
        message('Unpacking private files')
        src = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['PRIVATE_FILES_ARCHIVE'])
        dest = os.path.join(self.config.WEB['APP_ROOT'], self.config.DRUPAL[self.config.drupal_site]['PRIVATE_FILES_DST'])

        if remove_existing and os.path.exists(os.path.join(dest, 'private')):
            shutil.rmtree(os.path.join(dest, 'private'))

        unpack_tar(src, dest)
        os.system("chmod -Rf 777 %s" % os.path.join(dest, 'private'))
