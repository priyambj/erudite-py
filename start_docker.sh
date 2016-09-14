#!/bin/bash
docker run -i -t -v $PWD:erudite/ -w=erudite/ --rm -p 8888:8888 floriangeigl/erudite
