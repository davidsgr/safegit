#!/usr/bin/env python

import sys
from subprocess import run

# -------------------------------------------------------------------------#
def safe_clone(machine_name, args):
    """Perform a safe git clone, correctly setting access permissions"""

    # Get any options sent to git
    options = [v for v in args if v[0] == '-']

    # Get the repo URL
    if len(args) == len(options):
        raise RuntimeError("fatal: You must specify a repository to clone.")
    repo = args[len(options)]

    # Get the name of the code being cloned
    code_name = repo.split('/')[1].split('.git')[0]
    
    # Get the directory, if specified
    directory = code_name
    if len(args) > len(options) + 1:
        directory = args[-1]
        
    # Perform the clone
    run(['git', 'clone'] + options + [repo, directory])

    # Define the machines where we must set permissions
    machines = ['apollo.ornl.gov', 'remus.ornl.gov', 'romulus.ornl.gov']

    # Define the groups for each code
    codes = {'scale' : 'scale6',
              'terrenus' : 'terrenus'}

    # Fix the permissions if necessary
    if machine_name in machines and code_name in codes:
        print("Setting permissions in " + directory + " to 750")
        run(['chmod', '750', directory])
        print("Changing group in " + directory + " to " + codes[code_name])
        run(['chgrp', codes[code_name], directory])  
        
# -------------------------------------------------------------------------#
def safe_git(machine_name, args):
    """Performs a safe execution of git, preserving correct permissions"""

    # Argument to git is clone. Perform a safe clone
    if args[0] == 'clone':
        safe_clone(machine_name, args[1:])

    # Argument is something other than clone.
    else:
        run(['git'] + args)

# -------------------------------------------------------------------------#
def get_machine_name(args):
    """Gets the machine name if present.  Raises if invalid machine name"""
    assert len(args) > 0

    machine_name = str()
    if '--machine-name' in args[0]:
        tokens = args[0].split('=')
        if len(tokens) != 2:
            raise RuntimeError('No valid machine name specified')
        machine_name = tokens[1]
        args = args[1:]
    else:
        # Get the machine name, peeling off '\n'
        machine_name = run(['uname', '-n'], capture_output=True,
                           text=True).stdout[:-1]
        
    # Check that we're not on a compute node
    if 'node' in machine_name:
        raise RuntimeError('fatal: safegit is being run from a compute node. '
                           'Machine name must be specified') 
    return machine_name, args
    
# -------------------------------------------------------------------------#
if __name__ == '__main__':
    # Ensure we're using Python 3.5 or greater (needed for subprocess.run)
    if sys.version_info[0] < 3 or \
        (sys.version_info[0] == 3 and sys.version_info[1] < 5):
        raise RuntimeError("This script requires python version >= 3.5")

    # Check correct usage
    if len(sys.argv) == 1:
        print('Usage: safe_git [--machine-name=mach_name] git_commands')
        run(['git'])
    else:
        machine_name, args = get_machine_name(sys.argv[1:])
        safe_git(machine_name, args)
