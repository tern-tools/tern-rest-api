#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
from dataclasses import dataclass, field
from typing import Any, Dict

from attr import asdict
from flask import jsonify
from flask.wrappers import Response


@dataclass
class TernAPIResponse:
    data: Dict[str, Any] = field(default_factory=dict)
    status_code: int = 200
    errors: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the dataclass data to a dictionary.

        :return: Response data as a dictionary
        :rtype: ``dict``
        """
        return asdict(self)

    def to_response(self) -> Response:
        """Converts the dataclass data to a Flask jsonified format, building a
        consistent response format for the requests to the API.

        :return: Flask Response
        :rtype: ``flask.wrappers.Response``
        """
        response_data = dict()
        response_data["data"] = self.data
        if self.errors:
            response_data["error"] = self.errors

        jsonified_response = jsonify(response_data)
        if self.status_code != 200:
            jsonified_response.status_code = self.status_code

        return jsonified_response
