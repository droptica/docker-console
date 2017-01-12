from docker_console.web.engines.base.tests import BaseTests
from docker_console.web.engines.drupal8.docker import Docker

class Tests(BaseTests):

    def __init__(self, config):
        super(Tests, self).__init__(config)
        self.docker = Docker(config)
