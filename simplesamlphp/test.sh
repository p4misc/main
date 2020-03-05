#!/bin/bash

docker rm -f `docker ps -a -q`
docker-compose up -d
#docker exec ldap-host slapcat
#docker exec ldap-host ldapsearch -x -H ldap://localhost -b dc=p4misc,dc=com -D "cn=admin,dc=p4misc,dc=com" -w p4misc123456
#docker exec ldap-host ldapsearch -x -D "cn=admin,dc=p4misc,dc=com" -w "p4misc123456"
docker exec ldap-host ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config dn
#docker cp base.ldif ldap-host:.
#docker exec ldap-host ldapadd -H ldapi://localhost -f base.ldif
