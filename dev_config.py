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
import colorama
import time
from colorama import Fore, Back, Style

# Global variables
#-----------------------------------------------------------------------------
VERSION = "1.2.1"
OPTIONS_FILE = "configs.yml"

# System commands
#-----------------------------------------------------------------------------
_APT_ADD = "add-apt-repository -y"
_APT_INSTALL = "DEBIAN_FRONTEND=noninteractive apt-get -y -f install"
_APT_REMOVE = "DEBIAN_FRONTEND=noninteractive apt-get -y -f remove"
_APT_UPDATE = "DEBIAN_FRONTEND=noninteractive apt-get -y update"
_APT_UPGRADE = "DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"
_WGET = "wget"

FRED = Fore.RED
FGREEN = Fore.GREEN
FBLUE = Fore.BLUE
FWHITE = Fore.WHITE
FCYAN = Fore.CYAN
FMAGENTA = Fore.MAGENTA
FYELLOW = Fore.YELLOW
FBLACK = Fore.BLACK
BRED = Back.RED
BGREEN = Back.GREEN
BLUE = Back.BLUE
BWHITE = Back.WHITE
BCYAN = Back.CYAN
BMAGENTA = Back.MAGENTA
BYELLOW = Back.YELLOW
SDIM = Style.DIM
SNORMAL = Style.NORMAL
SBRIGHT = Style.BRIGHT
BOLD = '\x1b[1;37m'
QUESTION = SBRIGHT+FBLUE+Back.RESET
OLDQ = SBRIGHT+FMAGENTA+Back.RESET

WARNING = SDIM+FYELLOW+Back.RESET
CHOICES = SNORMAL+FCYAN+Back.RESET
ERROR = SBRIGHT+FRED+BYELLOW
SUCCESS = SBRIGHT+FGREEN+Back.RESET
RESET = Style.RESET_ALL+Fore.RESET+Back.RESET

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
        status = "[ IN PROGRRESS ]"
    statuscolor = FYELLOW
    sys.stdout.write(RESET+SDIM+"%s"%waitmessage+statuscolor+SBRIGHT+"%s"%status.rjust(80-len(waitmessage))+RESET)
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
        status = "[ DONE ]"
        statuscolor = SUCCESS
    else:
        if exitonerror == 0:
            status = "[ WARNING ]"
            statuscolor = WARNING
        else:
            status = "[ ERROR ]"
            statuscolor = ERROR

    sys.stdout.write(RESET+SDIM+"\r%s"%description+statuscolor+SBRIGHT+"%s\n"%status.rjust(80-len(description))+RESET)

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

def getChar():
    userInput = ''
    while len(userInput) != 1:
        userInput = input("=> ")
    return userInput.lower()

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

def doPackages(configs):
    # Install all requested packages
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

def doDotfiles(configs):
    # Download the dotfiles from specified locations and use them
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

def doVimstuff(configs):
    # Clone the vimrc settings into home dir
    instr = configs["vimrc"]["clone"]
    showexec("Cloning the vim settings repo from github...", instr+" $HOME")
    instr = configs["vimrc"]["runit"]
