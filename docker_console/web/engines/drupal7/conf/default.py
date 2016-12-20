from docker_console.web.engines.base.conf.default import *
from docker_console.utils.console import message

DRUPAL = {
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

# set default dev image for given web app engine
DEV_DOCKER_IMAGES['default'] = ('droptica/drupal-dev', None)

try:
    from config_overrides import *
except Exception as exception:
    #TODO: check this
    if "No module named config_overrides" in str(exception):
        if os.path.exists(os.path.join(DOCKER_RUN_PATH, 'docker', 'docker_drupal', 'docker_drupal_config_overrides.py')):
            if len(args) > 0 and args[0] != 'migrate-to-dcon':
                message("You probably forgot to migrate file wrapper/docker/docker_drupal/docker_drupal_config_overrides.py to wrapper/docker_console/config_overrides.py", 'error')
                message("You can move override files manually or use command 'dcon migrate-to-dcon' to move them automatically. Remember about replacing usages of docker_drupal with docker_console.", 'error')
                exit(0)
    else:
        print "Error during config_overrides file import: ", exception

WEB_APP_ROOT = os.path.realpath(os.path.join(BUILD_PATH, WEB_APP_LOCATION))
