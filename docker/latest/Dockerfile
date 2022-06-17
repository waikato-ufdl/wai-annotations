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

WORKDIR /opt/wai-annotations

RUN git clone https://github.com/waikato-ufdl/wai-annotations-core.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-adams.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-bluechannel.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-coco.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-commonvoice.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-festvox.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-generic.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-grayscale.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-imgaug.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-imgstats.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-imgvis.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-indexedpng.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-layersegments.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-opex.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-redis-predictions.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-roi.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-subdir.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-tf.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-vgg.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-video.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-voc.git && \
    git clone https://github.com/waikato-ufdl/wai-annotations-yolo.git
RUN pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-core && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-adams && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-bluechannel && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-coco && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-commonvoice && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-festvox && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-generic && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-grayscale && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-imgaug && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-imgstats && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-imgvis && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-indexedpng && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-layersegments && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-opex && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-redis-predictions && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-subdir && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-tf && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-vgg && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-video && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-voc && \
    pip3 --no-cache-dir install /opt/wai-annotations/wai-annotations-yolo
RUN mkdir -p /.config/wai-annotations

COPY bash.bashrc /etc/bash.bashrc

WORKDIR /workspace

