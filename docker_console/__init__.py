import os
import sys
from optparse import OptionParser, OptionGroup
from docker_console.utils.aliases import __all__ as available_aliases, aliases
from docker_console.utils.console import message
from docker_console.version import __version__

parser = OptionParser(version=__version__)

global_commands = ['default', 'init', 'init-tests', 'help', 'refresh-autocomplete', 'cleanup', 'show-nginx-proxy-ip']

args = ["-p", "--docker-run-path",
        "-s", "--docker-shell-run",
        "-c", "--docker-container",
        "-f", "--force-replace-conf",
        "-e", "--drush-eval-run-code",
        "--version",
        "--tpl",
        "--db",
        "--site",
        "--groups",
        "--suites",
        "--group-by",
        "--with-env",
        "-y"]

for i, arg in enumerate(sys.argv):
    if arg.startswith('-'):
        arg = arg.split('=')[0].strip()
        if not arg in args:
            print "Additional args: " + arg
            dest = "docker_fake_value_" + str(i)
            parser.add_option(arg, action="store")

parser.add_option("-p", "--docker-run-path", dest="docker_run_path",
              help="set path do drupal wrapper with 'docker-compose.yml' files and 'docker' folder", metavar="DOCKER_RUN_PATH")

parser.add_option("-s", "--docker-shell-run", action="store_true", dest="docker_shell_run",
              help="Use with no action or 'shell' action. "
                   "set if you want to run docker shell",)

parser.add_option("-c", "--docker-container", dest="docker_container",
              help="Use with 'shell' action. Set container name to run bash in it.", metavar="DOCKER_CONTAINER")

parser.add_option("-f", "--force-replace-conf", action="store_true", dest="docker_init_replace_conf",
              help="Use with action 'init'. "
                   "Set if you want force replace your existing config files ",)

parser.add_option("-y", action="store_true", dest="docker_yes_all",
              help="yes to all questions where 'confirm_action' is used in action steps",)

parser.add_option("--tpl", dest="init_template",
              help="select web engine to init in project", metavar="INIT_TEMPLATE")

parser.add_option("--db", dest="app_database",
              help="select DB to work with", metavar="APP_DATABASE")

parser.add_option("--groups", dest="parallel_test_groups",
              help="Number of parallel test groups", metavar="PARALLEL_TEST_GROUPS")

parser.add_option("--suites", dest="parallel_test_suites",
              help="Test suites to run", metavar="PARALLEL_TEST_SUITES")

parser.add_option("--group-by", dest="parallel_group_by",
              help="Group tests by files or single tests", metavar="PARALLEL_GROUP_BY")

#TODO: this options should be in drupal7 engine but engine is loaded later in __main__
parser.add_option("-e", "--drush-eval-run-code", dest="docker_drush_eval_run_code",
              help="Use with action 'drush'. "
                   "Set if you want run code in drush eval", metavar="DRUSH_EVAL_RUN_CODE")

parser.add_option("--site", dest="drupal_site",
              help="select Drupal site to work with", metavar="DRUPAL_SITE")

parser.add_option("--with-env", action="store_true", dest="with_env",
              help="Use .env file with dcon commands")


parser.set_defaults(docker_shell_run=False)
parser.set_defaults(docker_init_replace_conf=False)
parser.set_defaults(docker_yes_all=False)
parser.set_defaults(app_database='default')
parser.set_defaults(drupal_site='default')
parser.set_defaults(parallel_test_groups=5)
parser.set_defaults(parallel_test_suites='')
parser.set_defaults(parallel_group_by='files')
parser.set_defaults(with_env=False)

group = OptionGroup(parser, "Available aliases", ", ".join('@%s' % alias for alias in available_aliases[:]))
parser.add_option_group(group)

(cmd_options, args) = parser.parse_args()

DOCKER_RUN_PATH = os.getcwd()

OS_USER_HOME_PATH = os.path.expanduser('~')

for idx, arg in enumerate(args):
    if arg.startswith('@'):
        try:
            DOCKER_RUN_PATH = aliases[arg.lstrip('@')]['path'].rstrip('/')
        except:
            pass
        del args[idx]
        del sys.argv[idx]

if cmd_options.docker_run_path is not None:
    DOCKER_RUN_PATH = cmd_options.docker_run_path.rstrip('/')

sys.path.append(os.path.join(DOCKER_RUN_PATH, 'docker_console'))
sys.path.append(os.path.join(OS_USER_HOME_PATH, '.docker_console'))

try:
    from dc_overrides import *
except Exception as exception:
    if "No module named dc_overrides" in str(exception):
        if os.path.exists(os.path.join(DOCKER_RUN_PATH, 'docker', 'docker_drupal', 'docker_drupal_overrides.py')):
            if len(args) > 0 and args[0] not in global_commands:
                message("You probably forgot to migrate file %s/docker/docker_drupal/docker_drupal_overrides.py to %s/docker_console/dc_overrides.py" % (DOCKER_RUN_PATH, DOCKER_RUN_PATH), 'error')
                message("Use command 'init' to create %s/docker_console/dc_overrides.py file, and then adjust overrides manually." % DOCKER_RUN_PATH, 'error')
    else:
        print "Error during dc_overrides file import: ", exception
