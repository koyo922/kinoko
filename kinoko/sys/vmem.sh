#!/usr/bin/env bash
set -e

# Author: qianweishuo
# Date: 2019/06/14
# Brief:
#   script for adding/removing virtual memory
# Globals:
#   None
# Arguments:
#   action, size, swap_file; see definition below
# Returns:
#   succ:0
#   fail:other

if [[ $(uname -s) != 'Linux' ]]; then
    colormsg 'only support Linux now' FAIL
    exit 1
fi

# put `.pyenv/.../bin` before `.pyenv/shims`
export PATH=$(python -c 'from distutils.sysconfig import EXEC_PREFIX as p; print(p + "/bin")'):$PATH
# `pip install` has already written something alike into `~/.bashrc`, but may not effect instantly
source $(which optparse.bash)

# optparse usage: https://github.com/nk412/optparse
optparse.define short=a long=action desc="action for turning on/off the vmem" variable=ACTION
optparse.define short=s long=size desc="size of the swap file in GB" variable=SIZE default=64
optparse.define short=f long=path desc="absolute path of the swap file" variable=SWAP_FILE default=$HOME/swap
source $(optparse.build)

#######################################
# Brief:
#   turn on swap file
# Globals:
#   SIZE, SWAP_FILE
# Arguments:
#   None
# Returns:
#   None
#######################################
function on(){
    # create the swap file using `dd` command
    dd if=/dev/zero of=${SWAP_FILE} bs=$(echo '1024*1024*1024' | bc) count=${SIZE}
    # make it as swap format
    mkswap ${SWAP_FILE}

    # peek the memory status(before)
    colormsg '`swapon -s` and `free -g` before:'
    swapon -s && free -g

    # use `swapon` to mount the swap_file
    if sudo -v; then
        sudo /sbin/swapon ${SWAP_FILE} # may need sudo
        # peek the memory status(after)
        colormsg '`swapon -s` and `free -g` after:'
        swapon -s && free -g
    else
        colormsg 'please execute the following command with ROOT' FAIL
        colormsg "/sbin/swapon ${SWAP_FILE} && free -g" FAIL
    fi
}


#######################################
# Brief:
#   turn off swap file
# Globals:
#   SWAP_FILE
# Arguments:
#   None
# Returns:
#   None
#######################################
function off(){
    if sudo -v; then
        # unmount the swap file
        sudo /sbin/swapoff ${SWAP_FILE}
        # delete it
        rm -rf ${SWAP_FILE}
    else
        colormsg 'please execute the following command with ROOT' FAIL
        colormsg "/sbin/swapoff ${SWAP_FILE} && rm -rf ${SWAP_FILE}" FAIL
    fi
}

function main(){
    if [[ ${ACTION} = 'on' ]]; then
        on
    else
        off
    fi
}

main "$@"