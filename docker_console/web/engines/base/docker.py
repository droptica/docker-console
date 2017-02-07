import os
import sys
import re
import yaml
from distutils import dir_util
from docker_console import cmd_options
from docker_console.bash_completion import setup_autocomplete
from docker_console.utils.console import run as run_cmd, call as call_cmd, message
from docker_console.utils.files import create_dir_copy


class BaseDocker(object):

    def __init__(self, config):
        self.config = config
        if self.config.ENV:
            env = '-' + self.config.ENV
        else:
            env = ''
        self.compose_path = os.path.join(self.config.BUILD_PATH, 'docker-compose.yml')
        if not os.path.exists(self.compose_path) and self.config.steps_key not in self.config.global_commands:
            message('docker-compose.yml file is missing. To run docker-console you need to do one of this things:\n'
                        'go to project wrapper path, \n'
                        'specify absolute path to project wrapper by -p (--docker-run-path) option\n'
                        'create alias with your project wrapper path in ~/.docker_console/aliases (then docker-console @project_dev)', 'warning')
            exit(0)
        self.compose_template_path = os.path.join(self.config.BUILD_PATH, 'docker-compose' + env + '-template.yml')
        self.base_alias = self.get_project_name(self.config.BUILD_PATH)

    def get_project_name(self, working_dir, project_name=None):
        def normalize_name(name):
            return re.sub(r'[^a-z0-9]', '', name.lower())

        project_name = project_name or os.environ.get('COMPOSE_PROJECT_NAME')
        if project_name:
            return normalize_name(project_name)

        project = os.path.basename(os.path.abspath(working_dir))
        if project:
            return normalize_name(project)

        return 'default'

    def docker_chown(self, path, uid):
        return self.docker_run('chown -Rf %s:%s %s' % (uid, uid, path))

    def docker_chmod(self, path):
        return self.docker_run('chmod -Rf 777 %s' % path)

    def config_prepare(self):
        if not os.path.isfile(self.compose_template_path):
            return
        config_file = open(self.compose_template_path, 'r')
        content = config_file.read()
        config_file.close()
        replacments = re.findall('{{([^{]+)}}', content)
        if replacments is not None:
            for replace in replacments:
                env = os.environ.get(replace.strip())
                if not env:
                    env = ''
                content = content.replace("{{%s}}" % replace, env)
        config_file = open(self.compose_path, 'w')
        config_file.write(content)
        config_file.close()

    def _get_links(self):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        links = []
        for container in docker_config:
            if 'links' in docker_config[container]:
                for key in docker_config[container]['links']:
                    if key not in links:
                        links.append(key)
        return ' '.join(['--link ' + self._container_alias(x) for x in links])

    def _get_hosts(self):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        hosts = []
        for container in docker_config:
            try:
                for host in docker_config[container]['environment']['VIRTUAL_HOST'].split(','):
                    hosts.append('--link %s:%s' % ('%s_%s_1' % (self.base_alias, container),
                                                   host.strip()))
                hosts.append('--link %s:%s' % ('%s_%s_1' % (self.base_alias, container),
                                               container))

            except:
                pass
        return ' '.join(hosts)

    def _get_volumes(self):
        volumes = []
        volumes.append('-v %s:%s' % (self.config.BUILD_PATH, '/app'))
        return ' '.join(volumes)

    def _container_alias(self, value):
        tmp = value.split(':')
        tmp[0] = '%s_%s_1' % (self.base_alias, tmp[0])
        return ':'.join(tmp)

    def docker_run(self, cmd):
        run_cmd(self.docker_command() + ' ' + cmd)

    def docker_up(self):
        run_cmd('docker-compose up -d', cwd=self.config.BUILD_PATH)

    def docker_update_images(self):
        run_cmd('docker-compose stop', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose rm -f', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose pull', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose build', cwd=self.config.BUILD_PATH)

        ALL_DEV_DOCKER_IMAGES = []
        for image in self.config.DEV_DOCKER_IMAGES:
            if isinstance(self.config.DEV_DOCKER_IMAGES[image], tuple):
                ALL_DEV_DOCKER_IMAGES.append(self.config.DEV_DOCKER_IMAGES[image])
            elif isinstance(self.config.DEV_DOCKER_IMAGES[image], list):
                ALL_DEV_DOCKER_IMAGES += self.config.DEV_DOCKER_IMAGES[image]

        for image in self.config.TESTS['IMAGES']:
            if isinstance(self.config.TESTS['IMAGES'][image], tuple):
                ALL_DEV_DOCKER_IMAGES.append(self.config.TESTS['IMAGES'][image])
            elif isinstance(self.config.TESTS['IMAGES'][image], list):
                ALL_DEV_DOCKER_IMAGES += self.config.TESTS['IMAGES'][image]

        for DEV_DOCKER_IMAGE, DEV_DOCKER_IMAGE_DOCKERFILE in ALL_DEV_DOCKER_IMAGES:
            run_cmd('docker pull %s' % DEV_DOCKER_IMAGE)
            if DEV_DOCKER_IMAGE_DOCKERFILE is not None:
                run_cmd('docker build --no-cache -t %s %s' %
                        (DEV_DOCKER_IMAGE, os.path.join(self.config.BUILD_PATH, DEV_DOCKER_IMAGE_DOCKERFILE)),
                        cwd=self.config.BUILD_PATH)

        run_cmd('docker-compose up -d', cwd=self.config.BUILD_PATH)

    def docker_stop(self):
        run_cmd('docker-compose stop', cwd=self.config.BUILD_PATH)

    def docker_rm(self):
        run_cmd('docker-compose rm -f', cwd=self.config.BUILD_PATH)

    def docker_rmi(self):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        docker_comose.close()
        images_to_remove = []
        for container in docker_config:
            config = docker_config[container]
            if 'image' in config:
                images_to_remove.append(docker_config[container]['image'])
            elif 'build' in config:
                images_to_remove.append('%s_%s' % (self.base_alias, container))

        run_cmd('docker rmi %s' % (' ' .join(images_to_remove)), cwd=self.config.BUILD_PATH)

    def docker_restart(self):
        self.docker_stop()
        self.docker_up()

    def docker_command(self):
        if self.config.NO_INTERACTIVE:
            return 'docker run --rm %s %s %s %s' % (self._get_volumes(), self._get_links(), self._get_hosts(),
                                                        self.config.DEV_DOCKER_IMAGES['default'][0])
        else:
            return 'docker run --rm -it %s %s %s %s' % (self._get_volumes(), self._get_links(), self._get_hosts(),
                                        self.config.DEV_DOCKER_IMAGES['default'][0])

    def get_container_ip(self):
        web_container_alias = self._container_alias("web:web").split(':')[0]
        if not run_cmd('docker ps -q -f name=%s' % web_container_alias, return_output=True):
            message("Docker is not up for this project and it will be started. It is required to add config entry to /etc/hosts.", 'info')
            self.docker_up()
        web_container_ip_address = run_cmd('docker inspect --format "{{ .NetworkSettings.IPAddress }}" %s'
                                               % web_container_alias,
                                               return_output=True)
        return web_container_ip_address

    def get_nginx_proxy_ip(self):
        if not run_cmd('docker ps -q -f name=nginx-proxy', return_output=True):
            return False
        container_ip_address = run_cmd('docker inspect --format "{{ .NetworkSettings.IPAddress }}" nginx-proxy',
                                               return_output=True)
        return container_ip_address

    def show_ip(self):
        print self.get_container_ip()

    def show_nginx_proxy_ip(self):
        print self.get_nginx_proxy_ip()

    def docker_shell(self):
        docker_command = self.docker_command()
        if cmd_options.docker_container:
            try:
                docker_command = "docker exec -it %s bash" % self._container_alias(cmd_options.docker_container+":").split(':')[0]
            except:
                pass
        print docker_command

        if cmd_options.docker_shell_run:
            call_cmd(docker_command)

    def docker_add_host(self, container, host):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        docker_comose.close()
        try:
            docker_config[container]['environment']['VIRTUAL_HOST'] += ',' + host
            docker_comose = open(self.compose_path, 'w')
            yaml.dump(docker_config, docker_comose)
            docker_comose.close()
        except:
            pass

    def docker_get_compose_option_value(self, container, option_name, group=None):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        docker_comose.close()
        try:
            if group:
                return docker_config[container][group][option_name]
            else:
                return docker_config[container][option_name]
        except:
            return ''

    def docker_set_compose_option_value(self, container, option_name, group=None, value=None):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        docker_comose.close()
        try:
            if group:
                if value is not None:
                    docker_config[container][group][option_name] = value
                else:
                    del docker_config[container][group][option_name]
            else:
                if value is not None:
                    docker_config[container][option_name] = value
                else:
                    del docker_config[container][option_name]

            docker_comose = open(self.compose_path, 'w')
            yaml.dump(docker_config, docker_comose)
            docker_comose.close()
        except Exception as exception:
            print "can't set option %s, check order and values of passed args: %s" % (option_name, str(exception))

    def _init_tpl_render(self, src):
        config_file = open(src, 'r')
        content = config_file.read()
        config_file.close()
        context = {
            '{{HOST}}': self.base_alias + '.dev'
        }
        for key in context:
            value = context[key]
            content = content.replace(key, value)
        dst = src[:-len('-tpl')]
        config_file = open(dst, 'w')
        config_file.write(content)
        config_file.close()
        os.remove(src)

    def _copy_init_tpl_files(self, type):
        init_tpl = {
            'docker_init': {
                'default_init_tpl_dir': 'docker_init_templates',
                'custom_init_tpl_dir': 'custom_docker_init_templates',
                'info_msg': 'You have to specify docker init template using option --tpl',
                'available_msg': 'Available %s docker init templates: %s',
                'missing_msg': "Docker init template '%s' does not exists."
            },
            'tests_init': {
                'default_init_tpl_dir': 'tests_init_templates',
                'custom_init_tpl_dir': 'custom_tests_init_templates',
                'info_msg': 'You have to specify tests init template using option --tpl',
                'available_msg': 'Available %s tests init templates: %s',
                'missing_msg': "Tests init template '%s' does not exists."
            }
        }
        default_init_tpl_path = os.path.join(os.path.dirname(sys.modules['docker_console'].__file__), init_tpl[type]['default_init_tpl_dir'])
        custom_init_tpl_path = os.path.join(os.path.expanduser('~'), '.docker_console', init_tpl[type]['custom_init_tpl_dir'])
        all_default_templates = []
        all_custom_templates = []
        for item in os.listdir(default_init_tpl_path):
            if os.path.isdir(os.path.join(default_init_tpl_path, item)):
                all_default_templates.append(item)
        if os.path.exists(custom_init_tpl_path):
            for item in os.listdir(custom_init_tpl_path):
                if os.path.isdir(os.path.join(custom_init_tpl_path, item)):
                    all_custom_templates.append(item)

        if not cmd_options.init_template:
            message(init_tpl[type]['info_msg'], 'error')
            message(init_tpl[type]['available_msg'] % ('default', ', '.join(all_default_templates)), 'error')
            if len(all_custom_templates):
                message(init_tpl[type]['available_msg'] % ('custom', ', '.join(all_custom_templates)), 'error')
            exit(0)
        if cmd_options.init_template and cmd_options.init_template not in all_default_templates and cmd_options.init_template not in all_custom_templates:
            message(init_tpl[type]['missing_msg'] % cmd_options.init_template, 'error')
            message(init_tpl[type]['available_msg'] % ('default', ', '.join(all_default_templates)), 'error')
            if len(all_custom_templates):
                message(init_tpl[type]['available_msg'] % ('custom', ', '.join(all_custom_templates)), 'error')
            exit(0)

        if cmd_options.init_template in all_custom_templates:
            temp_path = create_dir_copy(os.path.join(custom_init_tpl_path, cmd_options.init_template))
        else:
            temp_path = create_dir_copy(os.path.join(default_init_tpl_path, cmd_options.init_template))

        for root, dirs, files in os.walk(temp_path):
            for name in files:
                if name.endswith('-tpl'):
                    src = os.path.join(root, name)
                    self._init_tpl_render(src)

        create_dir_copy(temp_path, self.config.BUILD_PATH, cmd_options.docker_init_replace_conf)
        dir_util.remove_tree(temp_path)

    def docker_init(self):
        self._copy_init_tpl_files('docker_init')
        app_path = os.path.join(self.config.BUILD_PATH, 'app')
        if not os.path.exists(app_path):
            os.mkdir(app_path)
        message("Docker has been correctly initialized in this project.", 'info')
        message("If you want to automatically add config entry for this project to /etc/hosts, please run 'docker-console add-host-to-etc-hosts' command", 'info')

    def add_entry_to_etc_hosts(self):
        try:
            nginx_proxy_ip = self.get_nginx_proxy_ip()
            if not nginx_proxy_ip:
                raise Exception

            with open('/etc/hosts', 'rt') as f:
                host_names = self.docker_get_compose_option_value('web', 'VIRTUAL_HOST', 'environment').replace(',', ' ')
                phpmyadmin_host = self.docker_get_compose_option_value('phpmyadmin', 'VIRTUAL_HOST', 'environment').replace(',', ' ')
                if phpmyadmin_host:
                    host_names += ' ' + phpmyadmin_host
                s = f.read()
                if not host_names in s:
                    s += "\n%s\t\t%s\n" % (nginx_proxy_ip, host_names)
                    with open('/tmp/etc_hosts.tmp', 'wt') as outf:
                        outf.write(s)

                    run_cmd('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

                    message("Config entry with hosts: >>>%s<<< has beed succesfully added to /etc/hosts file." % host_names, 'info')
                else:
                    message("Config entry with hosts: >>>%s<<< was not added to /etc/hosts file because it already contains entry with this hosts" % host_names, 'info')
        except:
            message('Config entry was not added to /etc/hosts.', 'warning')

    def chown(self):
        self.docker_chown(self.config.WEB['APP_LOCATION'], os.getuid())

    def add_host(self):
        container = self.config.args[2]
        host = self.config.args[3]
        self.docker_add_host(container, host)

    def setfacl(self):
        if os.getuid():
            self.docker_run('setfacl -Rm g:www-data:rwX %s' % self.config.WEB['APP_LOCATION'])
            self.docker_run('setfacl -d -Rm g:www-data:rwX  %s' % self.config.WEB['APP_LOCATION'])
        else:
            run_cmd('setfacl -Rm g:www-data:rwX %s' % self.config.WEB['APP_LOCATION'])
            run_cmd('setfacl -d -Rm g:www-data:rwX  %s' % self.config.WEB['APP_LOCATION'])

    def cleanup(self):
        if run_cmd('docker ps -a -q -f status=exited', return_output=True):
            # remove exited containers
            run_cmd('docker rm -v $(docker ps -a -q -f status=exited)')

        if run_cmd('docker images -f "dangling=true" -q', return_output=True):
            # remove unwanted dangling images
            run_cmd('docker rmi $(docker images -f "dangling=true" -q)')

        # remove unwanted volumes
        run_cmd('docker run -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker:/var/lib/docker --rm martin/docker-cleanup-volumes')

    def refresh_autocomplete(self):
        setup_autocomplete()