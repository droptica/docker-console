import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import docker_console.version
import docker_console.autocomplete
import platform

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
      def pre_install(self):
            # TODO: add migrate script from docker-drupal to docker-console
            os_dist = platform.dist()
            os.system('%s python-yaml' % (os_commands[os_dist[0]]['package_install']))
            home_docker_console_dir = os.path.join(os.path.expanduser('~'), '.docker_console', 'aliases')
            if not os.path.exists(home_docker_console_dir):
                  os.makedirs(home_docker_console_dir)
                  os.chmod(home_docker_console_dir, 0777)

      def run(self):
            self.pre_install()
            install.run(self)
            docker_console.autocomplete.setup_autocomplete()

      def do_egg_install(self):
            self.pre_install()
            install.do_egg_install(self)
            docker_console.autocomplete.setup_autocomplete()

setup(name='docker-console',
      cmdclass={'install': custom_install},
      version=docker_console.version.__version__,
      description='Application that improves and speeds up web development process using Docker',
      long_description=long_description,
      url='https://github.com/droptica/docker-console',
      download_url = 'https://github.com/droptica/docker-console/archive/v' + docker_console.version.__version__ + '.tar.gz',
      author='Droptica',
      author_email='admin@droptica.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      entry_points = {
            'console_scripts': ['docker-console=docker_console.__main__:main', 'dcon=docker_console.__main__:main'],
      },
      install_requires=[
            'python-dotenv',
      ],
      include_package_data=True,
      zip_safe=False)
