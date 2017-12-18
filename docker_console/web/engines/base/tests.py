import os
import sys
import time
import yaml
from docker_console import cmd_options
from docker_console.web.engines.base.docker import BaseDocker
from docker_console.utils.console import run as run_cmd, message
from docker_console.utils.files import copy_file


class BaseTests(object):
    def __init__(self, config):
        self.config = config
        self.docker = BaseDocker(config)

    def codecept_run(self):
        cmd = ' '.join(self.config.args[2:])
        self.docker_codecept(cmd)

    def docker_codecept(self, cmd='', parallel=False):
        link_selenium_name = '--link selenium-test-%s:selenium' % self.docker.base_alias
        selenium_container_id = run_cmd('docker ps -a -q -f name=selenium-test-%s' % self.docker.base_alias,
                                        return_output=True)
        selenium_running_container_id = run_cmd('docker ps -q -f name=selenium-test-%s' % self.docker.base_alias,
                                                return_output=True)

        selenium_container_removed = False
        # Case when container is exited.
        if selenium_container_id and not selenium_running_container_id:
            run_cmd('docker rm selenium-test-%s' % self.docker.base_alias)
            selenium_container_removed = True

        if not selenium_container_id or selenium_container_removed:
            run_cmd('docker run -d --name selenium-test-%s %s %s %s'
                    % (self.docker.base_alias, self.docker._get_links(), self.docker._get_hosts(),
                       self.config.TESTS['IMAGES']['selenium_image'][0]))
            print "Waiting 5 sec."
            time.sleep(5)

        if parallel:
            command_container_id = run_cmd('docker run -d %s %s %s %s -w %s %s codecept %s'
                                           % (self.docker._get_volumes(), self.docker._get_links(),
                                              self.docker._get_hosts(),
                                              link_selenium_name, os.path.join('/app', self.config.TESTS['LOCATION']),
                                              self.config.TESTS['IMAGES']['codecept_image'][0], cmd),
                                           return_output=True)

            return command_container_id
        else:
            run_cmd('docker run --rm %s %s %s %s -w %s %s codecept %s'
                    % (self.docker._get_volumes(), self.docker._get_links(), self.docker._get_hosts(),
                       link_selenium_name, os.path.join('/app', self.config.TESTS['LOCATION']),
                       self.config.TESTS['IMAGES']['codecept_image'][0], cmd))

    def robo_run(self):
        cmd = ' '.join(self.config.args[2:])
        self.docker_robo(cmd)

    def robo_init(self):
        self.copy_robo_file(cmd_options.docker_init_replace_conf)
        codeception_config_path = os.path.join(self.config.BUILD_PATH, self.config.TESTS['LOCATION'], 'codeception.yml')
        codeception_config_yaml = open(codeception_config_path)
        codeception_config = yaml.load(codeception_config_yaml)
        codeception_config_yaml.close()
        try:
            if 'groups' not in codeception_config:
                codeception_config['groups'] = {
                    'parallel_group_*': 'tests/_output/parallel_group_*'
                }
            elif 'parallel_group_*' not in codeception_config['groups']:
                codeception_config['groups']['parallel_group_*'] = 'tests/_output/parallel_group_*'

            codeception_config_yaml = open(codeception_config_path, 'w')
            yaml.dump(codeception_config, codeception_config_yaml, default_flow_style=False)
            codeception_config_yaml.close()
        except:
            pass

    def copy_robo_file(self, force_replace = False):
        robo_file_path = os.path.join(os.path.dirname(sys.modules['docker_console'].__file__), 'tests_init_templates',
                                      'RoboFile.php')
        copy_file(robo_file_path, os.path.join(self.config.BUILD_PATH, self.config.TESTS['LOCATION'], 'RoboFile.php'),
                  force_replace)

    def docker_robo(self, cmd):
        run_cmd('docker run --rm %s %s %s -w %s %s robo %s'
                % (self.docker._get_volumes(), self.docker._get_links(), self.docker._get_hosts(),
                   os.path.join('/app', self.config.TESTS['LOCATION']),
                   self.config.TESTS['IMAGES']['codecept_image'][0], cmd))

    def test_run_parallel(self):
        self.robo_init()
        split_type = cmd_options.parallel_group_by
        number_of_groups = int(cmd_options.parallel_test_groups)
        suites = cmd_options.parallel_test_suites.split(',')

        self.docker_codecept('build')
        self.docker_codecept('clean')

        command_containers_ids = {}
        # Run parallel testing of suites.
        if len(suites) > 1:
            number_of_groups = len(suites)
            for idx in range(len(suites)):
                suite = suites[idx]
                suite_number = idx + 1
                command_container_id = self.docker_codecept(
                    'run tests/%s --html report_parallel_%s.html --xml report_parallel_%s.xml' % (suite, suite_number, suite_number), parallel=True)
                command_containers_ids[command_container_id] = {'finished': False, 'suite': suite}
        # Run parallel testing of groups.
        else:
            self.docker_robo('parallel:split-by-%s %s' % (split_type, number_of_groups))
            for group in xrange(1, number_of_groups + 1):
                group_file_path = os.path.join(self.config.BUILD_PATH, self.config.TESTS['LOCATION'], 'tests/_output/parallel_group_%s' % group)
                if os.path.isfile(group_file_path):
                    command_container_id = self.docker_codecept(
                        'run --group parallel_group_%s --html report_parallel_%s.html --xml report_parallel_%s.xml -vvv' % (group, group, group),
                        parallel=True)
                    command_containers_ids[command_container_id] = {'finished': False, 'group': 'parallel_group_%s' % group}
        if len(command_containers_ids) > 0:
            number_of_groups = len(command_containers_ids)
            message('%s containers with parallel test groups has been started. '
                    'We need to wait until all of them will finish.' % number_of_groups, 'info')
            self.wait_for_all_containers_to_finish(command_containers_ids)
            self.docker_robo('parallel:merge-htmlresults %s' % (number_of_groups))
            self.docker_robo('parallel:merge-xmlresults %s' % (number_of_groups))
        else:
            message('Seems like there is no group files created.', 'info')

        run_cmd('docker stop selenium-test-%s' % self.docker.base_alias)
        run_cmd('docker rm selenium-test-%s' % self.docker.base_alias)

    def tests_run(self):
        if ('selenium_image' not in self.config.TESTS['IMAGES']) or (
            'codecept_image' not in self.config.TESTS['IMAGES']):
            message('selenium_image or codecept_image is missing in TESTS config.', 'error')
            exit(0)
        if len(self.config.args) > 2:
            args = 'tests/' + ' '.join(self.config.args[2:])
        else:
            args = ''
        self.docker_codecept('build')
        self.docker_codecept('clean')
        self.docker_codecept('run %s --html --xml' % args)
        run_cmd('docker stop selenium-test-%s' % self.docker.base_alias)
        run_cmd('docker rm selenium-test-%s' % self.docker.base_alias)

    def wait_for_all_containers_to_finish(self, command_containers_ids):
        parallel_tests_finished = False
        while not parallel_tests_finished:
            print "\n\nWaiting 10 sec for next test status checking."
            time.sleep(10)
            parallel_tests_finished = True
            for container_id in command_containers_ids:
                container_tests_info = ''
                for info_name in ['group', 'suite']:
                    if info_name in command_containers_ids[container_id]:
                        container_tests_info = '(%s: %s)' % (info_name, command_containers_ids[container_id][info_name])
                        break

                test_running = run_cmd('docker ps -q -f id=%s' % container_id, return_output=True)
                if command_containers_ids[container_id]['finished']:
                    print "Container %s finished %s" % (container_id, container_tests_info)
                elif not test_running:
                    command_containers_ids[container_id]['finished'] = True
                    print "Container %s finished right now %s" % (container_id, container_tests_info)
                else:
                    print "Container %s still running %s" % (container_id, container_tests_info)
                    parallel_tests_finished = False

            if parallel_tests_finished:
                message('All containers finished', 'info')

    def tests_init(self):
        self.docker._copy_init_tpl_files('tests_init')

        message("Tests has been correctly initialized in this project.", 'info')
        message(
            "If you wolud like to have source code of testing environment locally you need to run 'composer install' command in tests directory.",
            'info')
