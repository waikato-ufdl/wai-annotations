ARG DOCKER_REGISTRY=public.aml-repo.cms.waikato.ac.nz:443/
FROM ${DOCKER_REGISTRY}ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       git-core \
       wget \
       python3 \
       python3-dev \
       python3-venv \
       python3-pip \
       build-essential \
       libglib2.0-0 \
       libsm6 \
       libxrender-dev \
       libxext6 \
       libgl1-mesa-glx \
       libpq-dev \
       libsndfile-dev \
       ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install "numpy<1.23.0" pipdeptree
RUN pip3 --no-cache-dir install "wai.annotations[tf]==0.8.0"
RUN mkdir -p /.config/wai-annotations

COPY bash.bashrc /etc/bash.bashrc
ENV NUMBA_CACHE_DIR /tmp

WORKDIR /workspace

