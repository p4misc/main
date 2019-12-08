FROM centos:centos7

LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN yum -y install epel-release \
    && yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm \
    && yum -y update \
    && yum-config-manager --enable remi-php72 \
    && yum -y install httpd mod_ssl php php-ldap php-mbstring php-memcache php-mcrypt php-pdo php-pear php-xml wget \
    && rm -rf /var/cache/yum/* \
    && yum -y clean all

RUN ssp_version=1.18.2; \
    ssp_hash=79157c5d420789fb3bb3f4c346a3b9c8737aefbcbb695bc4539b5523969ec977; \
    wget https://github.com/simplesamlphp/simplesamlphp/releases/download/v$ssp_version/simplesamlphp-$ssp_version.tar.gz \
    && echo "$ssp_hash  simplesamlphp-$ssp_version.tar.gz" | sha256sum -c - \
	&& cd /var \
	&& tar xzf /simplesamlphp-$ssp_version.tar.gz \
    && mv simplesamlphp-$ssp_version simplesamlphp \
    && rm /simplesamlphp-$ssp_version.tar.gz

RUN echo $'\nSetEnv SIMPLESAMLPHP_CONFIG_DIR /var/simplesamlphp/config\nAlias /simplesaml /var/simplesamlphp/www\n \
<Directory /var/simplesamlphp/www>\n \
    Require all granted\n \
</Directory>\n' \
       >> /etc/httpd/conf/httpd.conf

EXPOSE 80 443

CMD ["httpd", "-DFOREGROUND"]
