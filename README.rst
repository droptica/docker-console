Application that improves and speeds up web development process using Docker.

|

=========
**Setup**
=========

|

**docker-console package installation**
=======================================

Requirements for docker-console:

* python-pip package::

    sudo apt-get update && sudo apt-get -y install python-yaml python-setuptools python-pip python-dev build-essential

|

* docker
* docker-compose


When this requirements are satisfied, you can install docker-console through pip using command::

    sudo pip install docker-console

|

All other dependencies will be automatically installed during docker-console installation process.

|


**docker-console package update**
=================================
To update docker-console package, you need to run the same command as for installation with additional option **--upgrade**::

    sudo pip install docker-console --upgrade

|

**Autocomplete activation**
===========================

During package installation, bash completion scripts are placed in::

    /usr/share/bash-completion/completions/docker-console

|

To activate docker-console commands and options completion, you need to logout and login again, or type::

    exec bash

without logging out.

|
|

==================================
**Available commands and options**
==================================

Note that **docker-console** can be also run by **dcon**. This commands are equivalent.

|

**Commands that can be run from anywhere**
==========================================

- default:
    Default action if no command spefified. This command is equivalent to::

        docker-console

    and::

        docker-console help

|

- help:
    Print available options, aliases AND commands including commands added locally for project in dc_overrides.py (if you are running this command in project wrapper).
    If you use --help option, you will not see available commands, but you can always use::

        docker-console <tab><tab>

    to see this available commands. Note that autocomplete mechanism is not working for commands added locally for project in dc_overrides.py.

    |

    This command is equivalent to::

        docker-console

    and::

        docker-console default

|

- init:
- init-tests:
    This commands are copying files from selected template directory to project wrapper.

    Default **docker init** template is:
        - drupal7

    Default **tests init** template is:
        - drupal7


    To **init docker** in drupal7 project, you need to run::

        docker-console init --tpl drupal7

    To **init tests** in drupal7 project, you need to run::

        docker-console init-tests --tpl drupal7

    You can also create own custom docker init and tests init templates.

    Custom **docker init** templates have to be placed in::

        ~/.docker_console/custom_docker_init_templates/


    Custom **tests init** templates have to be placed in::

        ~/.docker_console/custom_tests_init_templates/

    Each template should be separate directory that contains files which will be copied to project wrapper.
    Init template can have any directory structure and can contain any type of files.
    Files in init template that ends with '-tpl' will be processed during init and '{{HOST}}' variable will be replaced by host name generated based on project dir name (eg. examplesite.dev).
    Custom init template directory name will be init template name.

    Eg. when custom **docker init** template directory will be::

        ~/.docker_console/custom_docker_init_templates/example_custom_init_template

    then in project wrapper you can run::

        docker-console init --tpl example_custom_init_template

    When custom **tests init** template directory will be::

        ~/.docker_console/custom_tests_init_templates/example_custom_tests_init_template

    then in project wrapper you can run::

        docker-console init-tests --tpl example_custom_tests_init_template


    Files existing in project wrapper localization, by default will not be replaced. If you want to force replace files, you need to use '-f' or '--force-replace-conf' option.

    |

    Options:

    \--tpl
        This is required param that specifies the template that is used to init docker in project wrapper.

    \-f, \--force-replace-conf
        Set if you want force replace your existing wrapper files with this from template.
        All your changes in wrapper files will be irrevocably lost. Other files in wrapper folder and 'docker' folder will stay unchanged.

|

- cleanup:
    | This command is running three commands that are cleaning up unneeded docker containers, images and volumes.
    | See http://blog.yohanliyanage.com/2015/05/docker-clean-up-after-yourself/ for precise description.

|

- refresh-autocomplete:
    Recreates bash completion script. It can be used if you want add support for autocomplete of newly added project aliases, or new custom project commands.
    After that command you need to logout and login again, or run::

        exec bash

    command to apply autocomplete changes.

|

**Commands that needs to be run from project wrapper with docker-compose.yml file**
===================================================================================

- shell:
    Print docker command that runs shell inside docker.

    |

    Options:

    \-c, \--docker-container
        Set container name to run bash in it.

    |

    \-s, \--docker-shell-run
        Set if you want to run docker shell.

|

- add-host-to-docker-compose:
    Add custom host to docker-compose.yml file.

|

- add-host-to-etc-hosts:
    | Add config entry for project to /etc/hosts depending on VIRTUAL_HOST variable for web and phpmyadmin containers configuration in docker-compose.yml.

    Example of /etc/hosts entry for project::

        172.17.0.2		project.dev www.project.dev phpmyadmin.project.dev

|

- up:
    Start all containers defined in docker-compose.yml

    |

    This command is equivalent to::

        docker-console start

|

- start:
    Start all containers defined in docker-compose.yml

    |

    This command is equivalent to::

        docker-console up

|

