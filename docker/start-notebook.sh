#!/bin/bash
cd /tmp/erudite/
exec screen -dmS ipython jupyter notebook --ip='*' --port 8888 --no-browser
