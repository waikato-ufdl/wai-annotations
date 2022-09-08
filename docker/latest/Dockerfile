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
RUN pip3 --no-cache-dir install \
      git+https://github.com/waikato-ufdl/wai-annotations-core.git \
      git+https://github.com/waikato-ufdl/wai-annotations-adams.git \
      git+https://github.com/waikato-ufdl/wai-annotations-audio.git \
      git+https://github.com/waikato-ufdl/wai-annotations-bluechannel.git \
      git+https://github.com/waikato-ufdl/wai-annotations-coco.git \
      git+https://github.com/waikato-ufdl/wai-annotations-commonvoice.git \
      git+https://github.com/waikato-ufdl/wai-annotations-coqui.git \
      git+https://github.com/waikato-ufdl/wai-annotations-festvox.git \
      git+https://github.com/waikato-ufdl/wai-annotations-generic.git \
      git+https://github.com/waikato-ufdl/wai-annotations-grayscale.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgaug.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgstats.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgvis.git \
      git+https://github.com/waikato-ufdl/wai-annotations-indexedpng.git \
      git+https://github.com/waikato-ufdl/wai-annotations-layersegments.git \
      git+https://github.com/waikato-ufdl/wai-annotations-opex.git \
      git+https://github.com/waikato-ufdl/wai-annotations-redis-predictions.git \
      git+https://github.com/waikato-ufdl/wai-annotations-roi.git \
      git+https://github.com/waikato-ufdl/wai-annotations-subdir.git \
      git+https://github.com/waikato-ufdl/wai-annotations-tf.git \
      git+https://github.com/waikato-ufdl/wai-annotations-vgg.git \
      git+https://github.com/waikato-ufdl/wai-annotations-video.git \
      git+https://github.com/waikato-ufdl/wai-annotations-voc.git \
      git+https://github.com/waikato-ufdl/wai-annotations-yolo.git
RUN mkdir -p /.config/wai-annotations

COPY bash.bashrc /etc/bash.bashrc
ENV NUMBA_CACHE_DIR /tmp

WORKDIR /workspace

