#!/bin/bash
if [[ $# -eq 0 ]] ; then
  JPORT=8888
else
  JPORT=$1
fi
docker run -i -t -v $PWD:erudite/ -w=erudite/ --rm -p ${JPORT}:8888 floriangeigl/erudite

