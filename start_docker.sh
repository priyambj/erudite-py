#!/bin/bash
if [ $# -eq 0 ]; then
  jport=8888
else
  jport=$1
docker run -i -t -v $PWD:erudite/ -w=erudite/ --rm -p $jport:8888 floriangeigl/erudite
