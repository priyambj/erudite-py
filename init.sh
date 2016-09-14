#!/bin/bash
chmod g+s ./
chmod -t ./
if [[ $(uname -s) == Linux* ]] ; then
  echo "running on Linux"
  setfacl -d -m g::rwx ./
else
  echo "running on Mac"
fi
