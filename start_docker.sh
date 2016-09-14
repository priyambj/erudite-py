#!/bin/bash
docker run -i -t -v $PWD:/home/erudite/erudite -w=/home/erudite/erudite --rm -p 8888:8888 floriangeigl/erudite
