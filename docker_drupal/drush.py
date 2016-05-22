from .helpers import run as run_cmd


class Drush:

    def __init__(self, config):
        self.config = config
        self.path = self.config.DRUPAL_ROOT
        self.uri = self.config.SITE_URI
        
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
        return self.run('upwd %s --password=%s' % (self.config.DRUPAL_ADMIN_USER, self.config.DRUPAL_ADMIN_PASS))

    def file_proxy(self):
        self.en('stage_file_proxy')
        return self.run('variable-set stage_file_proxy_origin "%s"' % self.config.STAGE_FILE_PROXY_URL)

