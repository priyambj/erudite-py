#!/bin/bash

# Handle special flags if we're root
if [ $UID == 0 ] ; then
    # Change UID of DUSER to DUID if it does not match
    if [ "$DUID" != $(id -u $DUSER) ] ; then
        usermod -u $DUID $DUSER
        chown -R $DUID $CONDA_DIR .
    fi

    # Enable sudo if requested
    if [ ! -z "$GRANT_SUDO" ]; then
        echo "$DUSER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook
    fi

    # Start the notebook server
    exec su $DUSER -c "env PATH=$PATH jupyter notebook --port 8882 --no-browser"
else
    # Otherwise just exec the notebook
    exec jupyter notebook --port 8882 --no-browser
fi
