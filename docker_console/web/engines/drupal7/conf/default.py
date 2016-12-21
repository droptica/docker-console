from docker_console.web.engines.base.conf.default import *

DRUPAL = {
    'default': {
        'FILES_DST': 'sites/default/',
        'FILES_ARCHIVE': 'files/files.tar.gz',
        'PRIVATE_FILES_ARCHIVE': 'files/private.tar.gz',
        'PRIVATE_FILES_DST': 'sites/default/files/',
        'SITE_DIRECTORY': 'default',
        'SITE_URI': 'default',
        'DRUPAL_ADMIN_USER': 'admin',
        'DRUPAL_ADMIN_PASS': '123',
        'SETTINGS_DIR': None,
        'STAGE_FILE_PROXY_URL': None
    }
}

# set default dev image for given web app engine
DEV_DOCKER_IMAGES['default'] = ('droptica/drupal-dev', None)