- update-images:
    Stop and remove project containers, pull and build images from docker-compose.yml, DEV_DOCKER_IMAGES and TESTS['IMAGES'] configs. Then starts containers from docker-compose.yml.

|

- stop:
    Stops all containers that were started for current project, without removing containers.

|

- rm:
    Stops all containers that were started for current project and removes related containers.

|

- rmi:
    Stops all containers that were started for current project, removes related containers and related images.

|

- restart:
    This command is equivalent to following two commands running one after another in order such as below::

        1. docker-console stop
        2. docker-console start/up

|

- codecept:
    This command allows to run any codeception command.

|

- test:
    This command runs all tests available in tests location.
    You can also run single test files using argument like **testSuite/testName**. By default tests are run with options --xml --html (codeception run command options).
    Tests can also be run by command::

        docker-console codecept run

|

- config-prepare:
    This command copies the docker-compose-template.yml to docker-compose.yml with replaced variables from .env file.

|

- show-ip:
    Shows web container IP address.

|

- show-nginx-proxy-ip:
    Shows nginx container IP address.

|

- dump:
    This command exports project database to DUMP_EXPORT_LOCATION in DB setting.

|


**Commands for drupal web engine**
==================================

- drush:
    Allows for running any drush command inside docker.

    |

    Options:

    \-e, \--drush-eval-run-code
        Set if you want run code in drush eval.

|

- build:
    This command is running::

        docker-console build-in-docker

    command inside docker and some commands to set proper files permissions.

|

- up-and-build:
    This command is equivalent to following two commands running one after another in order such as below::

        1. docker-console up
        2. docker-console build

|

- build-in-docker,
    This command is responsible for building Drupal application inside docker and it will be not working locally.
    It is used in::

        docker-console build

    command as one of building step.

|

**Global options**
==================
- \--v, \--version
    See application version

|

- \--help
    See help for docker-console, you can also use::

        docker-console help

    command

|

- \-p, \--docker-run-path
    Set path do drupal wrapper with 'docker-compose.yml' files and 'docker' folder

|

- \-y
    Yes to all questions where 'confirm_action' is used in command action steps

|

- \--db
    Set the database you want to work on.

|
|


**Drupal engine specific global options**
=========================================

- \--site
    Set the drupal site you want to work on.


|
|

