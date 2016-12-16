import os
import docker_console.helpers
from .. import DOCKER_RUN_PATH
from .. import args

ROOT_PASS = "123"

DB_NAME = "db"

DB_USER = "user"

DB_PASSWORD = "pass"

DBHOST = "mysql"

DBDUMP_FILE = "databases/database.sql.tar.gz"

FILES_DST = "sites/default/"

FILES_ARCHIVE = "files/files.tar.gz"

PRIVATE_FILES_ARCHIVE = "files/private.tar.gz"

PRIVATE_FILES_DST = "sites/default/files/"

TMP_PATH = "/tmp"

DRUPAL_LOCATION = "app"

TESTS_LOCATION = "tests"

SITE_DIRECTORY = "default"

SITE_URI = "default"

DRUPAL_ADMIN_USER = 'admin'

DRUPAL_ADMIN_PASS = '123'

BUILD_PATH = DOCKER_RUN_PATH

HOME_PATH = os.path.expanduser('~')

DEV_DOCKER_IMAGES = {
    'default': ('droptica/drupal-dev', None),
    'selenium_image': ('selenium/standalone-chrome', None),
    'codecept_image': ('droptica/codecept', None),
    'additional_images': [
        # ('droptica/additional_image', 'path_to_dockerfile')
    ]
}

SETTINGS_DIR = None

ENV = None

try:
    from config_overrides import *
except Exception as exception:
    if "No module named config_overrides" in str(exception):
        if os.path.exists(os.path.join(DOCKER_RUN_PATH, 'docker', 'docker_drupal', 'docker_drupal_config_overrides.py')):
            if len(args) > 0 and args[0] != 'migrate-to-dcon':
                docker_console.helpers.message("You probably forgot to migrate file wrapper/docker/docker_drupal/docker_drupal_config_overrides.py to wrapper/docker_console/config_overrides.py", 'error')
                docker_console.helpers.message("You can move override files manually or use command 'dcon migrate-to-dcon' to move them automatically. Remember about replacing usages of docker_drupal with docker_console.", 'error')
                exit(0)
    else:
        print "Error during config_overrides file import: ", exception

DRUPAL_ROOT = os.path.realpath(os.path.join(BUILD_PATH, DRUPAL_LOCATION))
