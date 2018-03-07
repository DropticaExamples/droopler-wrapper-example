FROM droptica/php-developer:7.0-v1.5

WORKDIR /root

ENV WK_MAJOR_VERSION 0.12
ENV WK_MINOR_VERSION 4
ENV GS_VERSION 9.22

RUN apt-get update && apt-get install xz-utils libcurl4-gnutls-dev libxml2-dev -y \
    && pecl install solr-2.4.0 -y \
    && docker-php-ext-enable solr \
    && curl -SLO https://downloads.wkhtmltopdf.org/${WK_MAJOR_VERSION}/${WK_MAJOR_VERSION}.${WK_MINOR_VERSION}/wkhtmltox-${WK_MAJOR_VERSION}.${WK_MINOR_VERSION}_linux-generic-amd64.tar.xz \
    && tar -xJf wkhtmltox-${WK_MAJOR_VERSION}.${WK_MINOR_VERSION}_linux-generic-amd64.tar.xz \
    && mv wkhtmltox/bin/* /bin/ \
    && mv wkhtmltox/lib/* /lib/ \
    && rm -rf wkhtmltox*

RUN curl -SLO https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs922/ghostscript-${GS_VERSION}.tar.gz \
  && tar zxpf ghostscript-${GS_VERSION}.tar.gz -C /tmp \
  && cd /tmp/ghostscript-${GS_VERSION} \
  && ./configure \
  && make \
  && make install

RUN git clone https://github.com/droptica/docker-console.git && cd docker-console && git checkout tags/v0.1.0 && python setup.py install

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "memory_limit = 1024M" > /usr/local/etc/php/conf.d/memory_limit.ini

WORKDIR /app
