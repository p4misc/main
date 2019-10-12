#!/bin/sh

docker build -t p4dmaster ./p4dmaster
docker run --name p4dmaster -d -p 1666:1666 -it p4dmaster
