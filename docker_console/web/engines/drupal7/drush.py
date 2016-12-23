from docker_console.utils.console import run as run_cmd, message


class Drush:

    def __init__(self, config):
        self.config = config
        self.path = self.config.WEB['APP_ROOT']
        self.uri = self.config.DRUPAL[self.config.drupal_site]['SITE_URI']
        
    def run(self, command):
        return run_cmd("drush -r %s --uri=%s %s " % (self.path, self.uri, command))
        # args = self.path
        # if self.uri:
        #     args += ' --uri=' + self.uri
        # return run_cmd("drush -r %s %s" % (args, command))

    def en(self, name):
        if type(name) in (tuple, list):
            return self.run("-y en %s" % ",".join(name))
        else:
            return self.run("-y en %s" % name)

    def cc_all(self):
        return self.run('cc all')

    def cr(self):
        return self.run('cr')

    def uli(self):
        return self.run('uli')

    def updb(self):
        return self.run('-y updb')

    def features_revert(self):
        return self.run('fra -y')

    def config_import(self):
        return self.run('config-import -y')

    def change_password(self):
        return self.run('upwd %s --password=%s' % (self.config.DRUPAL[self.config.drupal_site]['ADMIN_USER'], self.config.DRUPAL[self.config.drupal_site]['ADMIN_PASS']))

    def file_proxy(self):
        self.en('stage_file_proxy')
        return self.run('variable-set stage_file_proxy_origin "%s"' % self.config.DRUPAL[self.config.drupal_site]['STAGE_FILE_PROXY_URL'])

    def drush_import(self, file_path):
        self.run('sql-cli <%s' % file_path)

    def drush_drop_tables(self):
        message('Drop Tables')
        self.run('sql-drop -y')