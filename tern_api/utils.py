#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from dataclasses import dataclass, field
from typing import Any, Dict

from attr import asdict
from flask import jsonify


@dataclass
class TernAPIResponse:
    data: Dict[str, Any] = field(default_factory=dict)
    status_code: int = 200
    errors: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)

    def to_response(self):
        response_data = dict()
        response_data["data"] = self.data
        if self.errors:
            response_data["error"] = self.errors

        jsonified_response = jsonify(response_data)
        if self.status_code != 200:
            jsonified_response.status_code = self.status_code

        return jsonified_response
