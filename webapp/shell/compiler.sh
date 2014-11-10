#!/bin/bash

PROJECT=$1
VERSION=$2
PROJECT_PATH=$3

if [ "$PROJECT" = "" ]; then
    echo "Project is empty"
    exit
fi

if [ "$VERSION" = "" ]; then
    echo "Version is empty"
    exit
fi

if [ "$PROJECT_PATH" = "" ]; then
    cd /opt/engine.lintas.me/
else
    cd "$PROJECT_PATH"
fi

/usr/bin/scrapyd-deploy --version "$VERSION"

exit

