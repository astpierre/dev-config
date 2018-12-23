#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# Written by:   Andrew St. Pierre
# Description:  Script to configure Ubuntu desktop for development
# Usage:        $ sudo ./dev_config.py
###############################################################################
import os
import sys
import platform
import getopt
import shutil
import logging
import getpass
import yaml


# Global variables
#-----------------------------------------------------------------------------
VERSION = "1.1.0"
OPTIONS_FILE = "configs.yml"

# System commands
#-----------------------------------------------------------------------------
_APT_ADD = "add-apt-repository -y"
_APT_INSTALL = "DEBIAN_FRONTEND=noninteractive apt-get -y -f install"
_APT_REMOVE = "DEBIAN_FRONTEND=noninteractive apt-get -y -f remove"
_APT_UPDATE = "DEBIAN_FRONTEND=noninteractive apt-get -y update"
_APT_UPGRADE = "DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"
_WGET = "wget"

# Classes
#-----------------------------------------------------------------------------
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ORANGE = '\033[93m'
    NO = '\033[0m'

    def disable(self):
        self.RED = ''
        self.GREEN = ''
        self.BLUE = ''
        self.ORANGE = ''
        self.NO = ''

# Functions
#-----------------------------------------------------------------------------
def init():
    """
    Init the script
    """
    # Globals variables
    global VERSION

def syntax():
    """
    Print the script syntax
    """
    print("Ubuntu 18.10 development configuration script version %s\n" % VERSION)
    print("Usage: sudo dev_config.py [-h] [-v]")
    print("  -h         : Print the syntax and exit")
    print("  -v         : Print the version and exit\n")
    print("Examples:\n")
    print(" # sudo dev_config.py")
    print(" > Run the script with the default configuration file")
    print("   %s\n\n" % OPTIONS_FILE)

def version():
    """
    Print the script version
    """
    sys.stdout.write("Script version %s" % VERSION)
    sys.stdout.write(" (running on %s %s)\n" % (platform.system(), platform.machine()))

def isroot():
    """
    Check if the user is root
    Return TRUE if user is root
    """
    return(os.geteuid() == 0)

def showexec(description, command, exitonerror = 0, presskey = 0, waitmessage = ""):
    """
    Exec a system cmd w a pretty status display (Running / Ok / Warning / Error)
    By default (exitcode=0), the function did not exit if the command failed
    """

    # Wait message
    if (waitmessage == ""):
        waitmessage = description

    # Manage very long description
    if (len(waitmessage) > 65):
        waitmessage = waitmessage[0:65] + "..."
    if (len(description) > 65):
        description = description[0:65] + "..."

    # Display the command
    if (presskey == 1):
        status = "[ ENTER ]"
    else:
        status = "[Running]"
    statuscolor = colors.ORANGE
    sys.stdout.write(colors.NO + "%s" % waitmessage + statuscolor + "%s" % status.rjust(79-len(waitmessage)) + colors.NO)
    sys.stdout.flush()

    # Wait keypressed (optionnal)
    if (presskey == 1):
        try:
            input = raw_input
        except:
            pass
        raw_input()

    # Run the command
    returncode = os.system("/bin/sh -c \"%s\" >> /dev/null 2>&1" % command)

    # Display the result
    if ((returncode == 0) or (returncode == 25600)):
        status = "[  OK   ]"
        statuscolor = colors.GREEN
    else:
        if exitonerror == 0:
            status = "[Warning]"
            statuscolor = colors.ORANGE
        else:
            status = "[ Error ]"
            statuscolor = colors.RED

    sys.stdout.write(colors.NO + "\r%s" % description + statuscolor + "%s\n" % status.rjust(79-len(description)) + colors.NO)

    # Stop the program if returncode and exitonerror != 0
    if ((returncode != 0) & (exitonerror != 0)):
        exit(exitonerror)

def getpassword(description = ""):
    """
    Read password (with confirmation)
    """
    if (description != ""):
        sys.stdout.write ("%s\n" % description)

    password1 = getpass.getpass("Password: ");
    password2 = getpass.getpass("Password (confirm): ");

    if (password1 == password2):
        return password1
    else:
        sys.stdout.write (colors.ORANGE + "[Warning] Password did not match, please try again" + colors.NO + "\n")
        return getpassword()

def getstring(message = "Enter a value: "):
    """
    Ask user to enter a value
    """
    try:
        inpt = input(message)
    except:
        pass
    return inpt

def waitenterpressed(message = "Press ENTER to continue..."):
    """
    Wait until ENTER is pressed
    """
    try:
        input = raw_input
    except:
        pass
    raw_input(message)
    return 0

def main(argv):
    """
    Main function
    """
    # Parse the input arguments
    try:
        opts, args = getopt.getopt(argv, "c:hv", ["config", "help", "version"])
    except getopt.GetoptError:
        syntax()
        exit(2)

    # The default configurations file
    config_file = OPTIONS_FILE

    # Check if user wants to use help or see version
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            syntax()
            exit()
        elif opt in ('-v', "--version"):
            version()
            exit()

    # Are you root?
    if(not isroot()):
        showexec ("Script should be run as root", " ", exitonerror = 1)

    # Check the Ubuntu version (TODO: get more user info)
    UBUNTU_VERSION = os.uname()

    # Read the configuration file
    with open(config_file, 'r') as fyaml:
        configs = yaml.load(fyaml)

    # Install all requested packages
    '''
    if "packages" in configs:
        # Parse and exec pre-actions
        for pckg in configs["packages"]:
            # TESTING WITH virtualenv and htop
            command_install = _APT_INSTALL+" "+pckg
            showexec("Install package "+pckg, command_install)
        # Update repos
        showexec ("Update repositories", _APT_UPDATE)
        # Upgrade system
        showexec ("System upgrade (takes a while, be patient...)", _APT_UPGRADE)
    '''
    # Download the dotfiles from specified locations and use them
    '''
    if "dotfiles" in configs:
        for df in configs["dotfiles"]:
            if df == "bashrc":
                url = configs["dotfiles"]["bashrc"]
                showexec("Downloading .bashrc from github...", _WGET+" -O $HOME/.bashrc.bak "+url)
                showexec("Moving .bashrc into proper file...", "mv $HOME/.bashrc.bak $HOME/.bashrc")

            elif df == "bash_aliases":
                url = configs["dotfiles"]["bash_aliases"]
                showexec("Downloading .bash_aliases from github...", _WGET+" -O $HOME/.bash_aliases.bak "+url)
                showexec("Moving .bash_aliases into proper file...", "mv $HOME/.bash_aliases.bak $HOME/.bash_aliases")
            else: print("Unrecognized dotfile category: %s"%df)
        showexec("Running your new .bashrc script!", "source $HOME/.bashrc")
    '''
    # Clone the vimrc settings into home dir and add mouse clicking too
    '''
    if "vimrc" in configs:
        instr = configs["vimrc"]["clone"]
        showexec("Cloning the vim settings repo from github...", instr+" $HOME")
        with open("$HOME/.vimrc", "a") as vmrc:
            vmrc.write(configs["vimrc"]["addMouse"])
        instr = configs["vimrc"]["runit"]
        showexec("Implementing your new vim preferences...", instr)
    '''
    # End of the script
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("End of the configuration script.")
    print(" => configuration file: "+config_file+"\n")
    print("Restart your session to complete.")
    if(getstring("Would you like to reboot now? (y/n)") == "y"):
        print("REBOOT COMMENTED OUT...")
        #os.system("reboot")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# Main program
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    init()
    main(sys.argv[1:])
    exit()
