#!/bin/sh

set -e

if [ -z "$1" ]; then
    echo "Usage: <imagefile> <arch>"
    echo "For x86_64, amd64 is also supported."
    exit 1
fi

if [ -n "$2" ]; then
    if [ "$2" = 'amd64' ]; then
        ARCH='x86_64'
    else
        ARCH="$2"
    fi
else
    echo "Specify the architecture of the image"
    echo "Usage: <imagefile> <arch>"
    echo "For x86_64, amd64 is also supported."
    exit 1
fi

qemu-system-${ARCH} -m 1024 -enable-kvm -drive format=raw,file=./$1
