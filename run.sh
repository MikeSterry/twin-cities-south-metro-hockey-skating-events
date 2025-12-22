#!/bin/bash

docker compose -p hockey-app down
docker compose -p hockey-app -f /opt/docker/hockey-app/docker-compose.yml --env-file /opt/docker/global.env build --no-cache
docker compose -p hockey-app -f /opt/docker/hockey-app/docker-compose.yml --env-file /opt/docker/global.env up -d