ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/
FROM ${DOCKER_REGISTRY}ubuntu:20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       git-core \
       wget \
       libglib2.0-0 \
       libsm6 \
       libxrender-dev \
       libxext6 \
       python3 \
       python3-dev \
       python3-venv \
       build-essential \
       libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install "numpy>=1.16"
RUN pip3 --no-cache-dir install "wai.annotations==0.7.5"
RUN mkdir -p /.config/wai-annotations

COPY bash.bashrc /etc/bash.bashrc

WORKDIR /workspace

