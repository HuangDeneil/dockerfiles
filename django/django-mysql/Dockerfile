FROM ubuntu:22.04

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive TZ="Asia/Taipei"
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


RUN apt-get update -y

# Install basic tools
RUN apt-get install curl vim nano tree -y

# Install python 3.10
RUN apt-get install python3.10 python3.10-dev pkg-config gcc -y

# Install mariadb-client
RUN apt-get -y install mariadb-client libmariadb-dev 

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.10 get-pip.py

# set work directory
RUN mkdir -p /root
RUN mkdir -p /opt/app
COPY ./requirements.txt /root
WORKDIR /root

RUN pip install -r /root/requirements.txt


# RUN chmod +x /opt/app/docker-entrypoint.sh
# ENTRYPOINT [ "/opt/app/docker-entrypoint.sh" ]