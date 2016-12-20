import os
from docker_console.utils.console import run as run_cmd
from docker_console.web.engines.base.builder import BaseBuilder
from docker_console.web.engines.drupal7.docker import Docker
from docker_console.web.engines.drupal7.drush import Drush
from docker_console.web.engines.drupal7.drupal_settings import DrupalSettings
from docker_console.web.engines.drupal7.archive import Archive
from docker_console.web.engines.drupal7.tests import Tests

class Builder(BaseBuilder):

    def __init__(self, config):
        super(Builder, self).__init__(config)

        if os.environ.get("SITE_URI"):
            self.config.DRUPAL['SITE_URI'] = os.environ.get("SITE_URI")
        self.docker = Docker(self.config)
        self.tests = Tests(self.config)
        self.drush = Drush(self.config)
        self.drupal_settings = DrupalSettings(self.config)
        self.archive = Archive(self.config)

    def chmod_files(self):
        run_cmd('chmod 777 -Rf %s' % os.path.join(self.config.WEB_APP_ROOT, self.config.DRUPAL['FILES_DST'], 'files'))
