#!/usr/bin/env bash

CMD="$@"

if [ "$CMD" == "" ]; then
    echo "Please specify a comand to run."
elif [ -f /.dockerenv ]; then
    $CMD
else
    docker-compose run --rm web $CMD
fi