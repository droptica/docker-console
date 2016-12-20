import os, sys
import importlib

__all__ = []
aliases = {}
aliases_home_dir = os.path.join(os.path.expanduser('~'), '.docker_console', 'aliases')
sys.path.append(aliases_home_dir)

if(os.path.isdir(aliases_home_dir)):
    for file_name in os.listdir(aliases_home_dir):
        if file_name.endswith(".py"):
            try:
                i = importlib.import_module(file_name.rsplit('.')[0])

                __all__.extend(i.__all__)

                for alias in i.__all__:
                    aliases[alias] = getattr(i, alias)
            except:
                pass
