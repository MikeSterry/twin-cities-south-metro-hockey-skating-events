#!/bin/bash

# This will stop any running apps and run docker compose - build and up/run
# You do need a docker env file; which will contain shared parameters for all of your docker env
# This script, as well as the app requires a "DOCKER_CONFIG_PARENT_DIR" parameter in that file
# NOTE: The docker-compose requires both that env file as well as that variable to run as well
# 
# e.x. ./run.sh /opt/docker/global.env
# 
# NOTE: I do set a default for the env file, but not the config parent dir. Users can change the env to whatever they want, but the compose file does require the parent config var; 
#           which we can't override here

DOCKER_ENV_FILE=$2

set a
source ${DOCKER_ENV_FILE:=/opt/docker/global.env}

docker compose -p hockey-app -f $DOCKER_CONFIG_PARENT_DIR/twin-cities-south-metro-hockey-skating-events/docker-compose.yml --env-file ${DOCKER_ENV_FILE:=/opt/docker/global.env} build --no-cache

docker compose -p hockey-app down

docker compose -p hockey-app -f $DOCKER_CONFIG_PARENT_DIR/twin-cities-south-metro-hockey-skating-events/docker-compose.yml --env-file ${DOCKER_ENV_FILE:=/opt/docker/global.env} up -d
