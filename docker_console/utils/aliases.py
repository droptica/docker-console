import os, sys
import importlib

__all__ = []
aliases = {}
aliases_home_dir = os.path.join(os.path.expanduser('~'), '.docker_console', 'aliases')
sys.path.append(os.path.join(os.path.expanduser('~'), '.docker_console'))

if(os.path.isdir(aliases_home_dir)):
    for file_name in os.listdir(aliases_home_dir):
        if not file_name.startswith("__") and file_name.endswith(".py"):
            try:
                i = importlib.import_module('aliases.%s' % file_name.rsplit('.')[0])

                if hasattr(i, '__all__'):
                    __all__.extend(i.__all__)

                    for alias in i.__all__:
                        aliases[alias] = getattr(i, alias)
            except Exception as exception:
                print "Error while reading aliases from %s:" % os.path.join(aliases_home_dir, file_name), exception
