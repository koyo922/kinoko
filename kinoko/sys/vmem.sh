#!/bin/bash
set -e

# Author: qianweishuo
# Date: 2019/06/14
# Brief:
#   script for adding virtual memory
# Globals:
#   None
# Arguments:
#   1:size in GigaBytes. default: 64 GB
#   2:swap file path. default: ${HOME}/swap
# Returns:
#   succ:0
#   fail:other

function usage(){
    echo 'e.g.'
    echo 'vmem.sh -a on -s 64 -f /home/work/swap'
}

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
    ARGS=`getopt -o a:s:f: -l action:,size:,file -- "$@"`
    eval set -- "${ARGS}" # without the `eval` extra single quotes appear around each argument value
    while true
    do
        case "$1" in
        -a|--action)
            ACTION="$2"; shift
            ;;
        -s|--size)
            SIZE=${2:-64}; shift
            ;;
        -f|--file)
            SWAP_FILE=${2:-/home/work/swap}; shift
            ;;
        -h|--help)
            usage
            ;;
        --)
            shift; break
            ;;
        esac
        shift
    done

    #    echo $ACTION $SIZE $SWAP_FILE
    #    echo 'remaining args:' $@
    if [[ ${ACTION} = 'on' ]]; then
        on
    else
        off
    fi
}

main "$@"