#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from enum import Enum


class task_status(Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
