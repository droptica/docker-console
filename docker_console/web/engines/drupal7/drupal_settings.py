import os
import shutil

from docker_console.utils.console import message as msg


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

    def copy_settings(self, type):
        msg('Copy settings')
        dst = os.path.join(self.config.WEB['APP_ROOT'], 'sites/', self.config.DRUPAL[self.config.drupal_site]['SITE_DIRECTORY'])

        if hasattr(self.config, 'SETTINGS_TEMPLATE_SUBDIR') and self.config.DRUPAL[self.config.drupal_site]['SETTINGS_TEMPLATE_SUBDIR'] is not None:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, self.config.WEB['APP_CONF_LOCATION'], self.config.DRUPAL[self.config.drupal_site]['SETTINGS_TEMPLATE_SUBDIR'])
        else:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, self.config.WEB['APP_CONF_LOCATION'])

        #TODO: temporary solution, until drupal8 web engine will be ready
        if type == 'drupal8':
            for root, dirs, files in os.walk(settings_dir_path):
                for name in files:
                    src = os.path.join(root, name)
                    shutil.copyfile(
                        src,
                        os.path.join(dst, name)
                    )
        else:
            src = os.path.join(settings_dir_path, 'settings.php')
            shutil.copyfile(
                src,
                os.path.join(dst, 'settings.php')
            )
