#! env python

import sys
from subprocess import call

# -------------------------------------------------------------------------#
def safe_clone(args):
    """Perform a safe git clone, correctly setting access permissions"""

    # Get the machine name
    machine_name = call('uname --n')
    print(machine_name)

    # Get any options sent to git
    options = [v for v in args if v[0] == '-']
    print(options)

    # Get the repo URL
    if len(args) == len(options):
        raise RunTimeError("fatal: You must specify a repository to clone.")
    repo = args[len(options)]

    # Get the directory, if specified
    directory == "scale"
    if len(args) > len(options+1):
        directory = args[-1]

    # Perform the clone
    opt_str = str().join(options, " ")
    call('git clone ' + opt_str + ' ' + repo + ' ' + directory)

    # Set the permissions correctly
    if repo.split('/')[-1] == 'scale' or repo.split('/')[-1] == "scale.git":
        call('chmod 750 ' + directory)
        call('chgrp scale6 ' + directory)
    
# -------------------------------------------------------------------------#
def safe_git(args):
    """Performs a safe execution of git, preserving correct permissions"""

    # User has called git with no arguments
    if len(args) == 0:
        call('git')

    # User has called with with arguments
    else:
        # Argument to git is clone. Perform a safe clone
        if args[1] == 'clone':
            safe_clone(args[2:])

        # Argument is something other than clone.
        else:
            command = str()
            command.join(args, " ")
            call(command)

# -------------------------------------------------------------------------#
if '__name__' == '__main__':
    safe_git(sys.argsv)
    return 0
    
