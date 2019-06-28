# # import classes to override
# from docker_console.web.engines.drupal7.drush import Drush
# from docker_console.web.engines.drupal7.builder import Builder
#
# # add new methods
# class DrushLocal:
#     def localtest(self, text):
#         print text
#
# Drush.__bases__ += (DrushLocal,)
#
# class BuilderLocal:
#     def printlocal(self):
#         self.drush.localtest('printlocal')
#
# Builder.__bases__ += (BuilderLocal,)
#
# # override existing method
# def drush_uli_local(self):
#     print self.config.DRUPAL[self.config.drupal_site]['ADMIN_USER']
#
# Drush.uli = drush_uli_local
#
#
# # replace/add new commands
# commands_overrides = {
#     'localtest': [
#         'confirm_action',
#         'drush.localtest("upwd %s --password=123" % self.config.DRUPAL[self.config.drupal_site]["ADMIN_USER"])'
#     ],
#     'drush_uli': [
#         'confirm_action("no")',
#         'drush.uli'
#     ],
#     # When files should be unpacked during build, whole 'build-in-docker' command needs to be overridden and
#     # step 'archive.unpack_files' needs to be added to the list of steps, like below:
#     'build-in-docker': [
#         'archive.unpack_files(True)', # True when existing files should be overridden with new ones, default is False.
#         'drupal_settings.copy_settings("drupal7")',
#         'database.drop_db',
#         'database.create_db',
#         'database.import_db',
#         'drush.cc_all', # or 'drush.run("cc all")',
#         'drush.change_password',
#         'drush.uli' # or 'drush.run("uli")'
#     ],
# }
