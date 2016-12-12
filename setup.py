import os
from setuptools import setup, find_packages
from setuptools.command.install import install
import docker_drupal.version
import docker_drupal.autocomplete

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

class custom_install(install):
      def run(self):
            home_docker_drupal_dir = os.path.join(os.path.expanduser('~'), '.docker_drupal', 'aliases')
            if not os.path.exists(home_docker_drupal_dir):
                  os.makedirs(home_docker_drupal_dir)
                  os.chmod(home_docker_drupal_dir, 0777)
            install.run(self)
            docker_drupal.autocomplete.setup_autocomplete()

setup(name='docker-drupal',
      cmdclass={'install': custom_install},
      version=docker_drupal.version.__version__,
      description='Docker connector for drupal',
      long_description=long_description,
      url='https://github.com/droptica/docker-console',
      download_url = 'https://github.com/droptica/docker-console/archive/v' + docker_drupal.version.__version__ + '.tar.gz',
      author='Droptica',
      author_email='admin@droptica.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      entry_points = {
            'console_scripts': ['docker-drupal=docker_drupal.__main__:main'],
      },
      install_requires=[
          'pyyaml',
          'python-dotenv',
      ],
      include_package_data=True,
      zip_safe=False)
