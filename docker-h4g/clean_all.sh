#!/bin/bash

docker rm -f `docker ps -a -q`
docker image prune -f
docker network prune -f
docker volume prune -f

docker rm -f `docker ps -a -q`
docker network create -d bridge helix-core-network
docker-compose build
docker-compose up -d

