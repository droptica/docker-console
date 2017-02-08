from docker_console.web.engines.base.docker import BaseDocker


class Docker(BaseDocker):
    def __init__(self, config):
        super(Docker, self).__init__(config)
