import os
import shutil

from .helpers import message as msg


class DrupalSettings:

    def __init__(self, config):
        self.config = config

    def chmod(self, dst):
        if os.path.isfile(dst):
            os.chmod(dst, 0777)
        elif os.path.isdir(dst):
            for root, dirs, files in os.walk(dst):
                for name in files:
                    os.chmod(os.path.join(root, name), 0777)

    def copy_settings(self):
        msg('Copy settings')
        dst = os.path.join(self.config.DRUPAL_ROOT, 'sites/', self.config.SITE_DIRECTORY)

        if hasattr(self.config, 'SETTINGS_DIR') and self.config.SETTINGS_DIR is not None:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, 'conf', self.config.SETTINGS_DIR)
        else:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, 'conf')

        for root, dirs, files in os.walk(settings_dir_path):
            for name in files:
                src = os.path.join(root, name)
                shutil.copyfile(
                    src,
                    os.path.join(dst, name)
                )
