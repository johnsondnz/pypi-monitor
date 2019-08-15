#!/bin/sh

set -e

VERSION=`cat /VERSION`

if [ $1 == '--version' ]; then
  echo "Current version: $VERSION"
elif [ $1 == 'bash' ]; then
  sh
elif [ $1 == 'shell' ]; then
  sh
elif [ $1 == 'sh' ]; then
  sh
else
  python app.py
fi
