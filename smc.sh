#!/bin/sh
#
# Wrapper script for Secret Mayro Chronicles to ensure it saves various
# files in a sensible location.
#
smcbin='/usr/bin/smc.bin';

#Check binary exists and is executable
if [ ! -x $smcbin ]; then
    echo "error: $smcbin missing or not executable" 1>&2
    exit 1
fi

#Check home exists and is a directory
if [ ! -d $HOME ] ; then
    echo "error: $HOME is missing or not a directory" 1>&2
    exit 2
fi

#Check if ~/.smc/savegames exists and is directory, if not, make it
if [ ! -d "$HOME/.smc/savegames" ] ; then
    mkdir -p "$HOME/.smc/savegames"
fi

# Change to ~/.smc, launch smc, passing in any arguments
cd "$HOME/.smc"
exec $smcbin "$@"
