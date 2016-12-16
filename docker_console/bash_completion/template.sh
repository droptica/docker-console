#!/bin/bash

# save extglob settings
__docker_console_previous_extglob_setting=$(shopt -p extglob)
shopt -s extglob

# Transforms a multiline list of strings into a single line string
# with the words separated by "|".
# This is used to prepare arguments to __docker_console_pos_first_nonflag().
__docker_console_to_alternatives() {
	local parts=( $1 )
	local IFS='|'
	echo "${parts[*]}"
}

# Transforms a multiline list of options into an extglob pattern
# suitable for use in case statements.
__docker_console_to_extglob() {
	local extglob=$( __docker_console_to_alternatives "$1" )
	echo "@($extglob)"
}

# Finds the position of the first word that is neither option nor an option's argument.
# If there are options that require arguments, you should pass a glob describing those
# options, e.g. "--option1|-o|--option2"
# Use this function to restrict completions to exact positions after the argument list.
__docker_console_pos_first_nonflag() {
	local argument_flags=$1

	local counter=$((${subcommand_pos:-${command_pos}} + 1))
	while [ $counter -le $cword ]; do
		if [ -n "$argument_flags" ] && eval "case '${words[$counter]}' in $argument_flags) true ;; *) false ;; esac"; then
			(( counter++ ))
			# eat "=" in case of --option=arg syntax
			[ "${words[$counter]}" = "=" ] && (( counter++ ))
		else
			case "${words[$counter]}" in
				-*)
					;;
				@*)
					;;
				*)
					break
					;;
			esac
		fi

		# Bash splits words at "=", retaining "=" as a word, examples:
		# "--debug=false" => 3 words, "--log-opt syslog-facility=daemon" => 4 words
		while [ "${words[$counter + 1]}" = "=" ] ; do
			counter=$(( counter + 2))
		done

		(( counter++ ))
	done

	echo $counter
}

## autocomplete absolute path
#_path_autocomplete(){
#    echo -n "$1" | xargs -d: -I{} -r -- find -L {} -maxdepth 1 -mindepth 1 -type d -printf '%p\n' 2>/dev/null | sort -u
#}

# global options that may appear after the docker-console command
_docker_console_docker_console() {
	local boolean_options="
		$global_boolean_options
		--help
        --v --version
	"

	case "$prev" in
	    # autocomplete path
		--docker-run-path|-p)
			compopt -o dirnames
			;;
		$(__docker_console_to_extglob "$global_options_with_args") )
			return
			;;
	esac

	case "$cur" in
	    # autocomplete options
		-*)
			COMPREPLY=( $( compgen -W "$boolean_options $global_options_with_args" -- "$cur" ) )
			;;

	    # autocomplete aliases
		@*)
			COMPREPLY=( $( compgen -W "$global_aliases" -- "$cur" ) )
			;;

	    # autocomplete commands
		*)
			local counter=$( __docker_console_pos_first_nonflag $(__docker_console_to_extglob "$global_options_with_args") )
			if [ $cword -eq $counter ]; then
				COMPREPLY=( $( compgen -W "${commands[*]} help" -- "$cur" ) )
			fi
			;;
	esac
}

{{commands_completion_functions}}

_docker_console() {
	local previous_extglob_setting=$(shopt -p extglob)
	shopt -s extglob

    # define available commands
	local commands=(
		{{commands}}
	)

    # define available aliases
	local global_aliases="
		{{global_aliases}}
	"

    # define available boolean options
	local global_boolean_options="
		{{global_boolean_options}}
	"

    # define available options with arguments
	local global_options_with_args="
		{{global_options_with_args}}
	"

    # define variables that will be store arguments values
	local docker_run_path

	COMPREPLY=()
	local cur prev words cword
	_get_comp_words_by_ref -n : cur prev words cword

    # default command to run completion function (_docker_console_${command} will be _docker_console_docker_console)
	local command='docker_console' command_pos=0 subcommand_pos
	local counter=1
	while [ $counter -lt $cword ]; do
		case "${words[$counter]}" in

			# save docker-run-path
			--docker-run-path|-p)
				(( counter++ ))
				docker_run_path="${words[$counter]}"
				;;

			# prevent handle global args as commands
			$(__docker_console_to_extglob "$global_options_with_args") )
				(( counter++ ))
				;;

            # prevent handle options as commands
			-*)
				;;

            # prevent handle aliases as commands
			@*)
				;;

            # prevent handle arguments as commands
			=)
				(( counter++ ))
				;;

			# if no char -, @, or = this is command, run separate completion function
			*)
				command="${words[$counter]}"
				command_pos=$counter
				break
				;;
		esac
		(( counter++ ))
	done

    # run separate complete function for command
	local completions_func=_docker_console_${command}
	declare -F $completions_func >/dev/null && $completions_func

    # revert extglob settings
	eval "$previous_extglob_setting"

	return 0
}

# revert extglob settings
eval "$__docker_console_previous_extglob_setting"
unset __docker_console_previous_extglob_setting

complete -F _docker_console docker-console dcon
