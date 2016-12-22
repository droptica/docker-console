import os
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
from docker_console.bash_completion import setup_autocomplete
from docker_console.utils.files import create_dir_copy
from docker_console.version import __version__ as version

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

os_commands = {
    'Ubuntu': {
        'package_install': 'apt-get -y install',
    },
    'debian': {
        'package_install': 'apt-get -y install',
    },
}

class custom_install(install):
    def copy_docker_drupal_files(self, home_docker_console_dir):
        home_docker_drupal_dir = os.path.join(os.path.expanduser('~'), '.docker_drupal', 'aliases')
        if os.path.exists(home_docker_drupal_dir):
            create_dir_copy(home_docker_drupal_dir, home_docker_console_dir)

    def pre_install(self):
        os_dist = platform.dist()
        os.system('%s python-yaml' % (os_commands[os_dist[0]]['package_install']))
        home_docker_console_dir = os.path.join(os.path.expanduser('~'), '.docker_console', 'aliases')
        self.copy_docker_drupal_files(home_docker_console_dir)
        if not os.path.exists(home_docker_console_dir):
            os.makedirs(home_docker_console_dir)
            os.chmod(home_docker_console_dir, 0777)

        aliases_file_path = os.path.join(home_docker_console_dir, 'aliases.py')
        init_file_path = os.path.join(home_docker_console_dir, '__init__.py')
        if not os.path.exists(aliases_file_path):
            aliases = open(aliases_file_path, 'w')
            aliases.close()
        if not os.path.exists(init_file_path):
            aliases = open(init_file_path, 'w')
            aliases.close()

    def run(self):
        self.pre_install()
        install.run(self)
        setup_autocomplete()

    def do_egg_install(self):
        self.pre_install()
        install.do_egg_install(self)
        setup_autocomplete()

setup(name='docker-console',
    cmdclass={'install': custom_install},
    version=version,
    description='Application that improves and speeds up web development process using Docker',
    long_description=long_description,
    url='https://github.com/droptica/docker-console',
    download_url = 'https://github.com/droptica/docker-console/archive/v' + version + '.tar.gz',
    author='Droptica',
    author_email='admin@droptica.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points = {
        'console_scripts': [
            'docker-console=docker_console.__main__:main',
            'dcon=docker_console.__main__:main'
        ],
    },
    install_requires=[
        'python-dotenv',
    ],
    setup_requires=[
        'python-dotenv',
    ],
    include_package_data=True,
    zip_safe=False
)
