# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

FROM python:3.9-slim-buster as base

RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list.d/bullseye.list \
    && echo "Package: *\nPin: release n=bullseye\nPin-Priority: 50" > /etc/apt/preferences.d/bullseye \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    attr \
    findutils \
    fuse-overlayfs/bullseye \
    fuse3/bullseye \
    git \
    jq \
    skopeo \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache -r ./requirements.txt

RUN mkdir /opt/tern-rest-api

ADD . /opt/tern-rest-api
WORKDIR /opt/tern-rest-api

ENV TERN_API_CACHE_DIR=/var/opt/tern-rest-api/cache
ENV TERN_DEFAULT_REGISTRY="registry.hub.docker.com"

ENTRYPOINT [ "bash", "docker_start.sh" ]