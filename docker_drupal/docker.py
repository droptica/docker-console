import os
import re
import yaml
import tempfile
import uuid

import shutil
from distutils import dir_util
from .helpers import run as run_cmd, call as call_cmd, message
from .autocomplete import setup_autocomplete
from . import cmd_options


class Docker:

    def __init__(self, config):
        self.config = config
        if self.config.ENV:
            env = '-' + self.config.ENV
        else:
            env = ''
        self.compose_path = os.path.join(self.config.BUILD_PATH, 'docker-compose.yml')
        if not os.path.exists(self.compose_path) and self.config.steps_key not in ('default', 'init', 'help', 'refresh-autocomplete', 'cleanup'):
            message('docker-compose.yml file is missing. To run docker-drupal you need to do one of this things:\n'
                        'go to project wrapper path, \n'
                        'specify absolute path to project wrapper by -p (--docker-run-path) option\n'
                        'create alias with your project wrapper path in ~/.docker_drupal/aliases (then docker-drupal @project_dev)', 'warning')
            exit(0)
        self.compose_template_path = os.path.join(self.config.BUILD_PATH, 'docker-compose' + env + '-template.yml')
        self.base_alias = "".join(re.findall("[a-zA-Z]+", os.path.basename(self.config.BUILD_PATH))).lower()

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
        # if test:
        #     ret += ' --link selenium-test:selenium'
        # return ret

    def _get_hosts(self):
        docker_comose = open(self.compose_path)
        docker_config = yaml.load(docker_comose)
        hosts = []
        for container in docker_config:
            try:
                for host in docker_config[container]['environment']['VIRTUAL_HOST'].split(','):
                    hosts.append('--link %s:%s' % ('%s_%s_1' % (self.base_alias, container),
                                                   host.strip()))
            except:
                pass
        return ' '.join(hosts)

    def _get_volumes(self):
        volumes = []
        # if os.path.isfile(os.path.join(self.config.HOME_PATH, '.gitconfig')):
        #     volumes.append('-v %s:%s:ro' % (os.path.join(self.config.HOME_PATH, '.gitconfig'), '/root/.gitconfig'))
        # if os.path.isdir(os.path.join(self.config.HOME_PATH, '.ssh')):
        #     volumes.append('-v %s:%s:ro' % (os.path.join(self.config.HOME_PATH, '.ssh'), '/root/.ssh'))
        db_path = os.path.join(self.config.BUILD_PATH, 'databases', self.config.DBDUMP_FILE)
        if os.path.islink(db_path):
            real_db_path = os.path.realpath(db_path)
            volumes.append('-v %s:%s' % (real_db_path, os.path.join('/app/databases', self.config.DBDUMP_FILE)))
        volumes.append('-v %s:%s' % (self.config.BUILD_PATH, '/app'))
        return ' '.join(volumes)

    def _container_alias(self, value):
        tmp = value.split(':')
        tmp[0] = '%s_%s_1' % (self.base_alias, tmp[0])
        return ':'.join(tmp)

    def docker_run(self, cmd):
        run_cmd(self.docker_command() + ' ' + cmd)

    def drush_run(self):
        if cmd_options.docker_drush_eval_run_code is None:
            cmd = ' '.join(self.config.args[2:])
        else:
            cmd = "ev '%s'" % cmd_options.docker_drush_eval_run_code
            if cmd_options.docker_yes_all:
                cmd += ' -y'
        self.docker_drush(cmd)

    def docker_drush(self, cmd=''):
        self.docker_run('drush -r %s %s' % (os.path.join('/app', self.config.DRUPAL_LOCATION), cmd))

    def docker_compose(self):
        run_cmd('docker-compose stop', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose rm -f', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose pull', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose build', cwd=self.config.BUILD_PATH)

        ALL_DEV_DOCKER_IMAGES = [self.config.DEV_DOCKER_IMAGES['default']] + self.config.DEV_DOCKER_IMAGES['additional_images']

        for DEV_DOCKER_IMAGE, DEV_DOCKER_IMAGE_DOCKERFILE in ALL_DEV_DOCKER_IMAGES:
            run_cmd('docker pull %s' % DEV_DOCKER_IMAGE)
            if DEV_DOCKER_IMAGE_DOCKERFILE is not None:
                run_cmd('docker build --no-cache -t %s %s' %
                        (DEV_DOCKER_IMAGE, os.path.join(self.config.BUILD_PATH, DEV_DOCKER_IMAGE_DOCKERFILE)),
                        cwd=self.config.BUILD_PATH)

        run_cmd('docker-compose up -d', cwd=self.config.BUILD_PATH)

    def docker_stop(self):
        run_cmd('docker-compose stop', cwd=self.config.BUILD_PATH)
        run_cmd('docker-compose rm -f', cwd=self.config.BUILD_PATH)

    def docker_restart(self):
        self.docker_compose()

    def docker_command(self):
        if self.config.NO_INTERACTIVE:
            return 'docker run --rm %s %s %s %s' % (self._get_volumes(), self._get_links(), self._get_hosts(),
                                                        self.config.DEV_DOCKER_IMAGES['default'][0])
        else:
            return 'docker run --rm -it %s %s %s %s' % (self._get_volumes(), self._get_links(), self._get_hosts(),
                                        self.config.DEV_DOCKER_IMAGES['default'][0])

    def tests_run(self):
        if len(self.config.args) > 2:
            args = 'tests/' + ' '.join(self.config.args[2:])
        else:
            args = ''
        run_cmd('docker run -d --name selenium-test-%s %s %s selenium/standalone-chrome'
                % (self.base_alias, self._get_links(), self._get_hosts()))
        run_cmd('docker run --rm -it %s %s %s --link selenium-test-%s:selenium -w /app/tests/ %s codecept run %s --html'
            % (self._get_volumes(), self._get_links(), self._get_hosts(),
               self.base_alias, self.config.DEV_DOCKER_IMAGES['default'][0], args))

        run_cmd('docker stop selenium-test-%s' % self.base_alias)
        run_cmd('docker rm selenium-test-%s' % self.base_alias)
        self.docker_command()
        
    def get_container_ip(self):
        web_container_alias = self._container_alias("web:web").split(':')[0]
        if not run_cmd('docker ps -q -f name=%s' % web_container_alias, return_output=True):
            message("Docker is not up for this project and it will be started. It is required to add config entry to /etc/hosts.", 'info')
            self.docker_compose()
        web_container_ip_address = run_cmd('docker inspect --format "{{ .NetworkSettings.IPAddress }}" %s'
                                               % web_container_alias,
                                               return_output=True)
        return web_container_ip_address

    def get_nginx_proxy_ip(self):
        if not run_cmd('docker ps -q -f name=ngnix-proxy', return_output=True):
            return False
        container_ip_address = run_cmd('docker inspect --format "{{ .NetworkSettings.IPAddress }}" ngnix-proxy',
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

    def docker_init(self):
        temp_path = self.create_copy(os.path.join(os.path.dirname(__file__), 'setup_defaults'))
        compose_path = os.path.join(temp_path, 'docker-compose.yml')
        config_file = open(compose_path, 'r')
        content = config_file.read()
        config_file.close()
        content = content.replace("{{HOST}}", self.base_alias + '.dev')
        config_file = open(compose_path, 'w')
        config_file.write(content)
        config_file.close()

        self.create_copy(temp_path, self.config.BUILD_PATH, cmd_options.docker_init_replace_conf)
        dir_util.remove_tree(temp_path)
        message("Docker has been correctly initialized in this project.", 'info')
        message("If you want to automatically add config entry for this project to /etc/hosts, please run 'docker-drupal add-host-to-etc-hosts' command", 'info')

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

    def create_copy(self, path, dest_path=None, force_update=False):
        if dest_path is None:
            temp_dir = tempfile.gettempdir()
            dest_path = os.path.join(temp_dir, str(uuid.uuid4()))
            os.mkdir(dest_path)
        for root, dirs, files in os.walk(path):
            path_tail = root.split(path)[-1]
            if not path_tail:
                path_tail = "/"
            for dir in dirs:
                dest_dir_path = dest_path + os.path.join(path_tail, dir)
                if not os.path.exists(dest_dir_path):
                    os.mkdir(dest_dir_path)
            for name in files:
                dest_file_path = dest_path + os.path.join(path_tail, name)
                src = os.path.join(root, name)

                if not os.path.exists(dest_file_path) or force_update:
                    shutil.copyfile(
                        src,
                        dest_file_path
                    )

        return dest_path

    def chown(self):
        self.docker_chown(self.config.DRUPAL_LOCATION, os.getuid())

    def add_host(self):
        container = self.config.args[2]
        host = self.config.args[3]
        self.docker_add_host(container, host)

    def setfacl(self):
        if os.getuid():
            self.docker_run('setfacl -Rm g:www-data:rwX %s' % self.config.DRUPAL_LOCATION)
            self.docker_run('setfacl -d -Rm g:www-data:rwX  %s' % self.config.DRUPAL_LOCATION)
        else:
            run_cmd('setfacl -Rm g:www-data:rwX %s' % self.config.DRUPAL_LOCATION)
            run_cmd('setfacl -d -Rm g:www-data:rwX  %s' % self.config.DRUPAL_LOCATION)

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