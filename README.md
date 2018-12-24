# dev-config
The purpose of this repository is to provide a collection personal preferences and tools that compose my development environment. Feel free to copy and/or use any/all of this!

## Automated setup
I wrote a python script to automate most of the process. The script depends on one non-standard Python 3 package, colorama. You should install this package prior to executing the development configuration program.
### Getting started
1. Install git, ```sudo apt install git```  
2. Clone the repository, ```git clone https://github.com/astpierre/dev-config.git```  
3. Install the requirements ```pip3 install -r requirements.txt```
4. Run the program as root user ```sudo python3 dev_config.py```  
5. Respond to prompt as requested and reboot to see effects.  

## How it works
### Adjust the YAML fields   
To use the Python script for your own usage, you need to alter the YAML file.
I tried to make the YAML fields as simple as possible.  
#### Packages
List any packages under the packages field that you would like to install using the apt package manager.
#### Dot-files
This field has a spot for bashrc and bash_aliases (called from the bashrc). Host your files in a github repository and place your link to raw content in the respective spots.
#### Cosmetics
This field is where a user can place any gnome setting preferences. Some things I change include the sidebar size and location, terminal settings, and clock display format. If there is something you change but are unsure of the terminal command, use ```dconf watch /```.   
#### Vimrc
This field has a clone command to clone the awesome vim starter settings and a command to run the script. This field isn't really meant to be changed.   

## Screengrabs  
Below is a view of the script in action.
![screengrab1](https://github.com/astpierre/dev-config/blob/master/photos/screenshot1.png)

## Next steps
* add support for configuring Atom
* add way to automatically update your YAML based on diffing daily packages and usage

# END-OF-README
