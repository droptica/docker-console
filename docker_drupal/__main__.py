#!/usr/bin/env python
from . import args
from .builder import Builder
from .conf import default
from .helpers import message

try:
    from . import build_arrays_overrides
except:
    pass

build_arrays = {
    'init': ['confirm_action', 'docker.docker_init'],
    'add-host-to-etc-hosts': ['docker.add_entry_to_etc_hosts'],
    'refresh-autocomplete': ['docker.refresh_autocomplete'],
    'shell': ['docker.docker_shell'],

    'start': ['docker.docker_compose', 'chmod_files'],
    'up': ['docker.docker_compose', 'chmod_files'],
    'stop': ['docker.docker_stop'],
    'restart': ['docker.docker_restart', 'chmod_files'],

    'build': ['confirm_action', 'docker.docker_run("docker-drupal build-in-docker")',
              'docker.chown', 'docker.setfacl', 'chmod_files'],
    'up-and-build': ['confirm_action', 'docker.docker_compose', 'docker.docker_run("docker-drupal build-in-docker")',
                     'docker.chown', 'docker.setfacl', 'chmod_files'],

    'build-in-docker': ['drupal_settings.copy_settings', 'database.drop_db', 'database.create_db', 'database.import_db',
                        'drush.run("fra -y")', 'drush.run("-y updb")', 'drush.en("devel")', 'drush.run("fra -y")',
                        'drush.run("cc all")', 'drush.run("uli")'],

    'drush': ['docker.drush_run'],
    'config-prepare': ['docker.config_prepare'],
    'add-host-to-docker-compose': ['docker.add_host'],
    'show-ip': ['docker.show_ip'],
    'show-nginx-proxy-ip': ['docker.show_nginx_proxy_ip'],
    'default': ['print_help'],
    'help': ['print_help'],

    'cleanup': ['docker.cleanup'],
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
    default.steps_key = steps_key
    default.build_arrays = build_arrays

    builder = Builder(default)
    builder.build(build_steps)


if __name__ == '__main__':
    main()