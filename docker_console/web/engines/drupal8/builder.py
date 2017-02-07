import os
from docker_console.utils.console import run as run_cmd, message
from docker_console.web.engines.base.builder import BaseBuilder, cmd_options
from docker_console.web.engines.drupal8.docker import Docker
from docker_console.web.engines.drupal8.drush import Drush
from docker_console.web.engines.drupal8.drupal_settings import DrupalSettings
from docker_console.web.engines.drupal8.archive import Archive
from docker_console.web.engines.drupal8.tests import Tests

class Builder(BaseBuilder):

    def __init__(self, config):
        super(Builder, self).__init__(config)
        # check if executed command is global
        if self.config.steps_key not in self.config.global_commands:
            self.drupal_site = cmd_options.drupal_site
            if self.drupal_site not in self.config.DRUPAL:
                message("Site '%s' is not available in DRUPAL config in %s/docker_console/dc_settings.py" % (self.drupal_site, self.config.BUILD_PATH), 'error')
                exit(0)
            if os.environ.get("SITE_URI"):
                self.config.DRUPAL[self.drupal_site]['SITE_URI'] = os.environ.get("SITE_URI")
            self.config.drupal_site = self.drupal_site
            self.docker = Docker(self.config)
            self.tests = Tests(self.config)
            self.drush = Drush(self.config)
            self.drupal_settings = DrupalSettings(self.config)
            self.archive = Archive(self.config)

    def chmod_files(self):
        for site in self.config.DRUPAL:
            run_cmd('chmod -Rf 777 %s' % os.path.join(self.config.WEB['APP_ROOT'],
                                                      self.config.DRUPAL[site]['FILES_DST'], 'files'))

    def chmod_private_files(self):
        for site in self.config.DRUPAL:
            run_cmd('chmod -Rf 777 %s' % os.path.join(self.config.WEB['APP_ROOT'],
                                                      self.config.DRUPAL[site]['PRIVATE_FILES_DST'], 'private'))
