#!/usr/bin/env python
import os
from importlib import import_module
from docker_console import args, DOCKER_RUN_PATH, global_commands
from docker_console.utils.console import message

try:
    from docker_console import commands_overrides
except:
    pass

config = None

try:
    config = import_module('dc_settings')
    config.global_commands = global_commands
    config.WEB['APP_ROOT'] = os.path.realpath(os.path.join(config.BUILD_PATH, config.WEB['APP_LOCATION']))
except Exception as exception:
    if "No module named dc_settings" in str(exception):
        if os.path.exists(os.path.join(DOCKER_RUN_PATH, 'docker', 'docker_drupal', 'docker_drupal_config_overrides.py')):
            if len(args) > 0 and args[0] not in global_commands:
                message("You probably forgot to migrate file %s/docker/docker_drupal/docker_drupal_config_overrides.py to %s/docker_console/dc_settings.py" % (DOCKER_RUN_PATH, DOCKER_RUN_PATH), 'error')
                message("%s/docker_console/dc_settings.py file is required and must contain WEB, DB, DEV_DOCKER_IMAGES and engine specific settings." % DOCKER_RUN_PATH, 'error')
                message("Settings in docker_drupal_config_overrides.py and dc_settings.py are not compatibile, the best solution is to use command 'init' and then adjust default config manually.", 'error')
                exit(0)
        elif len(args) > 0 and args[0] not in global_commands:
            message("Missing %s/docker_console/dc_settings.py file. This file is required and must contain WEB, DB, DEV_DOCKER_IMAGES and engine specific settings. Use command 'init' and then adjust default config manually." % DOCKER_RUN_PATH, 'error')
            exit(0)
    else:
        print "Error during dc_settings file import: ", exception
        exit(0)

engine_loaded = False

if config and hasattr(config, 'WEB') and 'USE_CUSTOM_ENGINE' in config.WEB and config.WEB['USE_CUSTOM_ENGINE']:
    try:
        # try to load custom web engine from user home dir
        web_engine_builder = import_module('custom_web_engines.%s.builder' % config.WEB['ENGINE'])
        web_engine_commands = import_module('custom_web_engines.%s.commands' % config.WEB['ENGINE'])
        engine_loaded = True
    except Exception as exception:
        print "Error during loading custom web engine", exception

if not engine_loaded:
    try:
        # try to load web engine from docker_console
        web_engine_builder = import_module('docker_console.web.engines.%s.builder' % config.WEB['ENGINE'])
        web_engine_commands = import_module('docker_console.web.engines.%s.commands' % config.WEB['ENGINE'])
    except Exception as exception:
        if config is not None:
            print "Error during loading web engine from docker_console", exception

        # load base web engine and config
        web_engine_builder = import_module('docker_console.web.engines.base.builder')
        web_engine_commands = import_module('docker_console.web.engines.base.commands')
        config = import_module('docker_console.web.engines.base.conf.default')
        config.global_commands = global_commands


commands = web_engine_commands.commands

try:
    #try to override commands
    commands.update(commands_overrides)
except:
    pass


def build_array(key):
    if key in commands:
        return commands[key]
    else:
        raise Exception('Invalid parameter: "%s"' % key)


def main():
    steps_key = 'default'
    if len(args) > 0:
        steps_key = args[0]
    build_steps = build_array(steps_key)
    config.steps_key = steps_key
    config.build_arrays = commands

    if hasattr(web_engine_builder, 'Builder'):
        builder = web_engine_builder.Builder(config)
    else:
        builder = web_engine_builder.BaseBuilder(config)
    builder.build(build_steps)


if __name__ == '__main__':
    main()
