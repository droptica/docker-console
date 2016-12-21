import os
from docker_console import cmd_options
from docker_console.web.engines.base.docker import BaseDocker


class Docker(BaseDocker):
    def __init__(self, config):
        super(Docker, self).__init__(config)

    def _get_volumes(self):
        volumes = []
        db_path = os.path.join(self.config.BUILD_PATH, self.config.DB[self.config.db_alias]['DUMP_IMPORT_FILE'])
        if db_path and os.path.islink(db_path):
            real_db_path = os.path.realpath(db_path)
            volumes.append('-v %s:%s' % (real_db_path, db_path.replace(self.config.BUILD_PATH, '/app/')))

        files_path = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['FILES_ARCHIVE'])
        if files_path and os.path.islink(files_path):
            real_files_path = os.path.realpath(files_path)
            volumes.append('-v %s:%s' % (real_files_path, files_path.replace(self.config.BUILD_PATH, '/app/')))

        private_files_path = os.path.join(self.config.BUILD_PATH, self.config.DRUPAL[self.config.drupal_site]['PRIVATE_FILES_ARCHIVE'])
        if private_files_path and os.path.islink(private_files_path):
            real_private_files_path = os.path.realpath(private_files_path)
            volumes.append('-v %s:%s' % (real_private_files_path,
                                         private_files_path.replace(self.config.BUILD_PATH, '/app/')))

        volumes.append('-v %s:%s' % (self.config.BUILD_PATH, '/app'))
        return ' '.join(volumes)

    def drush_run(self):
        if cmd_options.docker_drush_eval_run_code is None:
            cmd = ' '.join(self.config.args[2:])
        else:
            cmd = "ev '%s'" % cmd_options.docker_drush_eval_run_code
            if cmd_options.docker_yes_all:
                cmd += ' -y'
        self.docker_drush(cmd)

    def docker_drush(self, cmd=''):
        self.docker_run('drush -r %s %s' % (os.path.join('/app', self.config.WEB['APP_LOCATION']), cmd))
