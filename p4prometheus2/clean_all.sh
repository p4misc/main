#!/bin/bash

docker rm -f `docker ps -a -q`
docker image prune -f
docker network prune -f
docker volume prune -f
