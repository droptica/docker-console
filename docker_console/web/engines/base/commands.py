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
    'run': [
        'docker.docker_run_cmd'
    ],
    'start': [
        'docker.docker_up'
    ],
    'up': [
        'docker.docker_up'
    ],
    'update-images': [
        'docker.docker_update_images'
    ],

    'stop': [
        'docker.docker_stop'
    ],
    'restart': [
        'docker.docker_restart'
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
    'robo': [
        'tests.robo_run'
    ],
    'init-robo': [
        'tests.robo_init'
    ],
    'test': [
        'tests.tests_run'
    ],
    'test-parallel': [
        'tests.test_run_parallel'
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
        'docker.docker_run("docker-console dump-in-docker")',
    ],
    'dump-in-docker': [
        'database.export_db',
    ]
}
