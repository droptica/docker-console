from docker_console import DOCKER_RUN_PATH

# do not override this - this is needed for aliases to work
BUILD_PATH = DOCKER_RUN_PATH

WEB = {}

DB = {}

DEV_DOCKER_IMAGES = {}

TESTS = {
    'IMAGES': {
        'selenium_image': ('selenium/standalone-chrome', None),
        'codecept_image': ('droptica/codecept', None)
    },
    'LOCATION': "tests"
}

ENV = None