def doCosmostuff(configs):
    # Parse and exec pre-actions
    for cosmo in configs["cosmetics"]:
        # TESTING WITH virtualenv and htop
        showexec("Configuring "+str(cosmo), configs["cosmetics"][cosmo])

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
    colorama.init()

    # Check if user wants to use help or see version
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            syntax()
            exit()
        elif opt in ('-v', "--version"):
            version()
            exit()

    note="Welcome to dev-config! v."
    sys.stdout.write(BWHITE+SBRIGHT+FBLACK+note+VERSION+" "*(80-len(note)-len(VERSION))+"\n")

    # Are you root?
    leftmessage = "Does user have root privs?"
    if(not isroot()):
        showexec ("Script should be run as root", " ", exitonerror = 1)
    rightmessage = "[ PASSED ]"
    sys.stdout.write(OLDQ+"%s"%leftmessage+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)

    # Check the Ubuntu version (TODO: get more user info)
    UBUNTU_VERSION = os.uname()

    # Read the configuration file and lets see what we will do with it
    with open(config_file, 'r') as fyaml:
        configs = yaml.load(fyaml)
    note="Now customizing your experience w. your configurations from your YAML file."
    sys.stdout.write(BWHITE+SBRIGHT+FBLACK+note+" "*(80-len(note))+"\n")

    if "dotfiles" in configs:
        # Ask if user wants to do this
        leftmessage = "Update dotfiles?"
        rightmessage = "[ (y)es / (n)o ]"
        sys.stdout.write(QUESTION+"%s"%leftmessage+RESET+CHOICES+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        sys.stdout.flush()
        if(getChar() == "y"):
            doDotfiles(configs)
            leftmessage = "Dotfiles successfully updated."
            rightmessage = "[ DONE ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        else:
            leftmessage = "Dotfiles left unchanged."
            rightmessage = "[ SKIPPED ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+WARNING+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)

    if "packages" in configs:
        # Ask if user wants to do this
        leftmessage = "Install packages on list in config.yml?"
        rightmessage = "[ (y)es / (n)o ]"
        sys.stdout.write(QUESTION+"%s"%leftmessage+RESET+CHOICES+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        sys.stdout.flush()
        if(getChar() == "y"):
            doPackages(configs)
            leftmessage = "Packages successfully installed."
            rightmessage = "[ DONE ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        else:
            leftmessage = "Packages left unchanged."
            rightmessage = "[ SKIPPED ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+WARNING+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)

    if "vimrc" in configs:
        # Ask if user wants to do this
        leftmessage = "Would you like to update your vim settings?"
        rightmessage = "[ (y)es / (n)o ]"
        sys.stdout.write(QUESTION+"%s"%leftmessage+RESET+CHOICES+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        sys.stdout.flush()
        if(getChar() == "y"):
            #doVimstuff(configs)
            leftmessage = "Vim configurations successfully changed."
            rightmessage = "[ DONE ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        else:
            leftmessage = "Vim configurations left unchanged."
            rightmessage = "[ SKIPPED ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+WARNING+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)

    if "cosmetics" in configs:
        # Ask if user wants to do this
        leftmessage = "Would you like to configure your desktop appearance?"
        rightmessage = "[ (y)es / (n)o ]"
        sys.stdout.write(QUESTION+"%s"%leftmessage+RESET+CHOICES+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        sys.stdout.flush()
        if(getChar() == "y"):
            doCosmostuff(configs)
            leftmessage = "Desktop appearance successfully configured."
            rightmessage = "[ DONE ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        else:
            leftmessage = "Desktop appearance left unchanged."
            rightmessage = "[ SKIPPED ]"
            sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+WARNING+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)

    # End of the script
    note="End of configuration script. Used configuration file: "
    sys.stdout.write(BWHITE+SBRIGHT+FBLACK+note+config_file+" "*(80-len(note)-len(config_file))+"\n")

    leftmessage = "Would you like to reboot now?"
    rightmessage = "[ (y)es / (n)o ]"
    sys.stdout.write(QUESTION+"%s"%leftmessage+RESET+CHOICES+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
    if(getChar() == "y"):
        leftmessage = "Rebooting in 3 seconds!"
        rightmessage = "[ REBOOTING ]"
        sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+SUCCESS+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
        time.sleep(3)
        os.system("reboot")
    else:
        leftmessage = "Ok, reboot later."
        rightmessage = "[ REBOOT POSTPONED ]"
        sys.stdout.write(OLDQ+"%s"%leftmessage+RESET+WARNING+"%s"%rightmessage.rjust(80-len(leftmessage))+RESET)
    sys.stdout.write(RESET+BWHITE+" "*80+RESET)

# Main program
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    init()
    main(sys.argv[1:])
    exit()
