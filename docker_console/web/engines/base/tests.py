import os
import sys
import time
import yaml
import itertools
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

    def docker_codecept(self, cmd='', parallel=False, group_name='', browser=''):
        selenium_container_name = 'selenium-test-%s' % self.docker.base_alias
        codeception_container_name = 'codeception-test-%s' % self.docker.base_alias
        if group_name:
            selenium_container_name += '-%s' % group_name
            codeception_container_name += '-%s' % group_name
        link_selenium_name = '--link %s:selenium' % selenium_container_name
        selenium_container_id = run_cmd('docker ps -a -q -f name=%s' % selenium_container_name,
                                        return_output=True)
        selenium_running_container_id = run_cmd('docker ps -q -f name=%s' % selenium_container_name,
                                                return_output=True)

        selenium_container_removed = False
        # Case when container is exited.
        if selenium_container_id and not selenium_running_container_id:
            run_cmd('docker rm %s' % selenium_container_name)
            selenium_container_removed = True

        browser_image = self.config.TESTS['IMAGES']['selenium_image'][0]
        if browser:
            if 'BROWSERS_IMAGES' in self.config.TESTS and browser in self.config.TESTS['BROWSERS_IMAGES']:
                browser_image_key = self.config.TESTS['BROWSERS_IMAGES'][browser]
                browser_image = self.config.TESTS['IMAGES'][browser_image_key][0]

        if not selenium_container_id or selenium_container_removed:
            run_cmd('docker run -d -v /dev/shm:/dev/shm --name %s %s %s %s %s %s'
                    % (selenium_container_name, self.docker.get_env_file(),
                       self.docker._get_extra_hosts(), self.docker._get_links(), self.docker._get_hosts(),
                       browser_image))
            print "Waiting 5 sec."
            time.sleep(5)

        if parallel:
            command_container_id = run_cmd('docker run -d --name %s %s %s %s %s %s %s -w %s %s codecept %s'
                                           % (codeception_container_name, self.docker.get_env_file(), self.docker._get_extra_hosts(),
                                              self.docker._get_volumes(), self.docker._get_links(), self.docker._get_hosts(),
                                              link_selenium_name, os.path.join('/app', self.config.TESTS['LOCATION']),
                                              self.config.TESTS['IMAGES']['codecept_image'][0], cmd),
                                           return_output=True)

            return command_container_id
        else:
            run_cmd('docker run --rm --name %s %s %s %s %s %s %s -w %s %s codecept %s'
                    % (codeception_container_name, self.docker.get_env_file(), self.docker._get_volumes(), self.docker._get_extra_hosts(), self.docker._get_links(), self.docker._get_hosts(),
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
        run_cmd('docker run --rm %s %s %s %s -w %s %s robo %s'
                % (self.docker._get_extra_hosts(), self.docker._get_volumes(), self.docker._get_links(), self.docker._get_hosts(),
                   os.path.join('/app', self.config.TESTS['LOCATION']),
                   self.config.TESTS['IMAGES']['codecept_image'][0], cmd))

    def product_dict(self, **kwargs):
        keys = kwargs.keys()
        vals = kwargs.values()
        for instance in itertools.product(*vals):
            yield dict(zip(keys, instance))

    def test_run_parallel(self):
        self.robo_init()
        split_type = cmd_options.parallel_group_by
        number_of_groups = int(cmd_options.parallel_test_groups)
        number_of_groups_iter = xrange(1, number_of_groups + 1)
        suites = cmd_options.parallel_test_suites.split(',')

        # todo: dont search for non existing container
        self.docker_codecept('build')
        self.docker_codecept('clean')

        command_containers_ids = {}
        # Run parallel testing of suites.
        if len(suites) > 1:
            for idx in range(len(suites)):
                suite = suites[idx]
                suite_number = idx + 1
                command_container_id = self.docker_codecept(
                    'run tests/%s --html report_parallel_group_%s.html --xml report_parallel_group_%s.xml' % (suite, suite_number, suite_number), parallel=True, group_name=str(suite_number))
                command_containers_ids[command_container_id] = {'finished': False, 'suite': suite}
        # Run parallel testing of groups.
        else:
            suites = []
            suites_config = {}
            groups = []
            groups_config = {}
            split_tests_command = 'parallel:split-by-%s %s' % (split_type, number_of_groups)
            if 'PARALLEL' in self.config.TESTS and 'SUITES' in self.config.TESTS['PARALLEL']:
                suites_config = self.config.TESTS['PARALLEL']['SUITES']
                suites = suites_config.keys()
            if 'PARALLEL' in self.config.TESTS and 'GROUPS' in self.config.TESTS['PARALLEL']:
                groups_config = self.config.TESTS['PARALLEL']['GROUPS']
                groups = groups_config.keys()

            if len(suites) > 0:
                split_tests_command += ' %s' % ','.join(suites)
                self.docker_robo(split_tests_command)
                groups_config = []
                for suite in suites_config:
                    groups_config_parts = {
                        'suite': [suite],
                        'group_number': number_of_groups_iter,
                    }
                    if 'BROWSERS' in suites_config[suite] and len(suites_config[suite]['BROWSERS']) > 0:
                        groups_config_parts['browser'] = suites_config[suite]['BROWSERS']
                    if 'ENVS' in suites_config[suite] and len(suites_config[suite]['ENVS']) > 0:
                        groups_config_parts['test_env'] = suites_config[suite]['ENVS']

                    groups_config_cartesian_prod = self.product_dict(**groups_config_parts)
                    groups_config += list(groups_config_cartesian_prod)

                for group_config in groups_config:
                    group_name = 'parallel_group_%s_%s' % (group_config['suite'], group_config['group_number'])
                    group_name_full = group_name
                    codecept_command_env = ''
                    browser = ''
                    if 'browser' in group_config:
                        browser = group_config['browser']
                        group_name_full += '_%s' % browser
                    if 'test_env' in group_config:
                        group_name_full += '_%s' % group_config['test_env']
                        codecept_command_env = ' --env %s' % group_config['test_env']
                    group_file_path = os.path.join(self.config.BUILD_PATH, self.config.TESTS['LOCATION'],
                                                   'tests/_output/%s' % group_name)
                    if os.path.isfile(group_file_path):
                        codecept_command = 'run --group %s --html report_%s.html --xml report_%s.xml' % (
                            group_name, group_name_full, group_name_full)
                        codecept_command += codecept_command_env
                        command_container_id = self.docker_codecept(codecept_command, parallel=True, group_name=group_name_full, browser=browser)
                        command_containers_ids[command_container_id] = {'finished': False,
                                                                        'group': group_name_full}

            elif len(groups) > 0:
                groups_config_all = []
                for group in groups_config:
                    groups_config_parts = {
                        'group': [group],
                    }
                    if 'BROWSERS' in groups_config[group] and len(groups_config[group]['BROWSERS']) > 0:
                        groups_config_parts['browser'] = groups_config[group]['BROWSERS']
                    if 'ENVS' in groups_config[group] and len(groups_config[group]['ENVS']) > 0:
                        groups_config_parts['test_env'] = groups_config[group]['ENVS']

                    groups_config_cartesian_prod = self.product_dict(**groups_config_parts)
                    groups_config_all += list(groups_config_cartesian_prod)

                for group_config in groups_config_all:
                    group_name = group_config['group']
                    group_name_full = 'parallel_group_%s' % (group_config['group'])
                    codecept_command_env = ''
                    browser = ''
                    if 'browser' in group_config:
                        browser = group_config['browser']
                        group_name_full += '_%s' % browser
                    if 'test_env' in group_config:
                        group_name_full += '_%s' % group_config['test_env']
                        test_env = group_config['test_env']
                        if browser:
                            test_env = '%s_%s' % (browser, test_env)
                        codecept_command_env = ' --env %s' % test_env

                    codecept_command = 'run --group %s --html report_%s.html --xml report_%s.xml' % (
                        group_name, group_name_full, group_name_full)
                    codecept_command += codecept_command_env
                    command_container_id = self.docker_codecept(codecept_command, parallel=True,
                                                                group_name=group_name_full, browser=browser)
                    command_containers_ids[command_container_id] = {'finished': False,
                                                                    'group': group_name_full}

            else:
                self.docker_robo(split_tests_command)
                for group in number_of_groups_iter:
                    group_file_path = os.path.join(self.config.BUILD_PATH, self.config.TESTS['LOCATION'], 'tests/_output/parallel_group_%s' % group)
                    if os.path.isfile(group_file_path):
                        command_container_id = self.docker_codecept(
                            'run --group parallel_group_%s --html report_parallel_group_%s.html --xml report_parallel_group_%s.xml' % (group, group, group),
                            parallel=True)
                        command_containers_ids[command_container_id] = {'finished': False, 'group': 'parallel_group_%s' % group}
        if len(command_containers_ids) > 0:
            number_of_groups = len(command_containers_ids)
            message('%s containers with parallel test groups has been started. '
                    'We need to wait until all of them will finish.' % number_of_groups, 'info')
            self.wait_for_all_containers_to_finish(command_containers_ids, 30, False)
            self.docker_robo('parallel:merge-htmlresults')
            self.docker_robo('parallel:merge-xmlresults')
        else:
            message('Seems like there is no group files created.', 'info')

        # Codeception containers will be stopped already.
        self.cleanup_tests(True, True)

    def cleanup_tests(self, clear_selenium=True, clear_codeception=True):
        if clear_selenium:
            run_cmd('docker stop $(docker ps -aq --filter name=selenium-test-%s*)' % self.docker.base_alias)
            run_cmd('docker rm $(docker ps -aq --filter name=selenium-test-%s*)' % self.docker.base_alias)
        if clear_codeception:
            run_cmd('docker stop $(docker ps -aq --filter name=codeception-test-%s*)' % self.docker.base_alias)
            run_cmd('docker rm $(docker ps -aq --filter name=codeception-test-%s*)' % self.docker.base_alias)

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

    def wait_for_all_containers_to_finish(self, command_containers_ids, check_interval=10, log_all=False):
        parallel_tests_finished = False
        while not parallel_tests_finished:
            print "\n\nWaiting %s sec for next test containers status checking." % check_interval
            time.sleep(check_interval)
            parallel_tests_finished = True
            for container_id in command_containers_ids:
                container_tests_info = ''
                for info_name in ['group', 'suite']:
                    if info_name in command_containers_ids[container_id]:
                        container_tests_info = '(%s: %s)' % (info_name, command_containers_ids[container_id][info_name])
                        break

                test_running = run_cmd('docker ps -q -f id=%s' % container_id, return_output=True, print_message=False)
                if command_containers_ids[container_id]['finished']:
                    if log_all:
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
