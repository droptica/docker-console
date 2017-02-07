from importlib import import_module

def load_driver(name):
    try:
        return import_module('docker_console.db.drivers.%s' % name)
    except ImportError:
        pass

