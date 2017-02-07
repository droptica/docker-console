import os
from ..utils.aliases import __all__ as available_aliases


def get_available_commands():
    from docker_console.__main__ import build_arrays
    from copy import deepcopy
    build_arrays_cpy = deepcopy(build_arrays)
    del build_arrays_cpy['build-in-docker']
    return """ {0} """.format("\n".join(build_arrays_cpy.keys()))

def get_commands_completion_functions():
    return """
_docker_console_init() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "-f --force-replace-conf" -- "$cur" ) )
			;;
	esac
}

_docker_console_shell() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "-s --docker-shell-run -c --docker-container" -- "$cur" ) )
			;;
	esac
}

_docker_console_drush() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "-e --drush-eval-run" -- "$cur" ) )
			;;
	esac
}
"""

def get_aliases():
    return """ {0} """.format("\n".join('@%s' % alias for alias in available_aliases[:]))

def get_boolean_options():
    return """
        -y
    """

def get_options_with_args():
    return """
        -p --docker-run-path
        -s --docker-shell-run
        -c --docker-container
    """

def setup_autocomplete():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'bash_completion', 'template.sh'), 'rt') as f:
            content = f.read()
            content = content.replace('{{commands_completion_functions}}', get_commands_completion_functions())
            content = content.replace('{{commands}}', get_available_commands())
            content = content.replace('{{global_aliases}}', get_aliases())
            content = content.replace('{{global_boolean_options}}', get_boolean_options())
            content = content.replace('{{global_options_with_args}}', get_options_with_args())

            with open('/tmp/bash_completion.tmp', 'wt') as outf:
              outf.write(content)

            os.system('sudo mv /tmp/bash_completion.tmp /usr/share/bash-completion/completions/docker-console')
            os.system('sudo ln -sf /usr/share/bash-completion/completions/docker-console /usr/share/bash-completion/completions/dcon')
    except:
          pass
