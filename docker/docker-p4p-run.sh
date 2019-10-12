#!/bin/sh

TARGET=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' p4dmaster`:1666
PORT=1777
docker build -t p4p --build-arg TARGET=$TARGET --build-arg PORT=$PORT ./p4p
docker run --name p4p -d -p $PORT:$PORT -it p4p
