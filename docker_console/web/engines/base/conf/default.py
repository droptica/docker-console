from docker_console import DOCKER_RUN_PATH

WEB = {
    #TODO:
    # 'ENGINE': 'base',
    'USE_CUSTOM_ENGINE': False, # True/False - useful when we have default and custom engine with the same name
    'APP_LOCATION': 'app'
}

DB = {
    #TODO:
    'default': {
        'DRIVER': 'mysql',
        'HOST': 'mysql',
        'NAME': 'db',
        'USER': 'user',
        'PASS': 'pass',
        'ROOT_USER': 'root',
        'ROOT_PASS': '123',
        'DUMP_IMPORT_FILE': 'databases/database.sql.tar.gz',
        'DUMP_EXPORT_LOCATION': 'databases/'
    }
}

DEV_DOCKER_IMAGES = {
    #TODO:
    'default': None, # this image will be set in each web engine separately
    # 'additional_images': [
    #     # ('vendor/additional_image', 'path_to_dockerfile')
    # ]
}

TESTS = {
    'IMAGES': {
        'selenium_image': ('selenium/standalone-chrome', None),
        'codecept_image': ('droptica/codecept', None)
    },
    'LOCATION': "tests"
}

TMP_PATH = "/tmp"

BUILD_PATH = DOCKER_RUN_PATH

ENV = None
