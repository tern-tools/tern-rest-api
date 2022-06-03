#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import os

from flask import Flask
from flask_executor import Executor

tern_app = Flask(__name__)
tern_app.config["TERN_API_CACHE_DIR"] = os.getenv("TERN_API_CACHE_DIR")
tern_app.config["TERN_DEFAULT_REGISTRY"] = os.getenv("TERN_DEFAULT_REGISTRY")

tern_tasks = Executor(tern_app)
tern_app.config["TERN_TASKS"] = tern_tasks
