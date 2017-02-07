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

    def copy_settings(self, type = 'drupal7', remove_existing=False):
        msg('Copy settings')
        dst = os.path.join(self.config.WEB['APP_ROOT'], 'sites/', self.config.DRUPAL[self.config.drupal_site]['SITE_DIRECTORY'])

        if 'SETTINGS_TEMPLATE_SUBDIR' in self.config.DRUPAL[self.config.drupal_site] and self.config.DRUPAL[self.config.drupal_site]['SETTINGS_TEMPLATE_SUBDIR'] is not None:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, self.config.WEB['APP_CONF_LOCATION'], self.config.DRUPAL[self.config.drupal_site]['SETTINGS_TEMPLATE_SUBDIR'])
        else:
            settings_dir_path = os.path.join(self.config.BUILD_PATH, self.config.WEB['APP_CONF_LOCATION'])

        if type == 'drupal8':
            for root, dirs, files in os.walk(settings_dir_path):
                for name in files:
                    dst_file = os.path.join(dst, name)
                    if remove_existing and os.path.exists(dst_file):
                        os.remove(dst_file)
                    src = os.path.join(root, name)
                    shutil.copyfile(
                        src,
                        dst_file
                    )
        else:
            src = os.path.join(settings_dir_path, 'settings.php')
            dst_file = os.path.join(dst, 'settings.php')
            if remove_existing and os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copyfile(
                src,
                dst_file
            )
