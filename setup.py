#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from setuptools import find_packages, setup

setup(
    name="tern-rest-api",
    version="1.0.0",
    url="https://github.com/tern/tern-rest-api",
    author="VMware Inc",
    author_email="",
    description="Tern REST API",
    packages=find_packages(),
    install_requires=["flask", "flask-restx", "tern"],
)
