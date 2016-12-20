import os
from docker_console import DOCKER_RUN_PATH

DB = {
    # 'default': {
    #     #TODO:
    #     'DRIVER': 'mysql',
    #     'HOST': 'mysql',
    #     'NAME': 'db',
    #     'USER': 'user',
    #     'PASS': 'pass',
    #     'ROOT_PASS': '123',
    #     'DUMP_IMPORT_FILE': 'databases/database.sql.tar.gz',
    #     'DUMP_EXPORT_LOCATION': 'databases/'
    # }
}

TMP_PATH = "/tmp"

WEB_APP_LOCATION = "app"

TESTS_LOCATION = "tests"

BUILD_PATH = DOCKER_RUN_PATH

OS_USER_HOME_PATH = os.path.expanduser('~')

DEV_DOCKER_IMAGES = {
    'default': None, # this image will be set in each web engine separately
    'selenium_image': ('selenium/standalone-chrome', None),
    'codecept_image': ('droptica/codecept', None),
    'additional_images': [
        # ('vendor/additional_image', 'path_to_dockerfile')
    ]
}

ENV = None
