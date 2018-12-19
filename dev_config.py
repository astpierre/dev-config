#!/usr/bin/env python
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
import ConfigParser

# Global variables
#-----------------------------------------------------------------------------
_VERSION = "1.0.0"
_CONF_FILE = "dev_config.cfg"

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
    global _VERSION
    global _DEBUG

def syntax():
    """
    Print the script syntax
    """
    print "Ubuntu 18.10 development configuration script version %s\n" % _VERSION
    print "Usage: sudo dev_config.py [-h] [-v]"
    print "  -h         : Print the syntax and exit"
    print "  -v         : Print the version and exit\n"
    print "Examples:\n"
    print " # sudo dev_config.py"
    print " > Run the script with the default configuration file"
    print "   %s\n\n" % _CONF_FILE

def version():
    """
    Print the script version
    """
    sys.stdout.write("Script version %s" % _VERSION)
    sys.stdout.write(" (running on %s %s)\n" % (platform.system(), platform.machine()))

def isroot():
    """
    Check if the user is root
    Return TRUE if user is root
    """
    return (os.geteuid() == 0)

def showexec(description, command, exitonerror = 0, presskey = 0, waitmessage = ""):
    """
    Exec a system command with a pretty status display (Running / Ok / Warning / Error)
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
    statuscolor = colors.BLUE
    sys.stdout.write (colors.NO + "%s" % waitmessage + statuscolor + "%s" % status.rjust(79-len(waitmessage)) + colors.NO)
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
        input = raw_input
    except:
        pass
    return raw_input(message)

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
    try:
        opts, args = getopt.getopt(argv, "c:hv", ["config", "help", "version"])
    except getopt.GetoptError:
        syntax()
        exit(2)

    config_file = ""
    config_url = _CONF_FILE

    # Check if user wants to use help or see version
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            syntax()
            exit()
        elif opt in ('-v', "--version"):
            version()
            exit()

    # Are your root ?
    if(not isroot()):
        showexec ("Script should be run as root", " ", exitonerror = 1)

    # Check the Ubuntu version
    _UBUNTU_VERSION = os.uname()

    # Read the configuration file
    if (config_file == ""):
        config_file = "dev_config.cfg"
        #showexec ("Download the configuration file", "rm -f "+config_file+" ; "+_WGET+" -O "+config_file+" "+config_url)
    #config = ConfigParser.RawConfigParser()
    #config.read(config_file)

    '''
    if (config.has_section("gnome3") and config.has_section("unity")):
        showexec ("Can not use both Gnome 3 and Unity, please change your .cfg file", "gnome3etunitygrosboulet", exitonerror = 1)
    '''

    # Parse and exec pre-actions
    '''
    for action_name, action_cmd in config.items("preactions"):
        showexec ("Execute preaction "+action_name.lstrip("action_"), action_cmd)
    '''

    # Parse and install repositories
    '''
    pkg_list_others = {}
    for item_type, item_value in config.items("repos"):
        if (item_type.startswith("ppa_")):
            showexec ("Install repository "+item_type.lstrip("ppa_"), _APT_ADD+" "+item_value)
        elif (item_type.startswith("url_")):
            showexec ("Install repository "+item_type.lstrip("url_"), _APT_ADD+" \\\"deb "+item_value+"\\\"")
        elif (item_type.startswith("key_")):
            showexec ("Install key for the "+item_type.lstrip("key_")+" repository", _APT_KEY+" "+item_value)
        elif (item_type.startswith("pkg_")):
            pkg_list_others[item_type] = item_value
    '''
    # Update repos
    #showexec ("Update repositories", _APT_UPDATE)

    # Upgrade system
    #showexec ("System upgrade (~20 mins, please be patient...)", _APT_UPGRADE)

    # Parse and install packages
    '''
    for pkg_type, pkg_list in config.items("packages"):
        if (pkg_type.startswith("remove_")):
            showexec ("Remove packages "+pkg_type.lstrip("remove_"), _APT_REMOVE+" "+pkg_list)
        else:
            showexec ("Install packages "+pkg_type, _APT_INSTALL+" "+pkg_list)

    # Install packages related to repositories
    #~ print pkg_list_others
    for pkg in pkg_list_others.keys():
        showexec ("Install packages "+pkg, _APT_INSTALL+" "+pkg_list_others[pkg])

    # Download and install dotfiles: vimrc, prompt...
    if (config.has_section("dotfiles")):
        # Create the bashrc.d subfolder
        showexec ("Create the ~/.bashrc.d subfolder", "mkdir -p $HOME/.bashrc.d")
        if (config.has_option("dotfiles", "bashrc")):
            showexec ("Download bash main configuration file", _WGET+" -O $HOME/.bashrc "+config.get("dotfiles", "bashrc"))
        if (config.has_option("dotfiles", "bashrc_prompt")):
            showexec ("Download bash prompt configuration file", _WGET+" -O $HOME/.bashrc.d/bashrc_prompt "+config.get("dotfiles", "bashrc_prompt"))
        if (config.has_option("dotfiles", "bashrc_aliases")):
            showexec ("Download bash aliases configuration file", _WGET+" -O $HOME/.bashrc.d/bashrc_aliases "+config.get("dotfiles", "bashrc_aliases"))
        showexec ("Install the bash configuration file", "chown -R $USERNAME:$USERNAME $HOME/.bashrc*")
        # Vim
        if (config.has_option("dotfiles", "vimrc")):
            showexec ("Donwload the Vim configuration file", _WGET+" -O $HOME/.vimrc "+config.get("dotfiles", "vimrc"))
            showexec ("Install the Vim configuration file", "chown -R $USERNAME:$USERNAME $HOME/.vimrc")

        # Htop
        if (config.has_option("dotfiles", "htoprc")):
            showexec ("Download the Htop configuration file", _WGET+" -O $HOME/.htoprc "+config.get("dotfiles", "htoprc"))
            showexec ("Install the Htop configuration file", "chown -R $USERNAME:$USERNAME $HOME/.htoprc")

        # Pythonrc
        if (config.has_option("dotfiles", "pythonrc")):
            showexec ("Download the Pythonrc configuration file", _WGET+" -O $HOME/.pythonrc "+config.get("dotfiles", "pythonrc"))
            showexec ("Install the Pythonrc configuration file", "chown -R $USERNAME:$USERNAME $HOME/.pythonrc")
    '''

    # End of the script
    print("---")
    print("End of the script.")
    print(" - Configuration file: "+config_file)
    print("")
    print("Please restart your session to complete.")
    print("---")

# Main program
#-----------------------------------------------------------------------------

if __name__ == "__main__":
    init()
    main(sys.argv[1:])
    exit()
