##### Build Image
FROM python:3.7-slim-bullseye AS builder
LABEL maintainer Peiyu
ARG PROJECT_NAME=map_world

RUN echo "deb http://opensource.nchc.org.tw/debian/ bullseye main" > /etc/apt/sources.list \
    && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-updates main" >> /etc/apt/sources.list \
    && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends\
    build-essential \
    libldap2-dev \
    #=2.4.47+dfsg-3+deb10u4 \
    libsasl2-dev \
    libpq-dev \
    libpq5
RUN apt-get install -y wget \
    unzip \
    libaio-dev \
    wget \
    libpq-dev \
    tzdata \
    cron \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2-binary==2.8.6

RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata


COPY ./${PROJECT_NAME} /${PROJECT_NAME}
COPY requirements.txt /${PROJECT_NAME}/requirements.txt

WORKDIR /${PROJECT_NAME}

RUN pip install --upgrade pip
RUN pip install -r /${PROJECT_NAME}/requirements.txt

### Copy entrypoint.sh file and link to root
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN ln -s /usr/local/bin/docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]

### COPY the uwsgi configuration file
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

### Port to use with TCP proxy
EXPOSE 55555

### Start uWSGI on container startup
CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
