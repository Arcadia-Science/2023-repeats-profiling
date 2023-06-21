# base image
FROM ubuntu:focal

# metadata labels
LABEL base.image="ubuntu:focal"
LABEL dockerfile.version="1"
LABEL software="uTR"
LABEL description="Profiling repeat expansions in FASTA sequences"
LABEL website="https://github.com/morisUtokyo/uTR/tree/main"
LABEL license="https://github.com/morisUtokyo/uTR/blob/main/LICENSE.txt"

# install dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    build-essential \
    autoconf \
    gcc \
    g++ && \
    apt-get autoclean

# download and install uTR executable
WORKDIR /opt
RUN git clone https://github.com/morisUtokyo/uTR.git && \
    cd uTR && \
    make && \
    chmod u+x ./uTR && \
    ln -s /opt/uTR/uTR /usr/local/bin

# set final working directory
WORKDIR /data
