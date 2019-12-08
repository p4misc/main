docker rm -f `docker ps -a -q`
docker image prune -f
docker build -t simplesamlphp .
docker run --name simplesamlphp -p 80:80 -p 443:443 -itd simplesamlphp 
docker exec -it simplesamlphp /bin/bash
