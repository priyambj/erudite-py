#!/bin/bash
chmod g+s ./
setfacl -d -m g::rwx ./
chmod -t ./