==============
**DB drivers**
==============
By default, there is available mysql DB driver. This is set in DRIVER param in DB config in <project_name>/docker_console/dc_settings.py::

    DB = {
        'default': {
            'DRIVER': 'mysql',
            ...
        ...

|
|

===============
**Web engines**
===============
By default, there is available drupal7 web engine. New custom engines can be created locally in user home directory. Custom web engines have to be placed in::

    ~/.docker_console/custom_web_engines/

Custom web engine have to contain following files:
    - config/default.py, containing at least line with importing of default config from base engine::

        from docker_console.web.engines.base.conf.default import *

    - builder.py, containing at least Builder class that inherits BaseBuilder class from base engine::

        class Builder(BaseBuilder):
            def __init__(self, config):
                super(Builder, self).__init__(config)

    - commands.py, containing at least line with importing of default commands from base engine::

        from docker_console.web.engines.base.commands import commands

Web engines are python modules, therefore on each directory level you need to add empty files __init__.py. For basic custom web engine this would be::

    ~/.docker_console/custom_web_engines/custom_engine_name/__init__.py
    ~/.docker_console/custom_web_engines/custom_engine_name/conf/__init__.py

If you would like to create custom web engine that overrides other default classes like 'BaseDocker' or 'BaseTests', please look at drupal7 default web engine as an example.

|

To use custom web engine you need to:
    - at the top of <project_name>/docker_console/dc_settings.py, replace line::

        from docker_console.web.engines.{default_engine_name}.conf.default import *

      with::

        from custom_web_engines.{custom_engine_name}.conf.default import *

    - set ENGINE param in WEB config in <project_name>/docker_console/dc_settings.py to your web engine name,
    - set USE_CUSTOM_ENGINE param in WEB config in <project_name>/docker_console/dc_settings.py to True, eg::

        WEB = {
            'ENGINE': 'custom_engine_name',
            'USE_CUSTOM_ENGINE': True,
            ...

    - if you would like to override something from your custom web engine in <project_name>/docker_console/dc_overrides.py, you need to remember to import classes from this custom engine, so import lines should looks like::

        from custom_web_engines.{custom_engine_name}.builder import Builder


Note that this is possible to have custom web engine with the same name as default ones.
If you will have such custom web engine but for some projects you would like to use default engine just set USE_CUSTOM_ENGINE param in WEB config to False.

|
|

======================
**Usage with project**
======================

|

**docker-console initialization in drupal project**
===================================================

To initialize docker-console in drupal project you should use command::

    docker-console init --tpl init_template_name

This command will copy init template files to project wrapper. See description of '- init' command for details.

|

After that, if needed, you should adjust settings for your project in::

    <project_name>/docker_console/dc_settings.py

|

**Adding config entry for project to /etc/hosts**
=================================================

To add config entry for project to /etc/hosts you need to run::

    docker-console add-host-to-etc-hosts

This command adds entry to /etc/hosts with IP Address taken from nginx-proxy container
and hosts names taken from VIRTUAL_HOST variable for web and phpmyadmin containers configuration in docker-compose.yml

|

**Adding project aliases**
==========================

docker-console application allows for defining project aliases like in drush. In alias configuration there is only project wrapper path configuration. This path should be absolute.

|

Alias files have to be placed in::

    ~/.docker_console/aliases/

folder. This folder is automatically created during installation. You can place here as many aliases files as you need, with any number of aliases in each file.

|

Example alias.py file::

    project_1_alias = {
        'path': '/path/to/project1/wrapper/'
    }

    project_2_alias = {
        'path': '/path/to/project2/wrapper/'
    }

    __all__ = ['project_1_alias', 'project_2_alias']

|

If you will create alias for project you will be able to run docker-console from anywhere with project path given in alias::

    docker-console @project_1_alias

|

After adding new aliases, you need to run::

    docker-console refresh-autocomplete

to add autocomplete support for new aliases.


|

**Adjusting default, global configuration options, classes methods and commands to specific project needs, using custom overriding files**
==========================================================================================================================================

|

**Adjusting configuration options**
-----------------------------------

To adjust configuration options you need to modify::

    <project_name>/docker_console/dc_settings.py

file.

|

You can either modify default options values or add new options.

|

Example dc_settings.py file for drupal7 web engine::

    # import default values from drupal7 engine (required)
    from docker_console.web.engines.drupal7.conf.default import *

    #################
    # BASE SETTINGS #
    #################

    WEB = {
        'ENGINE': 'drupal7',
        'USE_CUSTOM_ENGINE': False, # True/False - useful when we have default and custom engine with the same name
        'APP_LOCATION': 'app',
        'APP_CONF_LOCATION': 'app_conf',
        'APP_DATA_LOCATION': 'app_data',
        'TMP_PATH': '/tmp'
    }

    DB = {
        'default': {
            'DRIVER': 'mysql',
            'HOST': 'mysql',
            'NAME': 'db',
            'USER': 'user',
            'PASS': 'pass',
            'ROOT_USER': 'root',
            'ROOT_PASS': '123',
            'DUMP_IMPORT_FILE': 'app_databases/database.sql.tar.gz',
            'DUMP_EXPORT_LOCATION': 'app_databases/',
        }
    }

    TESTS = {
        'IMAGES': {
            'selenium_image': ('selenium/standalone-chrome', None),
            'codecept_image': ('droptica/codecept', None)
        },
        'LOCATION': "tests"
    }

    ENV = None

    ####################
    # DRUPAL7 SETTINGS #
    ####################

    DEV_DOCKER_IMAGES = {
        'default': ('droptica/drupal-dev', None),
        'additional_images': [
    #     ('vendor/image_name', None), # image from dockerhub
    #     ('vendor/image_name', 'path_to_dockerfile') # custom image from Dockerfile
        ]
    }

    DRUPAL = {
        'default': {
            'ADMIN_USER': 'admin',
            'ADMIN_PASS': '123',
            'SITE_URI': 'default.dev',
            'SITE_DIRECTORY': 'default',
            'FILES_DST': 'sites/default/',
            'PRIVATE_FILES_DST': 'sites/default/files/',
            'FILES_ARCHIVE': 'app_files/files.tar.gz',
            'PRIVATE_FILES_ARCHIVE': 'app_files/private.tar.gz',
            'SETTINGS_TEMPLATE_SUBDIR': None,
            'STAGE_FILE_PROXY_URL': None
        }
    }

|

**Adjusting classes methods and commands**
------------------------------------------

To adjust classes methods or commands you need to modify::

    <project_name>/docker_console/dc_overrides.py

file.

You can either replace existing classes methods or add new methods. Methods from classes can be used create new or replace existing commands locally in project context.

Example dc_overrides.py file for drupal7 web engine::


    # import classes to override
    from docker_console.web.engines.drupal7.drush import Drush
    from docker_console.web.engines.drupal7.builder import Builder

    # add new methods
    class DrushLocal:
        def localtest(self, text):
            print text

    Drush.__bases__ += (DrushLocal,)

    class BuilderLocal:
        def printlocal(self):
            self.drush.localtest('printlocal')

    Builder.__bases__ += (BuilderLocal,)

    # override existing method
    def drush_uli_local(self):
        print self.config.DRUPAL[self.config.drupal_site]['ADMIN_USER']

    Drush.uli = drush_uli_local


    # replace/add new commands
    commands_overrides = {
        'localtest': [
            'confirm_action',
            'drush.localtest("upwd %s --password=123" % self.config.DRUPAL[self.config.drupal_site]["ADMIN_USER"])'
        ],
        'drush_uli': [
            'confirm_action("no")',
            'drush.uli'
        ],
    }

