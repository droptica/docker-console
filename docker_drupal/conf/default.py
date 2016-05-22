import os
from .. import DOCKER_RUN_PATH

ROOT_PASS = "123"

DB_NAME = "db"

DB_USER = "user"

DB_PASSWORD = "pass"

DBHOST = "mysql"

DBDUMP_FILE = "database.sql.tar.gz"

FILES_DST = "sites/default/"

FILES_ARCHIVE = "files.tar.gz"

TMP_PATH = "/tmp"

DRUPAL_LOCATION = "app"

SITE_DIRECTORY = "default"

SITE_URI = "dockertest.dev"

DRUPAL_ADMIN_USER = 'oitadmin'

DRUPAL_ADMIN_PASS = '123'

BUILD_PATH = DOCKER_RUN_PATH

HOME_PATH = os.path.expanduser('~')

DEV_DOCKER_IMAGES = {
    'default': ('droptica/drupal-dev', None),
    'additional_images': [
        # ('droptica/additional_image', 'path_to_dockerfile')
    ]
}

SETTINGS_DIR = None

<<<<<<< HEAD
ENV = None

=======
>>>>>>> 2b903adeb2f6ef6e32e8780d5ef3584d35b24d6e
try:
    from docker_drupal_config_overrides import *
except Exception as exception:
    if "No module named docker_drupal_config_overrides" in str(exception):
        pass
    else:
        print "Error during docker_drupal_config_overrides file import: ", exception

DRUPAL_ROOT = os.path.realpath(os.path.join(BUILD_PATH, DRUPAL_LOCATION))
