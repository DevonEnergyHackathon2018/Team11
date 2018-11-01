#!/bin/bash

set -ex
if [ "$1" = 'hotdog' ]; then
    while true; do
        gosu drillbit python3 /opt/drillbit/circle_service.py 
    done
else
    exec "$@"
fi
