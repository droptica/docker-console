commands = {
    'init': [
        'confirm_action',
        'docker.docker_init'
    ],
    'init-tests': [
        'confirm_action',
        'tests.tests_init'
    ],
    'add-host-to-docker-compose': [
        'docker.add_host'
    ],
    'add-host-to-etc-hosts': [
        'docker.add_entry_to_etc_hosts'
    ],
    'refresh-autocomplete': [
        'docker.refresh_autocomplete'
    ],
    'shell': [
        'docker.docker_shell'
    ],
    'start': [
        'docker.docker_up',
        'chmod_files'
    ],
    'up': [
        'docker.docker_up',
        'chmod_files'
    ],
    'update-images': [
        'docker.docker_update_images',
        'chmod_files'
    ],

    'stop': [
        'docker.docker_stop'
    ],
    'restart': [
        'docker.docker_restart',
        'chmod_files'
    ],

    'rm': [
        'docker.docker_stop',
        'docker.docker_rm'
    ],
    'rmi': [
        'docker.docker_stop',
        'docker.docker_rm',
        'docker.docker_rmi'
    ],

    'codecept': [
        'tests.codecept_run'
    ],
    'test' : [
        'tests.tests_run'
    ],

    'config-prepare': [
        'docker.config_prepare'
    ],
    'show-ip': [
        'docker.show_ip'
    ],
    'show-nginx-proxy-ip': [
        'docker.show_nginx_proxy_ip'
    ],
    'default': [
        'print_help'
    ],
    'help': [
        'print_help'
    ],
    'cleanup': [
        'docker.cleanup'
    ],
    'dump': [
        'database.export_db'
    ],
}
