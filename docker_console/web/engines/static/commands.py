from docker_console.web.engines.base.commands import commands

static_commands = {
    'build': [
        'confirm_action',
        'docker.chown',
        'docker.setfacl'
    ],
    'up-and-build': [
        'confirm_action',
        'docker.docker_up',
        'docker.chown',
        'docker.setfacl',
    ],
}

commands.update(static_commands)
