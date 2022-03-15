#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import pytest
from werkzeug.test import TestResponse

from app import tern_app
from tests.utils import RequestDataTest


@pytest.fixture
def api_request():
    def _api_request(request_data: RequestDataTest) -> TestResponse:
        with tern_app.test_client() as api_client:
            with tern_app.app_context():
                if request_data.method.lower() == "get":
                    response = api_client.get(
                        request_data.endpoint, json=request_data.payload
                    )

                elif request_data.method.lower() == "post":
                    response = api_client.post(
                        request_data.endpoint, json=request_data.payload
                    )

                elif request_data.method.lower() == "put":
                    response = api_client.put(
                        request_data.endpoint, json=request_data.payload
                    )

                elif request_data.method.lower() == "delete":
                    response = api_client.delete(
                        request_data.endpoint, json=request_data.payload
                    )

                else:
                    raise ValueError("Invalid HTTP method")

                return response

    return _api_request
