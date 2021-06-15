FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y net-tools tcpdump

# the next lines will take care of tcpdump when --privileged is accure
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump && bash