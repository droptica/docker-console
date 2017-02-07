# Changelog

## (unreleased)

### 

* 2aa0105 (2017-01-19) [Damian Sikora]

  add changelog


* ad8d65c (2017-01-19) [Damian Sikora]

  add changelog



## v1.0.4 (2017-01-12)

### 

* 7069da5 (2017-01-12) [Maciej Lukianski]

  version


* 462255f (2017-01-12) [Damian Sikora]

  readme update


* 55c9ea4 (2017-01-12) [Damian Sikora]

  readme update


* 6125db3 (2017-01-12) [Maciej Lukianski]

  update commands


* 96ba46c (2017-01-11) [Maciej Lukianski]

  d8 setups


* fd4b115 (2017-01-05) [Maciej Lukianski]

  7 to 8


* 715ed6b (2017-01-05) [Maciej Lukianski]

  drupal8 init template


* e3ca6d3 (2017-01-12) [Damian Sikora]

  readme update



## v1.0.3 (2016-12-23)

### 

* ea7d9fb (2016-12-23) [Damian Sikora]

  restructure


* 3710eea (2016-12-23) [Damian Sikora]

  restructure


* 4813585 (2016-12-23) [Damian Sikora]

  restructure


* b4b1f8f (2016-12-22) [Damian Sikora]

  restructure


* 865271a (2016-12-21) [Damian Sikora]

  restructure


* b4600df (2016-12-20) [Damian Sikora]

  restructure



## v0.2.18 (2016-12-16)

### 

* 385f797 (2016-12-16) [Damian Sikora]

  update 'init-tests' command - add DrupalHelper class to default helpers


* 19105df (2016-12-16) [Damian Sikora]

  update 'migrate-to-dcon' command; add checks if override files are migrated from docker_drupal


* be075dd (2016-12-16) [Damian Sikora]

  improvements:
  - autocomplete fix that enables autoconplete with aliases
  - update command 'migrate-to-dcon' - change override files names and location, replace usage of docker_drupal to docker_console
  - update command 'test' and 'codecept' to use selenium only when executing 'codecept run'


* 87956cf (2016-12-15) [Damian Sikora]

  improvements:
  - copy aliases during install from ~/.docker_drupal/aliases to ~/.docker_console/aliases
  - add command 'migrate-to-dcon' to copy project overrides from wrapper/docker/docker_drupal to wrapper/docker_console
  - add command 'codecept' to make codecept image available for running any command manually
  - add tests_setup_defaults dir with basic tests config
  - add command 'init-tests' that sets up basic tests config in project (copy content of tests_setup_defaults to project wrapper)
  - update 'test' command - run 'codecept build' before 'codecept run'


* f2f2d1e (2016-12-15) [Damian Sikora]

  fix for setup on debian


* cf9c1b6 (2016-12-15) [Damian Sikora]

  improvements:
  - add command alias: dcon
  - update readme
  - update default config overrides


* 2583c9b (2016-12-14) [Damian Sikora]

  package name change to docker-console


* 433528e (2016-12-13) [Damian Sikora]

  remove fra and updb from default build


* 1d6f590 (2016-12-13) [Damian Sikora]

  improvements:
  - update 'restart' command to neither remove containers nor update images during restart
  - move codecept image from additional_images to separate entry in DEV_DOCKER_IMAGES config
  - add selenium_image entry in DEV_DOCKER_IMAGES config and use in 'test' command
  - add TESTS_LOCATION config and use in 'test' config
  - fix typo 'ngnix-proxy' in Docker.get_nginx_proxy_ip function


* b0666e4 (2016-12-12) [Damian Sikora]

  improvements:
  - change default 'up', 'start' and 'up-and-build' commands behavior to not pull or build images
  - added new command 'update-images' that pulls and builds images
  - change default 'stop' command behavior to not remove containers after stop
  - added new command 'rm' that stops and removes project containers
  - added new command 'rmi' that stops and removes project containers and related images if possible (without force)
  - updated 'test' command to use default testing image (droptica/codecept)
  - updated method 'Docker._get_hosts' to add links to containers with name from docker-compose.yml config
  - added new command 'dump' that dumps project database to databases dir in project wrapper



## v0.1.0 (2016-12-12)

### 

* 297f6c4 (2016-12-12) [Damian Sikora]

  cleanup


* 9317f12 (2016-12-12) [Damian Sikora]

  cleanup


* c5d652d (2016-06-24) [wodzik]

  Issue #0 - default admin user


* a8c6c80 (2016-06-24) [wodzik]

  Issue #0 - test run


* 514bc6c (2016-06-24) [wodzik]

  Issue #0 - test run


* 8b309db (2016-06-15) [wodzik]

  Issue #0 - archive


* e0aa8fb (2016-06-09) [wodzik]

  Fix project name, private files, db import fix


* edf4dba (2016-06-09) [wodzik]

  Fix project name, private files, db import fix


* 10872b3 (2016-06-08) [wodzik]

  Issue #0 - site uri


* a9f3744 (2016-06-03) [wodzik]

  Docker -it fix


* 21a88ef (2016-05-27) [Maciej Lukianski]

  default uri changed to &quot;default&quot;


* ebee6e4 (2016-05-24) [Maciej Lukianski]

  enable xdebug


* 10676d1 (2016-05-27) [wodzik]

  ENV


* d2a1df8 (2016-05-22) [Damian Sikora]

  fixes


* 3d9e0b2 (2016-05-22) [Damian Sikora]

  fix


* 39bcda0 (2016-05-22) [Damian Sikora]

  conflicts


* 919479b (2016-05-22) [Damian Sikora]

  docker drupal



