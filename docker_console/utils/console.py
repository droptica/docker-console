import sys, os
import subprocess
import functools
import struct

def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

def bcolors():
    return {
        'HEADER': '\033[95m',
        'OKBLUE': '\033[94m',
        'OKGREEN': '\033[92m',
        'WARNING': '\033[93m',
        'FAIL': '\033[91m',
        'ENDC': '\033[0m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
    }

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    parts = []
    for start in range(0, len(s), n):
        parts.append(s[start:start+n])
    return parts

def message(message, type=""):
    bc = bcolors()
    style = bc['OKBLUE']
    if type == 'error':
        style = bc['FAIL'] + bc['BOLD']
    if type == 'warning':
        style = bc['WARNING'] + bc['BOLD']
    if type == 'info':
        style = bc['OKGREEN'] + bc['BOLD']
    if type == 'white':
        style = bc['ENDC']

    width = 88
    height = 23
    signs_length = 10 + len(message)

    if signs_length > width:
        signs_length = width
    print style + (signs_length * "#")
    message_parts = chunks(message, width-10)
    for idx, chunk in enumerate(message_parts):
        if idx < len(message_parts) - 1 or signs_length < width:
            print (3 * "#") + "  " + chunk + "  " + (3 * "#")
        else:
            white_spaces_to_add = int((width - len(chunk) - 8) / 2)
            print (3 * "#") + "  " + chunk + (white_spaces_to_add * "  ") + (3 * "#")
    print (signs_length * "#") + bc['ENDC']


def run(command, cwd=None, return_output=False):
    try:
        message('Run: "' + command + '"')
        if return_output:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
            while True:
                error_lines = process.stderr.readlines()
                output = ''.join(error_lines)
                output_lines = process.stdout.readlines()
                output += ''.join(output_lines)

                if output == '' and process.poll() is not None:
                    break
                if output:
                    return output.strip('\t\n')
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=cwd)
            while True:
                output = process.stdout.readline()

                if output == '' and process.poll() is not None:
                    break
                if output:
                    print output.strip('\t\n')
        rc = process.poll()
        return rc
    except Exception as error:
        message('Error: "%s"' % command, 'error')
        print error

def call(command, cwd=None):
    try:
        message('Run: "' + command + '"')
        subprocess.call(command, shell=True)
    except Exception as error:
        message('Error: "%s"' % command, 'error')
        print error

def rgetattr(obj, attr):
    return functools.reduce(getattr, [obj]+attr.split('.'))

def query_yes_no(question, default=None, yes_to_all=False):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    if yes_to_all:
        return True
    else:
        while True:
            sys.stdout.write(question + "\n" + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

#TODO: fix size of output
