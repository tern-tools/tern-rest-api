#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from setuptools import find_packages, setup

setup(
    name="tern-rest-api",
    version="0.0.1",
    url="https://github.com/tern/tern-rest-api",
    author="VMware Inc",
    author_email="rjudge@vmware.com",
    description="Tern REST API",
    packages=find_packages(),
    install_requires=["flask", "flask-restx", "tern"],
)
