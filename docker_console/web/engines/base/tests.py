import os
import time
from docker_console.web.engines.base.docker import BaseDocker
from docker_console.utils.console import run as run_cmd, message
from docker_console.utils.files import create_dir_copy

class BaseTests(object):

    def __init__(self, config):
        self.config = config
        self.docker = BaseDocker(config)

    def codecept_run(self):
        cmd = ' '.join(self.config.args[2:])
        link_selenium = False
        if 'run' in cmd:
            link_selenium = True
        self.docker_codecept(cmd, link_selenium)

    def docker_codecept(self, cmd='', link_selenium=True):
        link_selenium_name = ''
        if link_selenium:
            run_cmd('docker run -d --name selenium-test-%s %s %s %s'
                    % (self.docker.base_alias, self.docker._get_links(), self.docker._get_hosts(), self.config.TESTS['IMAGES']['selenium_image'][0]))
            link_selenium_name = '--link selenium-test-%s:selenium' % self.docker.base_alias
            print "Waitng 5 sec."
            time.sleep(5)
        run_cmd('docker run --rm %s %s %s %s -w %s %s codecept %s'
            % (self.docker._get_volumes(), self.docker._get_links(), self.docker._get_hosts(),
               link_selenium_name, os.path.join('/app', self.config.TESTS['LOCATION']), self.config.TESTS['IMAGES']['codecept_image'][0], cmd))

    def tests_run(self):
        if ('selenium_image' not in self.config.TESTS['IMAGES']) or (
            'codecept_image' not in self.config.TESTS['IMAGES']):
            message('selenium_image or codecept_image is missing in TESTS config.', 'error')
            exit(0)
        if len(self.config.args) > 2:
            args = 'tests/' + ' '.join(self.config.args[2:])
        else:
            args = ''
        self.docker_codecept('build', False)
        self.docker_codecept('clean', False)
        self.docker_codecept('run %s --html --xml' % args)
        run_cmd('docker stop selenium-test-%s' % self.docker.base_alias)
        run_cmd('docker rm selenium-test-%s' % self.docker.base_alias)

    def tests_init(self):
        self.docker._copy_init_tpl_files('tests_init')

        message("Tests has been correctly initialized in this project.", 'info')
        message("If you wolud like to have source code of testing environment locally you need to run 'composer install' command in tests directory.", 'info')
