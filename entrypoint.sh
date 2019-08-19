#!/bin/sh

set -e

VERSION=`cat /VERSION`

if [ $# -eq 0 ]; then
  python app.py
elif [ $1 == 'bash' ]; then
  sh
elif [ $1 == 'shell' ]; then
  sh
elif [ $1 == 'sh' ]; then
  sh
elif [ $1 == '--version' ]; then
  echo "Version is: $VERSION"
fi
