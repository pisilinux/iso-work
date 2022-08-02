#!/bin/sh

source ./make.sh

if [ -f .firstRun ];then
  firstRun=$(cat .firstRun)
else
  firstRun=0
fi

if [ $firstRun -eq 0 ]; then
  make
  echo "1" > .firstRun
fi

sudo ./pisiman.py --style=breeze
