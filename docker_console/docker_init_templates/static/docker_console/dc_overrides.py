# # import classes to override
# from docker_console.web.engines.static.builder import Builder
#
# class BuilderLocal:
#     def printlocal(self):
#         self.drush.localtest('printlocal')
#
# Builder.__bases__ += (BuilderLocal,)
#
#
# # replace/add new commands
# commands_overrides = {
#     'printlocal': [
#         'printlocal'
#     ],
# }
