Application for running Drupal projects on Docker.

|

=========
**Setup**
=========

|

**docker-drupal package installation**
======================================

Requirements for docker-drupal:

* Python 2.7
* setuptools
* pyyaml
|
* docker
* docker-compose


When this requirements are satisfied, you can download docker-drupal package, unzip and go to unzipped directory with setup.py file. Then you can install package using command::

    sudo python setup.py install

|


**docker-drupal package update**
================================
To update docker-drupal package, you need to do the same steps as for installation.

|

**Autocomplete activation**
===========================

During package installation, bash completion scripts are placed in::

    /usr/share/bash-completion/completions/docker-drupal

|

To activate docker-drupal commands and options completion, you need to logout and login again, or type::

    exec bash

without logging out.

|
|

==================================
**Available commands and options**
==================================

|

**Commands that can be run from anywhere**
==========================================

- default:
    Default action if no command spefified. This command is equivalent to::

        docker-drupal
    and::

        docker-drupal help

|

- help:
    Print available options, aliases AND commands including commands added locally for project in docker_drupal_overrides.py (if you are running this command in project wrapper).
    If you use --help option, you will not see available commands, but you can always use::

        docker-drupal <tab><tab>
    to see this available commands. Note that autocomplete mechanism is not working for commands added locally for project in docker_drupal_overrides.py.

    |

    This command is equivalent to::

        docker-drupal
    and::

        docker-drupal default
|

- init:
    This command is copying following files from docker-drupal default templates to project wrapper:
        - docker-compose.yml,
        - docker-compose-jenkins.yml,
        - docker/my.conf,
        - docker/docker_drupal/docker_drupal_overrides.py,
        - docker/docker_drupal/docker_drupal_config_overrides.py
    Files existing in project wrapper localization, by default will not be replaced.

    |

    Options:

    \-f, \--force-replace-conf
        Set if you want force replace your existing config files listed above.
        All your changes in listed files will be irrevocably lost. Other files in wrapper folder and 'docker' folder will stay unchanged.

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

        docker-drupal start

|

- start:
    Start all containers defined in docker-compose.yml

    |

    This command is equivalent to::

        docker-drupal up

|

- stop:
    Stops all containers that were started for current project.

|

- restart:
    This command is equivalent to following two commands running one after another in order such as below::

        1. docker-drupal stop
        2. docker-drupal start/up

|

- drush:
    Allows for running any drush command inside docker.

    |

    Options:

    \-e, \--drush-eval-run-code
        Set if you want run code in drush eval.

|

- jenkins-prepare:
    Adds configuration options that are needed to run project on Jenkins environment.

|

- build:
    This command is running::

        docker-drupal build-in-docker

    command inside docker and some commands to set proper files permissions.

|

- up-and-build:
    This command is equivalent to following two commands running one after another in order such as below::

        1. docker-drupal up
        2. docker-drupal build

|

- build-in-docker,
    This command is responsible for building Drupal application inside docker and it will be not working locally.
    It is used in::

        docker-drupal build

    command as one of building step.

|

**Global options**
==================
- \--v, \--version
    See application version

|

- \--help
    See help for docker-drupal, you can also use::

        docker-drupal help
    command

|

- \-p, \--docker-run-path
    Set path do drupal wrapper with 'docker-compose.yml' files and 'docker' folder

|

- \-y
    Yes to all questions where 'confirm_action' is used in command action steps

|
|

=============================
**Usage with Drupal project**
=============================

|

**docker-drupal initialization in drupal project**
==================================================

To initialize docker-drupal in drupal project you can either manually create following files:

- docker-compose.yml,
- docker/docker_drupal/docker_drupal_overrides.py,
- docker/docker_drupal/docker_drupal_config_overrides.py

|

, or run::

    docker-drupal init
command. This command will copy this files and some other additional files:

- docker-compose-jenkins.yml,
- docker/my.conf,

|

from default package templates to your project wrapper. If you are creating **docker/docker_drupal/docker_drupal_config_overrides.py** file manually,
you should **look at the source of docker_drupal package conf/default.py** file to see what config options are available and what are default values.

After that, you should adjust settings for your project in::

    <project_name>/docker/docker_drupal/docker_drupal_config_overrides.py
file if needed.


|

**Adding config entry for project to /etc/hosts**
=================================================

To add config entry for project to /etc/hosts you need to run::

    docker-drupal add-host-to-etc-hosts

This command will run docker for current project and add entry to /etc/hosts with IP Address taken from web container
and hosts names taken from VIRTUAL_HOST variable for web and phpmyadmin containers configuration in docker-compose.yml

|

**Adding Project Aliases**
==========================

docker-drupal application allows for defining project aliases like in drush. In alias configuration there is only project wrapper path configuration. This path should be absolute.

|

Alias files have to be placed in::

    ~/.docker_drupal/aliases/
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

If you will create alias for project you will be able to run docker-drupal from anywhere with project path given in alias::

    docker-drupal @project_1_alias

|

After adding new aliases, you need to run::

    docker-drupal refresh-autocomplete
to add autocomplete support for new aliases.


|

**Adjusting default, global configuration options, classes methods and commands to specific project needs, using custom overriding files**
=======================================================================================================================================

|

**Adjusting configuration options**
-----------------------------------

To adjust configuration options you need to modify::

    <project_name>/docker/docker_drupal/docker_drupal_config_overrides.py
file.

|

You can either modify default options values or add new options.

|

Example docker_drupal_config_overrides.py file::

    DB_NAME = "not_standard_db_name"

    DB_USER = "not_standard_db_username"

    DB_PASSWORD = "not_standard_db_userpass"

    DRUPAL_LOCATION = "some_dir"

|

**Adjusting classes methods and commands**
------------------------------------------

To adjust classes methods or commands you need to modify::

    <project_name>/docker/docker_drupal/docker_drupal_overrides.py
file.

You can either replace existing classes methods or add new methods. Methods from classes can be used create new or replace existing commands locally in project context.

Example docker_drupal_overrides.py file::


    #import classes to override
    from docker_drupal.drush import Drush
    from docker_drupal.builder import Builder

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
        print self.config.DRUPAL_ADMIN_USER

    Drush.uli = drush_uli_local


    # replace/add new commands
    build_arrays_overrides = {
        'localtest': ['confirm_action', 'drush.localtest("upwd %s --password=123" % self.config.DRUPAL_ADMIN_USER)'],
        'drush_uli': ['confirm_action("no")', 'drush.uli'],
    }