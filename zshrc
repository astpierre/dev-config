# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
  export ZSH="/home/asaintp/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="refined"


# Which plugins would you like to load?
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
export SSH_KEY_PATH="~/.ssh/rsa_id"

# Example aliases
alias zshconfig="atom ~/.zshrc"
alias l="ls"
alias c="clear"
alias update="sudo apt update && sudo apt upgrade -y"

plugins=(git github zsh-syntax-highlighting sudo web-search zsh-autosuggestions)

source ./.zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
export JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
autoload -Uz promptinit; promptinit
#prompt pure
# alias ohmyzsh="mate ~/.oh-my-zsh"

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/home/asaintp/.sdkman"
[[ -s "/home/asaintp/.sdkman/bin/sdkman-init.sh" ]] && source "/home/asaintp/.sdkman/bin/sdkman-init.sh"
