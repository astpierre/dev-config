# dev-config
development environment configurations for Ubuntu 18.10 (or similar)  
The purpose of this repository is to provide a user a collection of steps to configure their development environment. Feel free to copy and/or use any/all of this!  

# Update OS and existing SW 
```sudo apt update && sudo apt upgrade -y```  
# Aliases & prompts  
I have a few aliases I have adopted from various sources that I cannot recall. They save time and keep  

# [git](https://git-scm.com/)  
Install git and configure yourself as the global user.  
```
sudo apt install git  
git config --global user.name "Andrew St. Pierre"  
git config --global user.email "astpier@purdue.edu"  
```  

# Process management  
## [htop](https://hisham.hm/htop/)  
I enjoy using ```htop``` instead of ```top``` to view system metrics and running processes. My Dad showed me this one, thanks Dad.  
```  
sudo apt install htop  
```  

# [Vim](https://www.vim.org/)  
Vim is my IDE of choice. Unfortunately it comes with a pretty crummy default set of settings. My conclusion is that you can sit and stare at ```.vimrc```'s all day and configure it to your liking, or you can just use this pretty great [existing configuration](https://github.com/amix/vimrc) and follow the following steps...  
```  
git clone --depth=1 https://github.com/amix/vimrc.git ~/.vim_runtime  
sh ~/.vim_runtime/install_awesome_vimrc.sh  
```  

# [Python](https://www.python.org/)  
Python 2 and 3 are likely already installed. However, there are a couple things any software developer needs to have in order to use Python to its fullest...  

## [curl](https://curl.haxx.se/)  
Not only is ```curl``` needed to install pip, it is a commonly used tool to transfer data using URLs.  
```
sudo apt install curl  
```

## [pip](https://pypi.org/project/pip/)  
```pip``` is a Python package manager.  
```
sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
sudo python get-pip.py
sudo pip install -U pip  
```  

## [virtualenv](https://virtualenv.pypa.io/en/latest/)  
Use this tool to create isolated Python environments. Why? Well, if you are using version ```1.9``` of ```foo``` in one project, but in another project you decide to use the latest version ```2.0``` of ```foo``` which depends on ```bar```, you may have a dependency issue.  
```
pip install virtualenv
```  

# [Node.js](https://nodejs.org/en/)  
```
sudo apt install nodejs -y
sudo apt install npm -y
```

# [Ruby](https://www.ruby-lang.org/en/documentation/)
```
sudo apt-get install ruby-full -y
```

# [Atom](https://atom.io/download/deb)  
Install Atom and install the embedded [live-server-package](https://atom.io/packages/atom-live-server) to aid in small-scale web-development.  

# END-OF-README
