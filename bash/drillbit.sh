#!/bin/bash

set -ex
if [ "$1" = 'hotdog' ]; then
    while true; do
        gosu ldapserv python3 /opt/drillbit/circle_service.py 
    done
else
    exec "$@"
fi
