FROM ubuntu:16.04

ADD sources.list /etc/apt/sources.list
#RUN echo "nameserver=8.8.8.8" >> /etc/resolv.conf
#    && mkdir /var/lib/apt/lists/partial
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nginx python3-pip python3 python3-dev python3-setuptools supervisor sqlite3 vim &&\
    pip3 install -U pip setuptools &&\
    apt-get clean all
RUN rm -rf /var/lib/apt/lists/*
COPY pip.conf /root/.pip/pip.conf
RUN pip3 install uwsgi

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt
ADD . /usr/src/app

# Symlink to this file from /etc/nginx/sites-enabled so nginx can see it
RUN ln -s /usr/src/app/mysite_nginx.conf /etc/nginx/sites-enabled/

RUN mkdir -p /var/log/supervisor /var/log/uwsgi
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8000
CMD ["/usr/bin/supervisord","-n"]