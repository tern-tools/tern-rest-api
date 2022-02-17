# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RequestDataTest:
    method: str
    endpoint: str
    payload: Dict[str, Any]
