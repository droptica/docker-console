import datetime
import os
import sys
import re
from copy import deepcopy
from dotenv import load_dotenv
from optparse import OptionGroup

from docker_console import parser, cmd_options
from docker_console.db import load_driver
from docker_console.utils.console import rgetattr, query_yes_no
from docker_console.web.engines.base.tests import BaseTests
from docker_console.web.engines.base.docker import BaseDocker

class BaseBuilder(object):

    def __init__(self, config):
        self.config = config
        dotenv_path = os.path.join(self.config.BUILD_PATH, '.env')
        if os.path.isfile(dotenv_path):
            load_dotenv(dotenv_path)
        self.config.ENV = os.environ.get("ENV")
        self.config.NO_INTERACTIVE = os.environ.get("NO_INTERACTIVE")
        self.config.args = sys.argv
        self.now = datetime.datetime.now()
        self.config.TIME_STR = self.now.strftime("%Y-%m-%d.%H.%M")
        self.tests = BaseTests(self.config)
        self.docker = BaseDocker(self.config)

        self.db_alias = cmd_options.app_database
        self.config.db_alias = self.db_alias
        if self.db_alias in config.DB and 'DRIVER' in config.DB[self.db_alias] and config.DB[self.db_alias]['DRIVER']:
            self.db_driver_name = config.DB[self.db_alias]['DRIVER']
            self.db_driver = load_driver(self.db_driver_name)
            self.database = self.db_driver.Database(self.config, self.db_alias)


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
