import datetime
import os
import sys
import re
from copy import deepcopy
from dotenv import load_dotenv

from .drush import Drush
from .docker import Docker
from .database import Database
from .drupal_settings import DrupalSettings
from .archive import Archive
from .helpers import run as run_cmd, rgetattr, query_yes_no
from . import parser, cmd_options
from optparse import OptionGroup


class Builder:

    def __init__(self, config):
        self.config = config
        dotenv_path = os.path.join(self.config.BUILD_PATH, '.env')
        if os.path.isfile(dotenv_path):
            load_dotenv(dotenv_path)
        self.config.ENV = os.environ.get("ENV")
        if os.environ.get("SITE_URI"):
            self.config.SITE_URI = os.environ.get("SITE_URI")
        self.config.NO_INTERACTIVE = os.environ.get("NO_INTERACTIVE")
        self.config.args = sys.argv
        self.now = datetime.datetime.now()
        self.config.TIME_STR = self.now.strftime("%Y-%m-%d.%H.%M")
        self.drush = Drush(self.config)
        self.drupal_settings = DrupalSettings(self.config)
        self.database = Database(self.config, self.drush)
        self.docker = Docker(self.config)
        self.archive = Archive(self.config)


    def chmod_files(self):
        run_cmd('chmod 777 -Rf %s' % os.path.join(self.config.DRUPAL_ROOT, self.config.FILES_DST, 'files'))

    def build(self, steps):
        for step in steps:
            params = re.search('\(.*\)', step)
            if params is not None:
                params = params.group(0)
                step = step.split(params)[0]
                params_splited = params[1:-1].split(',')
                params_arr = []
                for param in params_splited:
                    params_arr.append(eval(param))
                rgetattr(self, step)(*params_arr)
            else:
                rgetattr(self, step)()

    def confirm_action(self, default='yes'):
        action = self.config.steps_key
        pattern = r'\b' + re.escape('confirm_action') + r'\b'
        indices = [i for i, x in enumerate(self.config.build_arrays[action]) if re.search(pattern, x)]
        action_build_arrays = deepcopy(self.config.build_arrays[action])
        for idx in indices:
            del action_build_arrays[idx]
        answer = query_yes_no('Are you sure that you want execute action: %s? This action consists of following steps: \n%s'
                              % (action, ", ".join(action_build_arrays)), default, cmd_options.docker_yes_all)
        if answer == False:
            exit(0)

    def print_help(self):
        group = OptionGroup(parser, "Available actions", ", ".join(self.config.build_arrays))
        parser.add_option_group(group)
        parser.usage = "usage: %prog " + "[action] [options]"
        parser.print_help()
