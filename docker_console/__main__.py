#!/usr/bin/env python
from importlib import import_module
from docker_console import args
from docker_console.utils.console import message

try:
    from docker_console import build_arrays_overrides
except:
    pass

try:
    settings = import_module('config_overrides')
    WEB_ENGINE = settings.WEB['ENGINE']
    web_engine = import_module('docker_console.web.engines.%s.builder' % WEB_ENGINE)
    config = import_module('docker_console.web.engines.%s.conf.default' % WEB_ENGINE)
except Exception as excepttion:
    #TODO: load engines from home location
    # load base web engine
    web_engine = import_module('docker_console.web.engines.base.builder')
    config = import_module('docker_console.web.engines.base.conf.default')

#TODO: limit commands to used web engine
build_arrays = {
    'init': ['confirm_action', 'docker.docker_init'],
    'init-tests': ['confirm_action', 'tests.tests_init'],
    'add-host-to-etc-hosts': ['docker.add_entry_to_etc_hosts'],
    'refresh-autocomplete': ['docker.refresh_autocomplete'],
    'shell': ['docker.docker_shell'],

    'start': ['docker.docker_up', 'chmod_files'],
    'up': ['docker.docker_up', 'chmod_files'],
    'update-images': ['docker.docker_update_images', 'chmod_files'],

    'stop': ['docker.docker_stop'],
    'rm': ['docker.docker_stop', 'docker.docker_rm'],
    'rmi': ['docker.docker_stop', 'docker.docker_rm', 'docker.docker_rmi'],

    'restart': ['docker.docker_restart', 'chmod_files'],

    'build': ['confirm_action', 'docker.docker_run("docker-console build-in-docker")',
              'docker.chown', 'docker.setfacl', 'chmod_files'],
    'up-and-build': ['confirm_action', 'docker.docker_up', 'docker.docker_run("docker-console build-in-docker")',
                     'docker.chown', 'docker.setfacl', 'chmod_files'],

    'build-in-docker': ['drupal_settings.copy_settings', 'database.drop_db', 'database.create_db', 'database.import_db',
                        'drush.en("devel")', 'drush.run("cc all")', 'drush.run("uli")'],

    'drush': ['docker.drush_run'],
    'codecept': ['tests.codecept_run'],
    'config-prepare': ['docker.config_prepare'],
    'add-host-to-docker-compose': ['docker.add_host'],
    'show-ip': ['docker.show_ip'],
    'show-nginx-proxy-ip': ['docker.show_nginx_proxy_ip'],
    'default': ['print_help'],
    'help': ['print_help'],
    'test' : ['tests.tests_run'],
    'cleanup': ['docker.cleanup'],
    'dump': ['docker.docker_create_dump'],
    'migrate-to-dcon': ['docker.migrate_to_dcon'],
}

try:
    build_arrays.update(build_arrays_overrides)
except:
    pass


def build_array(key):
    if key in build_arrays:
        return build_arrays[key]
    else:
        message('Invalid parametr: "%s"' % key)
        return []


def main():
    steps_key = 'default'
    if len(args) > 0:
        steps_key = args[0]
    build_steps = build_array(steps_key)
    config.steps_key = steps_key
    config.build_arrays = build_arrays

    if hasattr(web_engine, 'Builder'):
        builder = web_engine.Builder(config)
    else:
        builder = web_engine.BaseBuilder(config)
    builder.build(build_steps)


if __name__ == '__main__':
    main()