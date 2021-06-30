# What image do we start from
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive # preventing dialog error

RUN apt-get update
RUN apt-get install -y build-essential curl apt-utils wget unzip tcpdump
RUN apt install -y net-tools iputils-ping
RUN apt-get install -y nano
RUN apt-get install -y vim

# the next lines will take care of tcpdump when --privileged is accure
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump && bash

RUN apt update
RUN apt-get install --fix-broken -y python3-pip
RUN apt-get install -y python3

RUN apt install -y git

# Emane dependencies 
 
RUN apt-get install -y gcc g++ autoconf automake libtool libxml2-dev libprotobuf-dev \
    libpcap-dev libpcre3-dev uuid-dev debhelper pkg-config protobuf-compiler git dh-python \
    python3-protobuf python3-setuptools python3-lxml

# Emane-Tutorial dependencies & installation
RUN apt-get install -y bridge-utils mgen fping gpsd gpsd-clients \
    iperf multitail openssh-server python-tk python-pmw python3-stdeb

RUN git clone https://github.com/adjacentlink/emane.git

RUN cd emane && \
    ./autogen.sh && \
    ./configure && \
    make -j8 deb

RUN cd emane/.debbuild && \
    dpkg -i *.deb

RUN apt-get install -f

# Opentestpoint additional dependencies & installation

RUN apt-get install -y python3-zmq python3-dev \
    libzmq5 libzmq3-dev sqlite3 libsqlite3-dev \
    python3-psutil python3-pyroute2

RUN git clone https://github.com/adjacentlink/opentestpoint.git

RUN cd opentestpoint && \
    ./autogen.sh && \
    ./configure && \
    make -j8 deb

RUN cd opentestpoint/.debbuild && \
    dpkg -i *.deb

RUN apt-get install -f

# Opentestpoint-probe-emane

RUN git clone https://github.com/adjacentlink/opentestpoint-probe-emane.git

RUN cd opentestpoint-probe-emane && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make deb

RUN cd opentestpoint-probe-emane/.debbuild && \
    dpkg -i *.deb

RUN mkdir opentestpoint-probe-example
ADD opentestpoint-probe-example/ /opentestpoint-probe-example

RUN chmod 777 -R opentestpoint-probe-example && \
    cd opentestpoint-probe-example && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make deb

RUN cd opentestpoint-probe-example/.debbuild && \
    dpkg-deb -xv *.deb /usr/lib/python3/dist-packages/otestpoint/

RUN apt-get install -f

RUN mkdir /emane-tutorial

#ENTRYPOINT "/bin/sh /emane-tutorial/1/start-demo.sh"
