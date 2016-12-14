import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import docker_console.version
import docker_console.autocomplete

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

class custom_install(install):
      def run(self):
            # TODO: add migrate script from docker-drupal to docker-console
            home_docker_console_dir = os.path.join(os.path.expanduser('~'), '.docker_console', 'aliases')
            if not os.path.exists(home_docker_console_dir):
                  os.makedirs(home_docker_console_dir)
                  os.chmod(home_docker_console_dir, 0777)
            install.run(self)
            docker_console.autocomplete.setup_autocomplete()

setup(name='docker-console',
      cmdclass={'install': custom_install},
      version=docker_console.version.__version__,
      description='Docker connector for drupal',
      long_description=long_description,
      url='https://github.com/droptica/docker-console',
      download_url = 'https://github.com/droptica/docker-console/archive/v' + docker_console.version.__version__ + '.tar.gz',
      author='Droptica',
      author_email='admin@droptica.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      entry_points = {
            'console_scripts': ['docker-console=docker_console.__main__:main'],
      },
      install_requires=[
          'pyyaml',
          'python-dotenv',
      ],
      include_package_data=True,
      zip_safe=False)
