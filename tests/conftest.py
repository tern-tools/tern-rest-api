# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import pytest
from werkzeug.test import TestResponse

from app import tern_api
from tests.utils import RequestDataTest


@pytest.fixture
def api_request():
    def _api_request(request_data: RequestDataTest) -> TestResponse:
        with tern_api.test_client() as api_client:
            with tern_api.app_context():
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
                    raise ValueError("Invalid HTTP methord")

                return response

    return _api_request
